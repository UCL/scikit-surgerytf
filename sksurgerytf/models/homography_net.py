# -*- coding: utf-8 -*-

"""
Module to implement HomographyNet by Daniel Detone et al. (2016).

The paper is on
`arXiv.org
<https://arxiv.org/abs/1606.03798>`_.

Again, this was written as a learning exercise, and as a tutorial, but
is actually useful!
"""
import os
import sys
import logging
import datetime
import platform
import ssl
from pathlib import Path
import numpy as np
from tensorflow import keras
import cv2


from sksurgerytf import __version__

LOGGER = logging.getLogger(__name__)


class HomographyNet:
    """
    Class to encapsulate HomographyNet by Daniel DeTone et al (2016).
    """
    def __init__(self,
                 logs="logs/fit",
                 weights=None,
                 learning_rate=0.001,
                 epochs=1
                 ):
        """
        Class to implement HomographyNet and provide entry
        points for both training and testing.

        If the constructor is called without weights, the data is loaded
        and a full training cycle is performed in order to learn the weights.

        If the constructor is called with weights, these are loaded, as is,
        with no further training.

        :param logs: relative path to folder to write tensorboard log files.
        :param weights: file name prefix of pre-saved weights.
        :param learning_rate: float, default=0.001 which is the Keras default.
        :param epochs: int, default=1
        """
        self.logs = logs
        self.learning_rate = learning_rate
        self.epochs = epochs

        LOGGER.info("Creating HomographyNet with log dir: %s.",
                    str(self.logs))
        LOGGER.info("Creating HomographyNet with weights file: %s.",
                    str(weights))
        LOGGER.info("Creating HomographyNet with learning_rate: %s.",
                    str(self.learning_rate))
        LOGGER.info("Creating HomographyNet with epochs: %s.",
                    str(self.epochs))

        # To fix issues with SSL certificates on CI servers.
        ssl._create_default_https_context = ssl._create_unverified_context

        self.model = None

        self.build_model()

        if weights is not None:
            self.model.load_weights(weights)
        else:
            self.load_data()
            self.train()

    def load_data(self):
        """
        Loads the data.
        """
        pass

    @staticmethod
    def __preprocess_data(images):
        """
        Pre-processes the data. For this data set we just:

          - To Do.

        :param images: (m x 28 x 28) numpy, RGB, [0-255], uchar
        :return: normalised (m x 28 x 28) numpy, RGB, [0-1], float
        """
        pass

    def build_model(self):
        """
        Constructs the neural network.

          - To Do

        """
        pass

    def train(self):
        """
        Method to train the neural network.

        Uses:

          - To Do

        :return: output of self.model.evaluate on test set.
        """

        log_dir = os.path.join(Path(self.logs),
                               datetime.datetime.now()
                               .strftime("%Y%m%d-%H%M%S"))
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir,
                                                           histogram_freq=1)

    def test(self, image_a, image_b):
        """
        Method to compute the homograpy between two images.

        :param image_a: (28 x 28), numpy, RGB, [0-255], uchar.
        :param image_b: (28 x 28), numpy, RGB, [0-255], uchar.
        :return: (params, matrix)
        """
        normalised_a = self.__preprocess_data(image_a)
        img_a = (np.expand_dims(normalised_a, 0))
        normalised_b = self.__preprocess_data(image_b)
        img_b = (np.expand_dims(normalised_b, 0))
        predictions = self.model.predict(img_a, img_b)
        return predictions

    def save_weights(self, filename):
        """
        Method to save the network weights to disk.

        :param filename: file to save to
        """
        self.model.save_weights(filename)


def run_homography_net_model(logs,
                             weights,
                             image_a,
                             image_b,
                             save):
    """
    Helper function to run the HomographyNet model from
    the command line entry point.

    :param logs: directory for log files for tensorboard.
    :param weights: file of previously trained weights
    :param image_a: first of a pair of images to test
    :param image_b: second of a pair of images to test
    :param save: file to save weights to
    """
    # pylint: disable=line-too-long
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    LOGGER.info("Starting homography_net.py version: %s", __version__)
    LOGGER.info("Starting homography_net.py with platform: %s.", str(platform.uname()))
    LOGGER.info("Starting homography_net.py with cwd: %s.", os.getcwd())
    LOGGER.info("Starting homography_net.py with path: %s.", sys.path)

    fmn = HomographyNet(logs, weights)

    if save is not None:
        fmn.save_weights(save)

    if image_a is not None and image_b is not None:
        img_a = cv2.imread(image_a)
        img_a_as_rgb = cv2.cvtColor(img_a, cv2.COLOR_BGR2RGB)
        img_b = cv2.imread(image_b)
        img_b_as_rgb = cv2.cvtColor(img_b, cv2.COLOR_BGR2RGB)

        params, matrix = fmn.test(img_a_as_rgb, img_b_as_rgb)

        LOGGER.info("Images: %s, %s give:\n%s\n%s",
                    image_a, image_b, params, matrix)
