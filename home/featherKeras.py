from keras.models import Sequential
from keras.layers import Dense, LeakyReLU
from keras.layers.core import Activation
from keras.layers.convolutional import Conv2D
from keras.layers.core import Flatten
import numpy as np
import h5py
from keras.models import Model
from keras import backend as K
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def discriminator_model():
    model = Sequential()
    model.add(
        Conv2D(32, (5, 5),
               padding='same',
               strides=(2, 2),
               input_shape=(128, 128, 3))
    )
    model.add(LeakyReLU(alpha=0.2))

    model.add(Conv2D(64, (5, 5), padding='same', strides=(2, 2)))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Conv2D(128, (5, 5), padding='same', strides=(2, 2)))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Conv2D(256, (5, 5), padding='same', strides=(2, 2)))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Conv2D(512, (5, 5), padding='same', strides=(2, 2)))
    model.add(LeakyReLU(alpha=0.2))

    model.add(Conv2D(1024, (5, 5), padding='same', strides=(2, 2)))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Flatten())

    model.add(Activation('relu'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.summary()
    return model

def get_mat(mat_path):
    # mat = h5py.File(mat_path, 'r')
    # mat_m = np.transpose(mat['m'])
    mat_m = np.load(mat_path)
    mat_m = mat_m.astype(np.float32) / 3.5 - 1
    return mat_m

class featherEtrKeras:
    def get_feather(self, path, batch_size=1):
        d_old = discriminator_model()
        d_old.load_weights(root + '/data/checkpoint/discriminator_94_400')
        d = Model(inputs=d_old.input, outputs=d_old.get_layer('flatten_1').output)
        d.summary()
        d.trainable = False
        x_mb = np.array([get_mat(f) for f in path])
        f = d.predict(x_mb.reshape([batch_size, 128, 128, 3]))
        K.clear_session()
        return f

