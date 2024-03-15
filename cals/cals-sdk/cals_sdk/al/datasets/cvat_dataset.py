from PIL import Image
from torch.utils.data import Dataset


class CVATDataset(Dataset):
    def __init__(self, task):
        self.task = task
        self.id = task.id
        self.name = task.name
        self.metadata = task.get_meta()
        self.start = self.metadata['start_frame']
        self.end = self.metadata['stop_frame']

        self.labels = {}
        for label in task.get_labels():
            self.labels[label.id] = label.name

        self.annotations = {}
        for annotation in task.get_annotations()['shapes']:
            frame_id = annotation.frame
            if frame_id not in self.annotations:
                self.annotations[frame_id] = []

            self.annotations[frame_id].append(annotation)

    def __len__(self):
        return self.end - self.start + 1

    def __getitem__(self, idx):
        frameBytes = self.task.get_frame(idx + self.start)
        frame = Image.open(frameBytes)
        anno = self.annotations[idx + self.start]
        return frame, anno

    def get_label_name(self, label_id):
        return self.labels[label_id]