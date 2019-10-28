# -*- coding: utf-8 -*-

"""
Module to implement a classifier for the Fashion MNIST dataset.

Inspired by
`TensorFlow tutorials
<https://www.tensorflow.org/tutorials/keras/classification>`_.

"""
import logging
import copy
import numpy as np
from tensorflow import keras
import cv2

LOGGER = logging.getLogger(__name__)


class FashionMNIST:
    """
    Class to encapsulate a classifier for the Fashion MNIST dataset.
    """
    def __init__(self, weights=None):
        """
        Class to implement a 10-class classifier for the Fashion MNIST dataset,
        and provide entry points for both training and testing.

        If the constructor is called without weights, the data is loaded
        and a full training cycle is performed in order to learn the weights.

        If the constructor is called with weights, these are loaded, as is,
        with no further training.

        :param weights file name of pre-saved weights.
        """
        self.model = None
        self.train_images = None
        self.train_labels = None
        self.test_images = None
        self.test_labels = None
        self.class_names = ['T-shirt/top', 'Trouser', 'Pullover',
                            'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker',
                            'Bag', 'Ankle boot']

        self.build_model()

        if weights is not None:
            self.model.load_weights(weights)
        else:
            self.load_data()
            self.train()

    def get_class_names(self):
        """
        Returns a copy of the valid class names.
        :return: list of strings
        """
        return copy.deepcopy(self.class_names)

    def load_data(self):
        """
        Loads the data.

        fashion_mnist is available from TF/Keras directly, and fortunately,
        it get's cached on your computer. So, subsequent calls are fast.
        """
        (self.train_images, self.train_labels), \
            (self.test_images, self.test_labels) = \
            keras.datasets.fashion_mnist.load_data()

        self.train_images = self.__preprocess_data(self.train_images)
        self.test_images = self.__preprocess_data(self.test_images)

    @staticmethod
    def __preprocess_data(images):
        """
        Pre-processes the data. For this data set we just:

          - Normalise unsigned char [0-255] to [0-1] float.

        :param images (m x 28 x 28) numpy, single channel, [0-255], uchar
        :returns normalised (m x 28 x 28) numpy, single channel, [0-255], float
        """
        return images / 255.0

    def build_model(self):
        """
        Constructs the neural network.

          - 128 node FC + relu
          - 10 node FC + softmax

        """
        self.model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation='relu'),
            keras.layers.Dense(10, activation='softmax')
        ])

        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

        self.model.summary()

    def train(self):
        """
        Method to train the neural network.

        Uses:

          - Adam optimiser
          - sparse_categorical_crossentropy cost function
          - evaluates accuracy metric

        Default parameters for demo purposes, 10 epochs.
        """
        self.model.fit(self.train_images, self.train_labels, epochs=10)

        self.model.evaluate(self.test_images,
                            self.test_labels,
                            verbose=2)

    def test(self, image):
        """
        Method to test a single (28 x 28) image.

        :param image: (28 x 28), numpy, single channel, [0-255], uchar.
        :return: (class_index, class_name)
        """
        normalised = self.__preprocess_data(image)
        img = (np.expand_dims(normalised, 0))
        predictions = self.model.predict(img)
        class_index = np.argmax(predictions[0])
        return class_index, self.class_names[class_index]

    def save_weights(self, filename):
        """
        Method to save the network weights to disk.
        :param filename: file to save to
        """
        self.model.save_weights(filename)

    def get_test_image(self, index):
        """
        Extracts an image from the test data. Useful for unit testing,
        as the original data comes packaged up in a zip file.

        :param index: int [0-9999], unchecked
        :return: image, (28 x 28), numpy, single channel, [0-255], uchar.
        """
        if self.test_images is None:
            self.load_data()
        img = self.test_images[index, :, :]
        reshaped = img.reshape([28, 28])
        rescaled = reshaped * 255
        output = rescaled.astype(np.uint8)
        return output


def run_fashion_model(load, image, save):
    """
    Helper function to run the Fashion MNIST model from
    the command line entry point.

    :param load: file of previously trained weights
    :param image: image to test
    :param save: file to save weights to
    """

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

    fmn = FashionMNIST(load)

    if save is not None:
        fmn.save_weights(save)

    if image is not None:
        img = cv2.imread(image)
        greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        class_index, class_name = fmn.test(greyscale)
        LOGGER.info("Image: %s, categorised as: %s:%s",
                    image, class_index, class_name)
