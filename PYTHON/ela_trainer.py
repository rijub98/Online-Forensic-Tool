from fileinput import filename
import sys, os, numpy as np

from keras.models import Sequential
from sklearn.model_selection import train_test_split

from trainer_helper import generate_cnn_model_vgg16
from trainer_helper import plot_model_accuracy
from trainer_helper import plot_model_loss
from trainer_helper import get_image_dataset_details
from trainer_helper import generate_ela_dataset_cv2
from ela_trainer import main_fcn

def main_fn():
  i = 0
  model_folder_path = "model_" + str(i)
  while os.path.exists(model_folder_path):
    i = i + 1
    model_folder_path = "model_" + str(i)

  os.mkdir(model_folder_path)

  print(model_folder_path)

  X = []
  Y = []
  
  filenames = ["../images/MICC-F220/groundtruthDB_220.txt", "../images/MICC-F2000/groundtruthDB_2000.txt","../images/CASIA2.0_revised/groundtruth.txt"]
  main_fcn(filenames)

  for file in filenames:
      training_src_dir = os.path.dirname(file)
      dataset = get_image_dataset_details(file)

      X_temp, Y_temp = generate_ela_dataset_cv2(dataset, training_src_dir, ".")

      if len(X):
          X = np.append(X, X_temp, axis=0)
      else:
          X = X_temp

      if len(Y):
          Y = np.append(Y, Y_temp, axis=0)
      else:
          Y = Y_temp

  model = generate_cnn_model_vgg16()

  # X -> rgb pixel value of every image
  # Y -> categorical value which states whether image is tampered or original

  X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=5, shuffle=True)

  history = model.fit(X_train, Y_train, batch_size=10, epochs=14, validation_data=(X_val, Y_val), verbose=2)

  model_filename = os.path.join(model_folder_path, "trained_ela_model.h5")
  model.save(model_filename)

  plot_model_accuracy(history, model_folder_path)
  plot_model_loss(history, model_folder_path)
