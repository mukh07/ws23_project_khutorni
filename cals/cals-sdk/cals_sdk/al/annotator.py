import os

import cv2
import torch
import numpy as np
import torch.nn as nn
from mmpose.apis import MMPoseInferencer


class KeypointAnnotator(nn.Module):
    """ A wrapper for MMPoseInferencer. 
    
    This is used by the auto-annotation module to run inference on images
    for the active learning workflow.
    """
    def __init__(self, config, checkpoint, device='cuda'):
        super().__init__()
        self._device = torch.device(device)
        self._model = MMPoseInferencer(config, checkpoint, device=device)

    def forward(self, image_path: str, **kwargs):
        result_generator = self._model(image_path, **kwargs)
        return next(result_generator)

    def predict(self, image_path: str, annos: list, 
                filter_indices: list = None,
                filter_threshold: float = 0.5):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        detections = []
        with torch.no_grad():
            for idx, anno in enumerate(annos):
                # Crop the image using GT bounding box
                x, y, w, h = anno['bbox']
                x, y, w, h = int(x), int(y), int(w), int(h)
                if x < 0 or y < 0 or w <= 0 or h <= 0:
                    continue

                # Temporarily save the cropped image
                cropped_image = image[y:y+h, x:x+w, :]
                cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
                temp_path = 'temp.jpg'
                cv2.imwrite(temp_path, cropped_image)

                # Run inferencer
                result = self.forward(temp_path)
                result = result['predictions'][0]

                if len(result) == 0:
                    continue
                result = result[0]

                # Remove the temporary image
                os.remove(temp_path)

                # Get the keypoints and scores
                keypoints, scores = result['keypoints'], result['keypoint_scores']
                keypoints = np.array(keypoints)
                scores = np.array(scores)

                # Filter the keypoints
                if filter_indices is None:
                    filter_indices = list(range(len(keypoints)))

                # Compute average score based on the filtered indices
                avg_score = np.mean(scores[filter_indices])

                # Compute a good/bad attribute based on the average score
                good = avg_score >= filter_threshold

                # Copy the GT keypoints and only update the keypoints in the filtered indices
                gt_keypoints = np.array(anno['keypoints']).reshape(-1, 3)
                gt_keypoints[filter_indices, :2] = keypoints[filter_indices]
                gt_keypoints[filter_indices, 2] = 1
                gt_keypoints = gt_keypoints.reshape(-1).tolist()

                # Count number of keypoints with non-zero visibility
                # num_visible_keypoints = np.sum(gt_keypoints[2::3] > 0)

                # Add the result to the list
                det = anno.copy()
                det['keypoints'] = gt_keypoints
                det['keypoint_scores'] = scores.tolist()
                # det['num_keypoints'] = num_visible_keypoints
                det['score'] = avg_score
                if 'attributes' not in det:
                    det['attributes'] = {}
                det['attributes']['good'] = 1 if good else 0

                detections.append(det)
        return detections

