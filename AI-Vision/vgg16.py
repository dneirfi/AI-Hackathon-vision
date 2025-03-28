# -*- coding: utf-8 -*-

from __future__ import print_function

from keras.models import Model
from keras.layers import Flatten, Dense, Input
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from keras.utils.data_utils import get_file
#import utils
import pickle
import warnings
warnings.filterwarnings("ignore")


DATA_DIR = 'data/'
WEIGHTS_FILE = 'vgg16_weights_th_dim_ordering_th_kernels.h5'
PCA_FILE = 'PCAmatrices.mat'
IMG_SIZE = 1024

def download(url, file_name):
    with open(file_name, "wb") as file:
        response=get(url)
        file.write(response.content)

def save_obj(obj, filename):
    f = open(filename, 'wb')
    pickle.dump(obj, f)
    f.close()
    #print "Object saved to %s." % filename


def load_obj(filename):
    f = open(filename, 'rb')
    obj = pickle.load(f)
    f.close()
    #print "Object loaded from %s." % filename
    return obj


def preprocess_image(x):

    # Substract Mean
    x[:, 0, :, :] -= 103.939
    x[:, 1, :, :] -= 116.779
    x[:, 2, :, :] -= 123.68

    # 'RGB'->'BGR'
    x = x[:, ::-1, :, :]

    return x

def VGG16(weights_path = None, input_shape = (3, 224, 224)):
    
    # Determine proper input shape
    img_input = Input(shape=input_shape)
    
    # Block 1
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='block1_conv1')(img_input)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='block2_conv1')(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv1')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv2')(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv1')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv2')(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    # Classification block
    x = Flatten(name='flatten')(x)
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dense(1000, activation='softmax', name='predictions')(x)

    # Create model
    model = Model(img_input, x)

    # Load pre-trained weights if available
    if weights_path:
        model.load_weights(weights_path)

    return model


if __name__ == '__main__':
   
    weights = get_file('VGGweights','https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg16_weights_th_dim_ordering_th_kernels.h5')
    #weights_path = DATA_DIR + WEIGHTS_FILE
    #weights_path = vgg16_weights_th_dim_ordering_th_kernels.h5
    #model = VGG16(weights_path)
    
    model = VGG16(weights)
    #print(model.summary())
