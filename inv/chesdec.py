# system related
import os
import sys
sys.path.append('../src/')
# import custom modules
import helpers as hp
#import mammoscan as ms
# path manipulation
from pathlib import Path
# regex
import re
# plotting
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle
# data manipulation / preparation
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# image manipulation
from PIL import Image
from IPython.display import Image
# metrics
from sklearn.metrics import confusion_matrix, classification_report
# keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPool2D, Dropout
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

mammo = hp.create_mias_dataset('info.txt')



def clean_ds_files(df: pd.DataFrame) -> pd.DataFrame:
 '''Removes records with invalid data
 and cast x and y to float'''
 new_df = df.copy()
 # search for invalid x values for removal
 indices = new_df.x[lambda x: x == '*NOTE'].index
 
 for idx in indices:
   n_idx = new_df.index.get_loc(idx)
   # drop from dataset
   new_df.drop(new_df.index[n_idx], inplace=True)
   # delete from directory
   delete_image(idx)
  # make x and y float values
   new_df.x = new_df.x.astype(float)
   new_df.y = new_df.y.astype(float)
 
 return new_df


mias = hp.generate_subsamples('../all-mias/', mias)