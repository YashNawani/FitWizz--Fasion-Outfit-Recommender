import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras import layers
from tensorflow.keras import losses

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers.experimental.preprocessing import StringLookup

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import cv2

import matplotlib.image as mpimg


def my_le(styles):
    articleTypeLB = LabelEncoder()
    genderLB = LabelEncoder()
    baseColourLB = LabelEncoder()
    seasonLB = LabelEncoder()
    usageLB = LabelEncoder()
 
    styles['articleType'] = articleTypeLB.fit_transform(styles['articleType'])
    styles['gender'] = genderLB.fit_transform(styles['gender'])
    styles['baseColour'] = baseColourLB.fit_transform(styles['baseColour'])
    styles['season'] = seasonLB.fit_transform(styles['season'])
    styles['usage'] = usageLB.fit_transform(styles['usage'])
    return styles, articleTypeLB, genderLB, baseColourLB, seasonLB, usageLB


def get_234_df(x):
    styles = pd.read_csv("styles.csv", error_bad_lines=False)
    styles = styles.drop(["productDisplayName"], axis=1)
    styles = styles.drop(["year"], axis=1)
    styles = styles[(styles.masterCategory == 'Apparel') | (styles.masterCategory == 'Footwear')]
    styles = styles.drop(styles[styles["subCategory"] == "Innerwear"].index)
    styles = styles.dropna()
    

def build_model(width, height, articleTypeLB, genderLB, baseColourLB, seasonLB, usageLB):
    res50 = keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(80, 60, 3))
    res50.trainable = False
    inputs = keras.Input(shape=(width, height, 3), name="images")
    x = res50(inputs, training=False)
    x = layers.Flatten()(x)
    x = layers.Dense(1024, activation='relu')(x)
 
    article_branch = make_branch(x, len(articleTypeLB.classes_), 'softmax', 'articleType')
    gender_branch = make_branch(x, len(genderLB.classes_), 'softmax', 'gender')
    color_branch = make_branch(x, len(baseColourLB.classes_), 'softmax', 'baseColour')
    season_branch = make_branch(x, len(seasonLB.classes_), 'softmax', 'season')
    usage_branch = make_branch(x, len(usageLB.classes_), 'softmax', 'usage')
 
    model = keras.Model(inputs=inputs, outputs=[article_branch, gender_branch, color_branch, season_branch, usage_branch])
    return model