import tempfile
from typing import List

import cvat_sdk.models as models
import cvat_sdk.auto_annotation as cvataa
from cvat_sdk import Client
import PIL.Image

from cals_sdk.al.annotator import KeypointAnnotator


class AnnotationTask(cvataa.DetectionFunction):
    """ A keypoint annotator using a pre-trained model.
     
    It uses a pre-trained MMPose model to detect keypoints in an image and automatically
    annotate them in CVAT. The model is loaded from a configuration file and a checkpoint.

    Args:
        config (str): The path to the model configuration file.
        checkpoint (str): The path to the model checkpoint.
        device (str): The device to run the model on. Defaults to 'cuda'.
    """
    def __init__(self, config: str, checkpoint: str, device='cuda') -> None:
        self._model = KeypointAnnotator(config, checkpoint, device=device)

    @property
    def spec(self) -> cvataa.DetectionFunctionSpec:
        # describe the annotations
        return cvataa.DetectionFunctionSpec(
            labels=[
                cvataa.skeleton_label_spec("person", 0, [
                    cvataa.keypoint_spec("1", 0),
                    cvataa.keypoint_spec("2", 1),
                    cvataa.keypoint_spec("3", 2),
                    cvataa.keypoint_spec("4", 3),
                    cvataa.keypoint_spec("5", 4),
                    cvataa.keypoint_spec("6", 5),
                    cvataa.keypoint_spec("7", 6),
                    cvataa.keypoint_spec("8", 7),
                    cvataa.keypoint_spec("9", 8),
                    cvataa.keypoint_spec("10", 9),
                    cvataa.keypoint_spec("11", 10),
                    cvataa.keypoint_spec("12", 11),
                    cvataa.keypoint_spec("13", 12),
                    cvataa.keypoint_spec("14", 13),
                    cvataa.keypoint_spec("15", 14),
                    cvataa.keypoint_spec("16", 15),
                    cvataa.keypoint_spec("17", 16),
                    cvataa.keypoint_spec("18", 17),
                    cvataa.keypoint_spec("19", 18),
                    cvataa.keypoint_spec("20", 19),
                    cvataa.keypoint_spec("21", 20),
                    cvataa.keypoint_spec("22", 21),
                    cvataa.keypoint_spec("23", 22),
                ]),
            ]
        )

    def detect(self, context, image: PIL.Image.Image) -> List[models.LabeledShapeRequest]:
        # save image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            image_path = f.name
            image.save(image_path)

            # run the ML model
            detections = self._model(image_path)

        # parse results
        request = []
        for detection in detections:
            keypoints = detection['keypoints']

            # convert keypoints to CVAT format
            sublabels = []
            for i in range(len(keypoints)):
                sublabels.append(cvataa.keypoint(i, keypoints[i].tolist()))

            label = cvataa.skeleton(0, sublabels)
            request.append(label)

        return request

    def annotate(self, client: Client, task_id: int) -> None:
        # start the annotation process
        cvataa.annotate_task(client, task_id, self)


