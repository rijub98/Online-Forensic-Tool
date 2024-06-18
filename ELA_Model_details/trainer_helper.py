import sys
import os
import numpy as np

from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam
from keras.applications.vgg16 import VGG16

from ela_analysis import ela_cv2


def get_image_dataset_details(filename):

    if not filename:
        filename = input("Enter the filename: ")

    assert os.path.exists(filename), "Could not find file at: " + str(filename)

    fo = open(filename)

    image_list = []

    while True:

        line = fo.readline()

        if not line:
            break

        x = line.lstrip()
        x = x.split()

        if x:
            image_list.append(x)

    fo.close()
    return image_list


def generate_ela_dataset_cv2(input_dataset, dataset_folder_path, model_folder_path):
    X = []
    Y = []
    resize_factor = (128,128)

    for image_detail in input_dataset:
        image_file = os.path.join(dataset_folder_path, image_detail[0])
        X.append(np.array(ela_cv2(image_file, 90, resize_factor, model_folder_path)).flatten() / 255.0)
        Y.append(image_detail[1])

    X = np.array(X)
    Y = to_categorical(Y, 2)
    X = X.reshape(-1, 128, 128, 3)

    return X, Y


def generate_cnn_model_vgg16():

    vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
    
    model = Sequential()

    for layer in vgg_conv.layers[:-5]:
        layer.trainable = False

    for layer in vgg_conv.layers:
        print(layer, layer.trainable)

    model.add(vgg_conv)
    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(2, activation='softmax'))

    model.summary()

    opt = Adam(learning_rate=1e-3, epsilon=0.1)
    model.compile(loss='binary_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    
    return model


def plot_model_accuracy(history, model_folder_path):

    acc = history.history["accuracy"]
    test_acc = history.history["val_accuracy"]
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'b', label='Training Set')
    plt.plot(epochs, test_acc, 'g', label='Testing Set')
    plt.ylim(0.5, 1.0)
    
    plt.title("Accuracy History Plot") 
    plt.legend()
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")

    plotFile = os.path.join(model_folder_path, "accuracy_plot.png")
    plt.savefig(plotFile)
    plt.close()

    np_acc = np.array(acc)
    with open(os.path.join(model_folder_path, 'train_acc.npy'), 'wb') as f:
      np.save(f, np_acc)
    
    np_test_acc = np.array(test_acc)
    with open(os.path.join(model_folder_path, 'test_acc.npy'), 'wb') as f:
      np.save(f, np_test_acc)
    
    np_epochs = np.array(epochs)
    with open(os.path.join(model_folder_path, 'acc_epochs.npy'), 'wb') as f:
      np.save(f, np_epochs)


def plot_model_loss(history, model_folder_path):

    loss = history.history["loss"]
    test_loss = history.history["val_loss"]
    epochs = range(len(loss))
    
    plt.plot(epochs, loss, 'b', label='Training Set')
    plt.plot(epochs, test_loss, 'g', label='Testing Set')
    plt.ylim(0, 1.0)

    plt.title("Loss History Plot") 
    plt.legend()
    plt.xlabel("Epochs")
    plt.ylabel("Loss")

    plotFile = os.path.join(model_folder_path, "loss_plot.png")
    plt.savefig(plotFile)
    plt.close()

    np_loss = np.array(loss)
    with open(os.path.join(model_folder_path, 'train_loss.npy'), 'wb') as f:
      np.save(f, np_loss)
    
    np_test_loss = np.array(test_loss)
    with open(os.path.join(model_folder_path, 'test_loss.npy'), 'wb') as f:
      np.save(f, np_test_loss)
    
    np_epochs = np.array(epochs)
    with open(os.path.join(model_folder_path, 'loss_epochs.npy'), 'wb') as f:
      np.save(f, np_epochs)