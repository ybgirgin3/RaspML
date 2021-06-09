import os
import sys
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from termcolor import colored

# Root directory of the project
# ROOT_DIR = os.path.abspath("../../")
ROOT_DIR = os.path.abspath("./")  # currnet directory
print(ROOT_DIR)

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log



# directory of dataset 
DATASET_DIR = os.path.join(ROOT_DIR,"datasets/apples")
print(DATASET_DIR)

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class FruitConfig(Config):
    """Configuration for training on the fruit dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "apple"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1   ####

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + fruit

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

config = FruitConfig()
config.display()



class InferenceConfig(config.__class__):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


inference_config = InferenceConfig()
inference_config.display()


# ekran kartını kullan
DEVICE = "/gpu:0"

with tf.device(DEVICE):
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=inference_config)

model_path = COCO_MODEL_PATH
print("Loading weights from ", model_path)
#model.load_weights(model_path, by_name=True)
model.load_weights(model_path, by_name=True, 
                        exclude=[ "mrcnn_class_logits", 
                                  "mrcnn_bbox_fc", 
                                  "mrcnn_bbox", 
                                  "mrcnn_mask"])

from fruit import FruitDataset
dataset_val = FruitDataset()
dataset_val.load_fruit(DATASET_DIR, "val")
dataset_val.prepare()

image_id = random.choice(dataset_val.image_ids)

# 2, 3 ve 4. değerini almalıyız
original_image = gt_class_id, gt_bbox, gt_mask = list(modellib.load_image_gt(dataset_val, inference_config, image_id, use_mini_mask=False))[1:4]
# ret = modellib.load_image_gt(dataset_val, inference_config, image_id, use_mini_mask=False)
# print(f"ret: {colored(ret, 'yellow')}")
# with open("ret.txt", "a") as f:
#     f.write(str(ret))

info = dataset_val.image_info[image_id]
print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], image_id, 
                                       dataset_val.image_reference(image_id)))

visualize.display_instances(original_image, gt_bbox, gt_mask, gt_class_id,
                             dataset_val.class_names, figsize=(8,8))


log("original_image", original_image)
# log("image_meta", image_meta)
log("gt_class_id", gt_class_id)
log("gt_bbox", gt_bbox)
log("gt_mask", gt_mask)

