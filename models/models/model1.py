# -*- coding: utf-8 -*-
"""Model 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a_q0gwb2Rq8wwBBW8JKlQwuYllQ_OLob
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from webcolors import CSS3_HEX_TO_NAMES, hex_to_rgb
from scipy.spatial import KDTree
import PIL.Image as Image
import cv2
from google.colab import drive

