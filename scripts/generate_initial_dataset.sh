SPLIT=${1:-val2017}

python src/generate_initial_dataset.py \
  --coco_path data/coco \
  --coco_split $SPLIT \
  --save_path data/coco-extended \
  --min_keypoints 3 \
  --min_keypoint_score 0.3 \
  --min_bbox_score 0.5 \
  --min_bbox_area 32 \
  --min_bbox_overlap 0.7