#!/bin/bash

# make the directory structure
mkdir -p data/coco/annotations
mkdir -p data/coco/val2017
mkdir -p data/coco/train2017

# change to the directory
cd data/coco

# download the annotations
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip

# unzip the annotations
unzip annotations_trainval2017.zip 'annotations/person_keypoints_val2017.json' 'annotations/person_keypoints_train2017.json' -d .

# move the annotations to the appropriate folder
mv annotations/person_keypoints_val2017.json annotations/
mv annotations/person_keypoints_train2017.json annotations/

# remove the extra files
rm -rf annotations
rm annotations_trainval2017.zip

# download the validation and training images
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/zips/train2017.zip

# unzip the images
unzip val2017.zip -d val2017/
unzip train2017.zip -d train2017/

# remove the zip files
rm val2017.zip
rm train2017.zip
