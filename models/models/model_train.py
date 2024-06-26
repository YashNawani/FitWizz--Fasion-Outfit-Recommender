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


def group_color(styles):
    styles["colorgroup"] = -1
    styles.loc[(styles.baseColour=='Red')|
           (styles.baseColour=='Brown')|
           (styles.baseColour=='Coffee Brown')|
           (styles.baseColour=='Maroon')|
           (styles.baseColour=='Rust')|
           (styles.baseColour=='Burgundy')|
           (styles.baseColour=='Mushroom Brown'),"colorgroup"] = 0
    styles.loc[(styles.baseColour=='Copper'),"colorgroup"] = 1
    styles.loc[(styles.baseColour=='Orange')|
               (styles.baseColour=='Bronze')|
               (styles.baseColour=='Skin')|
               (styles.baseColour=='Nude'),"colorgroup"] = 2
    styles.loc[(styles.baseColour=='Gold')|
               (styles.baseColour=='Khaki')|
               (styles.baseColour=='Beige')|
               (styles.baseColour=='Mustard')|
               (styles.baseColour=='Tan')|
               (styles.baseColour=='Metallic'),"colorgroup"]= 3
    styles.loc[(styles.baseColour=='Yellow'),"colorgroup"] = 4
    styles.loc[(styles.baseColour=='Lime Green'),"colorgroup"]= 5
    styles.loc[(styles.baseColour=='Green')|
           (styles.baseColour=='Sea Green')|
           (styles.baseColour=='Fluorescent Green')|
           (styles.baseColour=='Olive'),"colorgroup"] = 6
    styles.loc[(styles.baseColour=='Teal')|
           (styles.baseColour=='Turquoise Blue'),"colorgroup"] = 7
    styles.loc[(styles.baseColour=='Blue'),"colorgroup"]= 8
    styles.loc[(styles.baseColour=='Navy Blue'),"colorgroup"] = 9
    styles.loc[(styles.baseColour=='Purple')|
           (styles.baseColour=='Lavender'),"colorgroup"] = 10
    styles.loc[(styles.baseColour=='Pink')|
           (styles.baseColour=='Magenta')|
           (styles.baseColour=='Peach')|
           (styles.baseColour=='Rose')|
           (styles.baseColour=='Mauve'),"colorgroup"] = 11
    styles.loc[(styles.baseColour=='Black')|
           (styles.baseColour=='Charcoal'),"colorgroup"] = 12
    styles.loc[(styles.baseColour=='White')|
           (styles.baseColour=='Off White')|
           (styles.baseColour=='Cream'),"colorgroup"] = 13
    styles.loc[(styles.baseColour=='Grey')|
           (styles.baseColour=='Silver')|
           (styles.baseColour=='Taupe')|
           (styles.baseColour=='Grey Melange'),"colorgroup"] = 14
    styles.loc[(styles.baseColour=='Multi'),"colorgroup"] = 15  

def df_drop(styles, col, item):
    for i in item:
        styles = styles.drop(styles[styles[col] == i].index)
    return styles

def get_df():
    styles = pd.read_csv("styles.csv", error_bad_lines=False)
    styles = styles.drop(["productDisplayName"], axis=1)
    styles = styles.drop(["year"], axis=1)
    styles = styles[(styles.masterCategory == 'Apparel') | (styles.masterCategory == 'Footwear')]
    styles = styles.drop(styles[styles["subCategory"] == "Innerwear"].index)
    styles = styles.dropna()
    styles = df_drop(styles, "subCategory", ["Apparel Set", "Dress", "Loungewear and Nightwear", "Saree", "Socks"])
    styles["subCategory"] = styles["subCategory"].transform(lambda x: "Footwear" if (x in ["Shoes", "Flip Flops", "Sandal"]) else x)
    styles = styles.drop(labels=[6695, 16194, 32309, 36381, 40000], axis=0)
    
    # Filter only top, bottom, and shoes categories
    styles = styles[styles["subCategory"].isin(["Top", "Bottom", "Shoes"])]

    group_color(styles)
    return styles

def make_input_array_subcate(df):
    train_images = np.zeros((len(df.id), 80, 60, 3))
    for i in range(len(df.id)):
        ID = df.id.iloc[i]
        path = f"images/{ID}.jpg"
        img = cv2.imread(path)
        if img.shape != (80, 60, 3):
            img = image.load_img(path, target_size=(80, 60, 3))
        train_images[i] = img

    data = tf.data.Dataset.from_tensor_slices(
        (
            {
                "images": train_images
            },
            {
                "subCategory": df[["subCategory"]]
            }
        )
    )
    return data

def make_branch(res_input, n_out, act_type, name):
    z = layers.Dense(512, activation="relu")(res_input)
    z = layers.Dense(256, activation='relu')(z)
    z = layers.Dense(128, activation='relu')(z)
    z = layers.Dense(64, activation='relu')(z)
    z = layers.Dense(n_out)(z)
    z = layers.Activation(act_type, name=name)(z)
    return z


def build_model(width, height):
    res50 = keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(80, 60, 3))
    res50.trainable = False
    inputs = keras.Input(shape=(width, height, 3), name="images")
    x = res50(inputs, training=False)
    
    x = layers.Flatten()(x)
    x = layers.Dense(1024, activation='relu')(x)

    sub_branch = make_branch(x, 3, 'softmax', 'subCategory')  # Adjusted to classify into 3 categories: top, bottom, shoes

    model = keras.Model(inputs=inputs, outputs=[sub_branch])
    return model
