import cv2
import numpy as np
import os
import pandas as pd
import pickle
import tarfile
from keras.applications import InceptionResNetV2
from keras.applications import VGG16
from keras.callbacks import ModelCheckpoint
from keras.layers import GlobalAveragePooling2D
from keras.layers import LeakyReLU
from keras.layers.core import Dropout
from keras.layers.core import Flatten
from keras.layers.core import Dense
from keras.layers.convolutional import Conv2D
from keras.models import load_model
from keras.models import Sequential
from keras.models import Model
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from urllib.request import urlopen

TRAIN_PATH = 'MO444_dogs/train/'
VAL_PATH = 'MO444_dogs/val/'
TEST_PATH = 'MO444_dogs/test/'
MODEL_FILENAME = 'model_incep_RMS.h5'
HISTORY_FILENAME = 'history_incep_RMS.pkl'

def create_test_folders():
    test_labels = pd.read_csv("MO444_dogs_test.txt", sep=' ', header=None)

    for l in range(len(test_labels.iloc[:])):
        data_filename = test_labels[1][l].split('/')[-1:][0]
        label = test_labels[2][l]

        if not os.path.exists(TEST_PATH + str(label)):
            os.mkdir(TEST_PATH + str(label))
        os.rename(TEST_PATH + data_filename, TEST_PATH + str(label) + '/' +
                                                                  data_filename)

def create_class_folders(path):
    if path == TRAIN_PATH:
        create_test_folders()
    for file in os.listdir(path):
        label = file[:2]
        image = cv2.imread(path + file)
        if image is not None:
          # Create directory
            if not os.path.exists(path + label):
                os.mkdir(path + label)
            os.rename(path + file, path + label + '/' + file)

# Download the Dataset
dogs = urlopen("http://www.recod.ic.unicamp.br/~feandalo/MO444_dogs.tar.gz")
with open('dogs.tar.gz','wb') as output:
    output.write(dogs.read())

# Extract files
tf = tarfile.open("dogs.tar.gz")
tf.extractall()

# Organize files based on their classes
create_class_folders(TRAIN_PATH)
create_class_folders(VAL_PATH)
create_class_folders(TEST_PATH)

"""# Pre Processing"""

data_augmentation = ImageDataGenerator(rescale = 1./255, horizontal_flip = True,
               fill_mode = "nearest", zoom_range = 0.3, width_shift_range = 0.3,
               height_shift_range=0.3, rotation_range=30)

""" Get generators """

train_generator = data_augmentation.flow_from_directory(
    TRAIN_PATH,
    target_size = (299, 299),
    batch_size = 64,
    class_mode = "categorical"
)

validation_generator = ImageDataGenerator(rescale=1./255).flow_from_directory(
    VAL_PATH,
    target_size = (299, 299),
    class_mode = "categorical"
)

test_generator = ImageDataGenerator(rescale=1./255).flow_from_directory(
    TEST_PATH,
    target_size=(299, 299),
    class_mode="categorical"
)

""" Modeling """

base_model = InceptionResNetV2(weights='imagenet', include_top=False,
                                                    input_shape = (299, 299, 3))

# Freeze the layers of the base model
for layer in base_model.layers:
    layer.trainable = False

# Add layers and create a model
x = base_model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.3)(x)
output = Dense(83, activation="softmax")(x)
model = Model(input = base_model.input, output = output)

""" Optimizers """
# opt = SGD(lr=0.0001, momentum=0.9)
# opt = Adam(lr=0.0001)
opt = RMSprop(lr=0.0001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['acc'])

""" Training """
checkpoint = ModelCheckpoint(filepath=MODEL_FILENAME, monitor='val_loss',
                                                verbose=1, save_best_only=True)
history = model.fit_generator(
    train_generator,
    validation_data = validation_generator,
    validation_steps = validation_generator.samples /
                                                validation_generator.batch_size,
    epochs = 10,
    verbose = 1,
    steps_per_epoch = train_generator.samples / train_generator.batch_size,
    callbacks = [checkpoint]
)

# Saving logs
with open(HISTORY_FILENAME, 'wb') as file:
  pickle.dump(history.history, file)

""" Testing model """

# Read the model to test it
model = load_model(MODEL_FILENAME)

evalu = model.evaluate_generator(test_generator,
              steps=test_generator.samples/test_generator.batch_size, verbose=1)

print("(loss, accuracy): {}".format(evalu))
