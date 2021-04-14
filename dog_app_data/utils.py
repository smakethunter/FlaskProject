from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import tensorflow_hub as hub
import tensorflow as tf
import matplotlib.pyplot as plt

BATCH_SIZE = 1
NUM_IMAGES = 1
IMG_SIZE=224
labels_breed=pd.read_csv('/home/smaket/PycharmProjects/flaskProject2/dog_app_data/labels.csv')['breed'].to_numpy()

breeds=np.unique(labels_breed)
print(len(breeds))
def img_to_tensor(imagepath,IMG_SIZE=224,img_type='jpeg'):
  image = tf.io.read_file(imagepath)
  # deode filepath
  if img_type=='jpeg':
   image = tf.image.decode_jpeg(image,channels=3)
  else:
    image=tf.image.decode_png(image,channels=3)
  # normalize colour channel to 0-1 scale
  image = tf.image.convert_image_dtype(image,tf.float32)
  #resize image
  image=tf.image.resize(image,[IMG_SIZE,IMG_SIZE])
  return image
def get_image_label(image_path,label):
  image = img_to_tensor(imagepath=image_path)
  #label=tf.constant(label)
  return image , label

def get_batch(x, y=None, batch_size=BATCH_SIZE, valid=False, buffer_size=NUM_IMAGES, image_type='jpeg'):
    """
    Creates batches of data in pairs (x,y)
    it shuffles data if it's training data,
    doesn't shuffle if it's validation
    Accepts test data.
    """
    # Test data
    if y is None:
        print("Creating test batches")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(x)))
        data_batch = data.map(lambda x: img_to_tensor(x, img_type=image_type)).batch(batch_size)

    elif valid:
        print("Creating valid data batches")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(x),
                                                   tf.constant(y)))
        data_batch = data.map(get_image_label).batch(batch_size)
    else:
        print("Creating train batches")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(x),
                                                   tf.constant(y)))
        data.shuffle(buffer_size=buffer_size)
        data = data.map(get_image_label)

        data_batch = data.batch(batch_size)
    return data_batch


def unbatch_data(targets):
  imgs=[]

  for imgs_ in targets.unbatch().as_numpy_iterator():
    imgs.append(imgs_)

  return imgs
def plot_model_guesses(predictions, true_label, index):
    top10 = np.sort(predictions)[index][-10:]
    print(top10)
    breed_names = []
    proba = []
    for idx, pred in enumerate(predictions[index]):
        if pred in top10:
            pred *= 100
            breed_names.append(breeds[idx])
            proba.append(pred)
    summary = pd.DataFrame({'breed': breed_names, 'propability': proba})
    summary = summary.sort_values(by='propability')

    fig, ax = plt.subplots(figsize=(12,12))
    top_plot = plt.bar(summary['breed'], summary['propability'])
    ax.set_xticks(breed_names)
    ax.set_title('Top 10 guesses')
    ax.set_ylabel("Confidence in %")
    ax.set_xticklabels(breed_names, rotation=45)

    true = breeds[np.argmax(true_label)]
    if true in breed_names:
        top_plot[np.argmax(summary['breed'].apply(lambda x: x == true))].set_color("green")
    return fig
def predict_and_visualize(model,targets, index=0, random=False):
    imgs = unbatch_data(targets)


    predictions = model.predict(targets, verbose=1)
    print(predictions)
    fig,ax = plt.subplots(figsize=(6,6))

    ax.imshow(imgs[index])

    ax.set_title(
        f"predicted_label: {breeds[predictions[index].argmax()]}  Confidence:{np.max(predictions[index])*100:.2f}%",
        color='green')
    ax.set_xticks([])
    ax.set_yticks([])

    fig2 = plot_model_guesses(predictions, [breeds[predictions[index].argmax()]], index)
    return fig, fig2


if __name__ =="__main__":

    image = 'dog.jpeg'
    # image = tf.io.read_file(image)
    # image = tf.image.decode_image(image, channels=3)
    # image = tf.image.convert_image_dtype(image,tf.float32)
    # image = tf.image.resize(image,[224,244])

    print(len(breeds))
    path_to_model = '20210413-173553-whole_data_adam_mnv2.h5'
    breed_predictor = load_model(path_to_model, custom_objects={"KerasLayer":hub.KerasLayer})


    img = get_batch([image], batch_size=1)
    # print(img.shape)
    breed_predictor.summary()
    # pred = breed_predictor.predict(img)
    predict_and_visualize(breed_predictor,img)
    import matplotlib.pyplot as plt

    plt.show()
