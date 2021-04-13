from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow_hub as hub
import tensorflow as tf

print(tf.executing_eagerly())
image = 'dog.png'
image = tf.io.read_file(image)
image = tf.image.decode_png(image, channels=3)
image = tf.image.convert_image_dtype(image,tf.float32)
image = tf.image.resize(image,[224,244])
img = image
path_to_model = '20210413-173553-whole_data_adam_mnv2.h5'
breed_predictor = load_model(path_to_model, custom_objects={"KerasLayer":hub.KerasLayer})
list_of_breeds = pd.read_csv('labels.csv')['breed'].to_list()
pred = breed_predictor.predict(img)
print(img.shape)
breed_predictor.summary()
import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()