from torchvision.datasets import CocoDetection

from .active_dataset_wrapper import ActiveDatasetWrapper


class KeypointDataset(ActiveDatasetWrapper):
    def __init__(self, root, anno_file, transforms=None, **kwargs):
        super().__init__(CocoDetection(root, anno_file, transforms, **kwargs))
        self.coco = self.dataset.coco
        self.ids = self.dataset.ids
        self.root = root

    def __getitem__(self, idx):
        return self.dataset[idx]
    
    def __len__(self):
        return len(self.dataset)

    def _create_batch(self, indices: list):
        """ Create a batch of data.

        Args:
            indices (list): The indices of the batch.

        Returns:
            dict: The batch data.
        """
        # Select batch images
        batch_images = [self.coco.loadImgs(self.ids[idx])[0]
                         for idx in indices]

        # Select batch annotations
        batch_annos = []
        for idx in indices:
            ann_ids = self.coco.getAnnIds(imgIds=self.ids[idx])
            annotations = self.coco.loadAnns(ann_ids)
            batch_annos.extend(annotations)

        # Create COCO-like batch (see https://cocodataset.org/#format-data)
        # info and licenses stay the same as the complete dataset
        return {
            'info': self.coco.dataset['info'],
            'licenses': self.coco.dataset['licenses'],
            'images': batch_images,
            'annotations': batch_annos,
        }

