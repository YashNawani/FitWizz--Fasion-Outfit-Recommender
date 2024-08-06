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

#!zip -r '"foot_model.zip"' '"foot_model"'
foot_history = foot_base_model.fit(foot_train,
                    epochs=5,
                    steps_per_epoch = 2000,
                    validation_data = foot_val)
 
foot_base_model.evaluate(foot_test)
 
foot_base_model.save("/content/drive/MyDrive/model_2.2")


def make_input_xx(x):
    x_input = x.shuffle(buffer_size=len(x))
    x_train_size = int(0.6 * len(x_input))
    x_val_size = int(0.2 * len(x_input))
    x_train = x_input.take(x_train_size).batch(2)
    x_val = x_input.skip(x_train_size).take(x_val_size).batch(2)
    x_test = x_input.skip(x_train_size + x_val_size).batch(2)
    return x_train, x_val, x_test
 
train_module.py
 
  
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
    """
    This function drops certain columns
    input: styles, dataframe
        col, the item we want to drop in this coloumn
        item, which item we want to drop 
    """
    for i in item:
        styles = styles.drop(styles[styles[col] == i].index)
    return styles

def get_df():
    styles = pd.read_csv("styles.csv", error_bad_lines=False)
    styles = styles.drop(["productDisplayName"], axis=1)
    styles = styles.drop(["year"], axis=1)
    styles = styles[(styles.masterCategory=='Apparel')| (styles.masterCategory=='Footwear')]
    styles = styles.drop(styles[styles["subCategory"] == "Innerwear"].index)
    styles = styles.dropna()
    styles = df_drop(styles,"subCategory", ["Apparel Set", "Dress","Loungewear and Nightwear","Saree","Socks"])
    styles["subCategory"] = styles["subCategory"].transform(lambda x: "Footwear" if(x in ["Shoes","Flip Flops","Sandal"]) else x)
    styles = styles.drop(labels=[6695,16194,32309,36381,40000], axis=0)
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
            {"images": train_images},
            {"subCategory": df[["subCategory"]]}
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
    x = layers.Conv2D(32, (2, 2), activation='relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(1024, activation='relu')(x)
    sub_branch = make_branch(x, len(le.classes_), 'softmax', 'subCategory')
    model = keras.Model(inputs=inputs, outputs=[sub_branch])
    return model




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
    styles = df_drop(styles, "subCategory", ["Apparel Set", "Dress", "Loungewear and Nightwear", "Saree", "Socks"])
    styles["subCategory"] = styles["subCategory"].transform(lambda x: "Footwear" if (x in ["Shoes", "Flip Flops", "Sandal"]) else x)
    styles = styles.drop(labels=[6695, 16194, 32309, 36381, 40000], axis=0)
    styles = styles[styles.subCategory == x]
    group_color(styles)
    styles.baseColour = styles.colorgroup
    return styles
    

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

