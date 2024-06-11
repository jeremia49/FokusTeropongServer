import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
from sklearn.neighbors import KernelDensity
from sklearn.metrics import mean_squared_error
import glob
import os 
import json

class Detection():
    def __init__(self):
        self.load_encoder_interpreter()
        self.encoder_output_shape = self.encoder_interpreter.get_output_details()[0]['shape']
        self.IMGSIZE = 256
        self.loadKDE()

    
    def load_encoder_interpreter(self):
        self.encoder_interpreter = tflite.Interpreter(model_path = 'encoder_pucukrebung.tflite')
        self.interpreter = tflite.Interpreter(model_path = 'pucukrebung.tflite')


    def encode(self,img):
        print("encoding...")
        input_details = self.encoder_interpreter.get_input_details()
        output_details = self.encoder_interpreter.get_output_details()

        input_type = input_details[0]['dtype']

        self.encoder_interpreter.allocate_tensors()

        np_features = img.astype(input_type)
        np_features = np.expand_dims(np_features, axis = 0)

        self.encoder_interpreter.set_tensor(input_details[0]['index'],np_features)

        self.encoder_interpreter.invoke()

        output = self.encoder_interpreter.get_tensor(output_details[0]['index'])
        return output


    def predict(self, img):
        print("predicting...")
        # print()
        # print("Input Details :")
        # print(input_details)
        # print()
        # print("Output Details :")
        # print(output_details)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        input_type = input_details[0]['dtype']

        self.interpreter.allocate_tensors()

        np_features = img.astype(input_type)
        np_features = np.expand_dims(np_features, axis = 0)

        self.interpreter.set_tensor(input_details[0]['index'],np_features)

        self.interpreter.invoke()
        output = self.interpreter.get_tensor(output_details[0]['index'])
        return output
    
    def loadKDE(self):
        if("pucukrebung.npy" not in os.listdir('./kde/')):
            encoded_images = []
            fpath = "./pucukrebung/"
            for filename in glob.glob(fpath+"*.jpg"):
                img  = Image.open(filename)
                img = np.array(img.resize((self.IMGSIZE,self.IMGSIZE), Image.ANTIALIAS))
                img = img / 255.
                encoded_images.append(self.encode(img))

            out_vector_shape = self.encoder_output_shape[1]*self.encoder_output_shape[2]*self.encoder_output_shape[3]
            self.encoded_images_vector = [np.reshape(img, (out_vector_shape)) for img in encoded_images]
            np.save('./kde/pucukrebung', self.encoded_images_vector)
        else:
            self.encoded_images_vector = np.load('./kde/pucukrebung.npy')

        self.kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(self.encoded_images_vector)

    def calcKDE(self, encoded_img):
        out_vector_shape = self.encoder_output_shape[1]*self.encoder_output_shape[2]*self.encoder_output_shape[3]
        return self.kde.score_samples([np.reshape(encoded_img, (out_vector_shape))] )[0] 

    def calcerr(self, truth, pred):
        return mean_squared_error(truth,pred,)

    def checkAnomaly(self,img):
        img = Image.open(img)
        img = np.array(img.resize((256,256), Image.ANTIALIAS))
        img = img / 255.

        encodedimg = self.encode(img)
        density = self.calcKDE(encodedimg)

        reconstruct = self.predict(img)
        reconstruct_err = self.calcerr(img.reshape(-1), reconstruct.reshape(-1))

        return (density,reconstruct_err)




# s = predict(img)

# Setup KDE


    
# a = Detection()

# img  = Image.open('./test.jpg')
# print(a.checkAnomaly(img))




# def check_anomaly(img_path):
#     density_threshold = 4100 #Set this value based on the above exercise
#     reconstruction_error_threshold = 0.02 # Set this value based on the above exercise
#     img  = Image.open(img_path)
#     img = np.array(img.resize((448,448), Image.ANTIALIAS))
    

#     img = img / 255.
#     img = img[np.newaxis, :,:,:]
#     encoded_img = model.predict([[img]]) 
#     encoded_img = [np.reshape(img, (out_vector_shape)) for img in encoded_img] 
#     density = kde.score_samples(encoded_img)[0] 

#     reconstruction = model.predict([[img]])
#     reconstruction_error = model.evaluate([reconstruction],[[img]], batch_size = 1)[0]

#     print("Density", density)
#     print("Reconstruction Error :", reconstruction_error)
#     print(density < density_threshold)
#     print(reconstruction_error > reconstruction_error_threshold)

#     if density < density_threshold or reconstruction_error > reconstruction_error_threshold:
#         print("The image is an anomaly")
        
#     else:
#         print("The image is NOT an anomaly")

        
# SIZE = 448

# modelname = "pucukrebung"
# model = tf.keras.models.load_model(modelname+".keras")

# batch_size = 64
# datagen = ImageDataGenerator(validation_split=0.1,
#                              rescale=1./255)

# train_generator = datagen.flow_from_directory(
#     'dataset',
#     target_size=(SIZE, SIZE),
#     batch_size=batch_size,
#     subset='training',
#     class_mode='input'
# )

# #Get encoded output of input images = Latent space
# encoded_images = model.predict_generator(train_generator)

# # Flatten the encoder output because KDE from sklearn takes 1D vectors as input
# encoder_output_shape = model.output_shape #Here, we have 8x8x8
# out_vector_shape = encoder_output_shape[1]*encoder_output_shape[2]*encoder_output_shape[3]

# encoded_images_vector = [np.reshape(img, (out_vector_shape)) for img in encoded_images]

# #Fit KDE to the image latent data
# kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(encoded_images_vector)

# out_vector_shape = (SIZE, SIZE)


# def check_anomaly(img_path):
#     density_threshold = 4100 #Set this value based on the above exercise
#     reconstruction_error_threshold = 0.02 # Set this value based on the above exercise
#     img  = Image.open(img_path)
#     img = np.array(img.resize((448,448), Image.ANTIALIAS))
    

#     img = img / 255.
#     img = img[np.newaxis, :,:,:]
#     encoded_img = model.predict([[img]]) 
#     encoded_img = [np.reshape(img, (out_vector_shape)) for img in encoded_img] 
#     density = kde.score_samples(encoded_img)[0] 

#     reconstruction = model.predict([[img]])
#     reconstruction_error = model.evaluate([reconstruction],[[img]], batch_size = 1)[0]

#     print("Density", density)
#     print("Reconstruction Error :", reconstruction_error)
#     print(density < density_threshold)
#     print(reconstruction_error > reconstruction_error_threshold)

#     if density < density_threshold or reconstruction_error > reconstruction_error_threshold:
#         print("The image is an anomaly")
        
#     else:
#         print("The image is NOT an anomaly")

        