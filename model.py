from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, ZeroPadding2D
from keras.layers.core import Flatten, Dense, Dropout
import h5py
from keras import backend as K
from keras.utils.conv_utils import convert_kernel
import tensorflow as tf
import numpy as np


# Model definition
def get_model(first_layer):
    
    # from keras import applications
    # model = applications.VGG16(include_top=False, weights='imagenet')

    model = Sequential()
    
    model.add(first_layer)
    model.add(Conv2D(64, 3, 3, activation='relu', name='conv1_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(64, 3, 3, activation='relu', name='conv1_2'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(128, 3, 3, activation='relu', name='conv2_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(128, 3, 3, activation='relu', name='conv2_2'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, 3, 3, activation='relu', name='conv3_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, 3, 3, activation='relu', name='conv3_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(256, 3, 3, activation='relu', name='conv3_3'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv4_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv4_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv4_3'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv5_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv5_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Conv2D(512, 3, 3, activation='relu', name='conv5_3'))
    model.add(MaxPool2D((2, 2), strides=(2, 2)))
    
    # model.summary()

    return model


def load_model_weights(model, weights_path):
    print('Loading model.')

    # Load pre-trained model
    model.load_weights(weights_path, by_name=True)

    # Tensoflow to Theano - depends on the version
    ops = []
    for layer in model.layers:
        if layer.__class__.__name__ in ['Conv2D']: # Layers with pre-trained weights
            original_w = K.get_value(layer.kernel)
            converted_w = convert_kernel(original_w)
            ops.append(tf.assign(layer.kernel, converted_w).op)
    K.get_session().run(ops)

    # Prev code
    # f = h5py.File(weights_path)
    # for k in range(f.attrs['nb_layers']):
    #     if k >= len(model.layers):
    #         # we don't look at the last (fully-connected) layers in the savefile
    #         break
    #     g = f['layer_{}'.format(k)]
    #     weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
    #     model.layers[k].set_weights(weights)
    # f.close()

    # model.save_weights(weights_path)
    print('Model loaded.')
    return model

# Return output of specified layer
def get_output_layer(model, layer_name):
    layer_dict = dict([(layer.name, layer) for layer in model.layers])
    layer = layer_dict[layer_name]
    return layer.output
