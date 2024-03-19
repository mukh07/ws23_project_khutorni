import datetime
import glob
import os
from pathlib import Path
import json
from typing import List, Optional
import random
import shutil
from zipfile import ZipFile

from cals_sdk.al.annotator import KeypointAnnotator
from cals_sdk.al.datasets import KeypointDataset
from src.datasets.datasets.body.coco_extended_dataset import CocoExtendedDataset
from cals_sdk.cvat import CVATClient


class ActiveLearningWorkflow:
    """
    Defines an active learning workflow.

    Attributes:
        model: Model to be used for active learning.
        dataset: Dataset to be used for active learning.
        batch_size: Number of samples to be selected in each iteration.
        project_id: ID of the CVAT project to be used for annotation.
        work_dir: Directory to be used for storing the active learning workflow.
        data_cfg: Keyword arguments to be passed to the dataset.
    """

    # coco_extended_model = "configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py"
    # inferencer = MMPoseInferencer(pose2d=coco_extended_model)

    def __init__(self, client: CVATClient, root, anno_file, model, batch_size,project_id, work_dir,
                 data_cfg={}, description=None, query_strategy="aggregate-threshold-uncertainty-sampling"):
        self.client = client
        self.model = "/home/khutorni/project/ws23_project_khutorni/configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py"
        self.dataset = KeypointDataset(root, anno_file)
        self.batch_size = batch_size
        self.project_id = project_id
        self.work_dir = work_dir
        self.data_cfg = data_cfg

        # Set filtering parameters
        self.filter_indices = [17, 18, 19, 20, 21, 22]
        self.filter_threshold = 0.5

        # Create work directory if it does not exist
        self.completed_dir = os.path.join(self.work_dir, 'completed')
        self.active_dir = os.path.join(self.work_dir, 'selected')
        self.queued_dir = os.path.join(self.work_dir, 'queued')
        self._create_work_dirs()

        # Initialize the batches
        if self.status == 'init':
            self._init_batches()
            self.status = 'ready'

        self._save_workflows_metadata(model, description, query_strategy)

    def _save_workflows_metadata(self, model: str, description: Optional[str], query_strategy: str):
        workflows_file = '/home/khutorni/project/ws23_project_khutorni/data/workflows.json'
        with open(workflows_file, "r+") as f:
            try:
                workflows_data = json.load(f)  # Load existing data
            except json.JSONDecodeError:
                workflows_data = {"workflows": []}  # Default value if file is empty or invalid

            workflows = workflows_data['workflows']
            name = Path(self.work_dir).name
            this_workflow_index = next((i for i, w in enumerate(workflows) if w['name'] == name), None)
            this_workflow_data = dict(
                name=name,
                project_id=self.project_id,
                batch_size=self.batch_size,
                model=model,
                description=description,
                query_strategy=query_strategy,
            )
            if this_workflow_index is not None:
                this_workflow_data['created_at'] = workflows[this_workflow_index]['created_at']
                this_workflow_data['description'] = workflows[this_workflow_index]['description']
                this_workflow_data['query_strategy'] = workflows[this_workflow_index]['query_strategy']
                workflows[this_workflow_index] = this_workflow_data
            else:
                this_workflow_data['created_at'] = datetime.datetime.now().isoformat()
                workflows.append(this_workflow_data)

            f.seek(0)  # Seek to the start of the file before writing
            f.truncate()  # Truncate the file to overwrite it
            json.dump(dict(workflows=workflows), f)  # Dump the updated data back into the file

    @staticmethod
    def get_all_workflows_metadata() -> List[dict]:
        data_folder = '/home/khutorni/project/ws23_project_khutorni/data'
        workflows_file = data_folder + '/workflows.json'
        with open(workflows_file, "r") as f:
            workflows = json.load(f)['workflows']

        enriched_workflows = []
        for w in workflows:
            w_folder = f"{data_folder}/{w['name']}"
            completed = len(glob.glob(f'{w_folder}/completed/*.zip'))
            queued = len(glob.glob(f'{w_folder}/queued/*.json'))
            selected_json_files = glob.glob(f'{w_folder}/selected/*.json')
            if len(selected_json_files) > 0:
                selected = int(
                    Path(selected_json_files[0]).name.__str__()[len('batch_'):-len('.json')]
                )
            else:
                selected = None
            with open(f"{w_folder}/metadata.json") as wf:
                metadata = json.load(wf)

            w['model'] = Path(w['model']).name.split(".")[0]
            enriched_workflows.append(dict(
                **w,
                completed=completed,
                queued=queued,
                selected=selected,
                metadata=metadata
            ))

        return enriched_workflows

    def _create_work_dirs(self):
        """
        Creates the work directories if they do not exist.
        """
        os.makedirs(self.completed_dir, exist_ok=True)
        os.makedirs(self.active_dir, exist_ok=True)
        os.makedirs(self.queued_dir, exist_ok=True)

    def _init_batches(self):
        """
        Initializes the batches for the active learning workflow.
        """
        # Split the dataset into batches
        splits = self.dataset.create_batches(batch_size=self.batch_size)

        # Save the batches
        for idx, split in enumerate(splits):
            batch_file = os.path.join(self.queued_dir, f'batch_{idx}.json')
            with open(batch_file, 'w') as f:
                json.dump(split, f)

    def _read_metadata(self):
        """
        Reads the metadata file.
        """
        metadata_file = os.path.join(self.work_dir, 'metadata.json')
        if not os.path.exists(metadata_file):
            with open(metadata_file, 'w') as f:
                json.dump({
                    'status': 'init',
                    'current_task': None,
                }, f)

        with open(metadata_file, 'r') as f:
            return json.load(f)

    def _update_metadata(self, key, value):
        """
        Saves the metadata file.
        """
        metadata = self._read_metadata()
        metadata[key] = value

        metadata_file = os.path.join(self.work_dir, 'metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)

    @property
    def status(self):
        """
        Returns the status of the active learning workflow.
        """
        metadata = self._read_metadata()
        return metadata['status']

    @status.setter
    def status(self, status):
        """
        Saves the status of the active learning workflow.
        """
        self._update_metadata('status', status)

    @property
    def completed(self):
        """
        Returns the list of completed batches.
        """
        return sorted([f for f in os.listdir(self.completed_dir) if f.endswith('.json')])

    @property
    def queued(self):
        """
        Returns the list of queued batches.
        """
        return sorted([f for f in os.listdir(self.queued_dir) if f.endswith('.json')])

    @property
    def current_batch(self):
        """
        Returns the id of the current batch.
        """
        # Get file names in the active directory
        active_files = [f for f in os.listdir(self.active_dir) if f.endswith('.json')]
        if len(active_files) == 0:
            return None
        
        if len(active_files) > 1:
            raise Exception('More than one active batch found.')
        
        current_batch = int(active_files[0].split('.')[0].split('_')[1])
        return current_batch

    @property
    def num_batches(self):
        """
        Returns the total number of batches.
        """
        active = 0 if self.current_batch is None else 1
        return len(self.completed) + len(self.queued) + active

    def _find_next_batch(self):
        """
        Finds the next batch to be selected.
        """
        # Check if there are any queued batches
        if len(self.queued) > 0:
            next_batch = self.queued[0]
            next_idx = int(next_batch.split('.')[0].split('_')[1])
            return next_idx

        # No batches found
        return None

    def select_next_batch(self):
        """
        Selects the next batch for annotation.
        """
        # Get the current batch
        current_batch = self.current_batch
        if current_batch is not None:
            # Move the current batch to the completed directory
            batch_file = os.path.join(self.active_dir, f'batch_{current_batch}.json')
            os.rename(batch_file, os.path.join(self.completed_dir, f'batch_{current_batch}.json'))

            # Move the zip file to the completed directory
            zip_file = os.path.join(self.active_dir, f'batch_{current_batch}.zip')
            os.rename(zip_file, os.path.join(self.completed_dir, f'batch_{current_batch}.zip'))

            # TODO: Set task status to completed on the annotation tool (CVAT)
            self._update_metadata('current_task', None)

        # Select the next batch
        default_batch = self._find_next_batch()
        next_idx = default_batch if self.current_batch is None else self.current_batch + 1

        # Check if the next batch exists
        if next_idx >= self.num_batches:
            raise Exception('No more batches to select.')

        return self.select_batch(next_idx)

    def select_batch(self, batch_idx):
        """
        Selects a batch for annotation.
        """
        # Make sure the batch exists
        batch_file = os.path.join(self.queued_dir, f'batch_{batch_idx}.json')
        if not os.path.exists(batch_file):
            raise Exception(f'Cound not find batch {batch_idx} annotations in {self.queued_dir}.')

        # Move the batch from queued to inprogress
        anno_file = os.path.join(self.active_dir, f'batch_{batch_idx}.json')
        os.rename(batch_file, anno_file)

        # Zip the images in the batch
        images_zip = self._zip_batch_images(anno_file, batch_idx)

        # Update status and metadata
        self.status = 'busy'

        return batch_idx, images_zip, anno_file

    def filter_batch(self, batch_idx, images_zip, anno_file):
        """
        Uses the model to filter the annotations in a batch.

        Returns:
            filtered_zip: Zip file containing the filtered images.
            filtered_anno: Annotation file containing the filtered annotations.
        """
        # Extract the zip file to a temporary directory in the work directory
        temp_dir = os.path.join(self.work_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        with ZipFile(images_zip, 'r') as f:
            f.extractall(temp_dir)

        # Create a new dataset from the batch annotations
        batch_dataset = KeypointDataset(temp_dir, anno_file, **self.data_cfg)

        # Run the model on the batch dataset
        predictions = self._run_model(batch_dataset, 
                                      filter_indices=self.filter_indices,
                                      filter_threshold=self.filter_threshold)

        # Delete the temporary directory
        shutil.rmtree(temp_dir)

        # Split the predictions into good and bad
        good = [p for p in predictions if p['attributes']['good'] == 1]
        bad = [p for p in predictions if p['attributes']['good'] != 1]

        good_annos = {
            'info': batch_dataset.coco.dataset['info'],
            'licenses': batch_dataset.coco.dataset['licenses'],
            'categories': batch_dataset.coco.dataset['categories'],
            'images': batch_dataset.coco.dataset['images'],
            'annotations': good
        }

        bad_annos = {
            'info': batch_dataset.coco.dataset['info'],
            'licenses': batch_dataset.coco.dataset['licenses'],
            'categories': batch_dataset.coco.dataset['categories'],
            'images': batch_dataset.coco.dataset['images'],
            'annotations': bad
        }

        # Move good predictions to the completed directory
        postfix = random.randint(0, 1000)
        batch_idx_good = f'{batch_idx}_{postfix}'
        good_anno_file = os.path.join(self.completed_dir, f'batch_{batch_idx_good}.json')
        with open(good_anno_file, 'w') as f:
            json.dump(good_annos, f)

        # Save the bad predictions to the active directory
        with open(anno_file, 'w') as f:
            json.dump(bad_annos, f)

        # Create a new zip file
        images_zip = self._zip_batch_images(anno_file, batch_idx)

        return images_zip, anno_file

    def _run_model(self, batch_dataset, filter_indices, filter_threshold):
        """
        Runs the model on the batch dataset.
        """
        model = KeypointAnnotator(
            "/home/khutorni/project/ws23_project_khutorni/configs/rtmpose-l_8xb256-420e_coco_extended-256x192.py.py",
            "/home/khutorni/project/ws23_project_khutorni/.tmp/checkpoint"
        )
        predictions = []
        for _, target in batch_dataset:
            if len(target) == 0:
                continue

            image_id = target[0]['image_id']
            
            # find file name
            file_name = None
            for image in batch_dataset.coco.dataset['images']:
                if image['id'] == image_id:
                    file_name = image['file_name']
                    break

            if file_name is None:
                raise Exception(f'Could not find image with id {image_id}.')


            image_path = os.path.join(batch_dataset.root, file_name)
            prediction = model.predict(image_path, target, filter_indices, filter_threshold)
            predictions.extend(prediction)
        return predictions

    def upload_batch(self, images_zip, anno_file) -> int:
        """
        Uploads the annotations for a batch.

        Returns:
            task_id: ID of the task created in the annotation tool.
        """
        task_id = self.client.upload_task_data(
            name=f'batch_{self.current_batch}',
            images_zip=images_zip,
            annotations_file=anno_file,
            project_id=self.project_id
        )

        self._update_metadata('current_task', task_id)
        return task_id

    def _zip_batch_images(self, anno_file, batch_idx):
        """
        Zips the images in a batch.
        """
        # Load the batch
        with open(anno_file, 'r') as f:
            batch = json.load(f)

        # Zip the images
        zip_file = os.path.join(self.active_dir, f'batch_{batch_idx}.zip')
        with ZipFile(zip_file, 'w') as f:
            for image in batch['images']:
                image_path = os.path.join(self.dataset.root, image['file_name'])
                f.write(image_path, arcname=image['file_name'])

        return zip_file
    
