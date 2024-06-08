import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random

from sklearn.neighbors import KernelDensity

SIZE = 448

modelname = "pucukrebung"
model = tf.keras.models.load_model(modelname+".keras")

batch_size = 64
datagen = ImageDataGenerator(validation_split=0.1,
                             rescale=1./255)

train_generator = datagen.flow_from_directory(
    'dataset',
    target_size=(SIZE, SIZE),
    batch_size=batch_size,
    subset='training',
    class_mode='input'
)

#Get encoded output of input images = Latent space
encoded_images = model.predict_generator(train_generator)

# Flatten the encoder output because KDE from sklearn takes 1D vectors as input
encoder_output_shape = model.output_shape #Here, we have 8x8x8
out_vector_shape = encoder_output_shape[1]*encoder_output_shape[2]*encoder_output_shape[3]

encoded_images_vector = [np.reshape(img, (out_vector_shape)) for img in encoded_images]

#Fit KDE to the image latent data
kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(encoded_images_vector)

out_vector_shape = (SIZE, SIZE)


def check_anomaly(img_path):
    density_threshold = 4100 #Set this value based on the above exercise
    reconstruction_error_threshold = 0.02 # Set this value based on the above exercise
    img  = Image.open(img_path)
    img = np.array(img.resize((448,448), Image.ANTIALIAS))
    

    img = img / 255.
    img = img[np.newaxis, :,:,:]
    encoded_img = model.predict([[img]]) 
    encoded_img = [np.reshape(img, (out_vector_shape)) for img in encoded_img] 
    density = kde.score_samples(encoded_img)[0] 

    reconstruction = model.predict([[img]])
    reconstruction_error = model.evaluate([reconstruction],[[img]], batch_size = 1)[0]

    print("Density", density)
    print("Reconstruction Error :", reconstruction_error)
    print(density < density_threshold)
    print(reconstruction_error > reconstruction_error_threshold)

    if density < density_threshold or reconstruction_error > reconstruction_error_threshold:
        print("The image is an anomaly")
        
    else:
        print("The image is NOT an anomaly")

        