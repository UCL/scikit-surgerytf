# coding=utf-8

"""
Tests for sksurgeryfashion which is a demo app, based on MNIST Fashion, from TF Tutorials.
"""

import pytest
import numpy as np
import cv2
import sksurgerytf.models.fashion as f


def test_train_then_test(setup_output_dir_for_fashion_tests):
    fmnist = f.FashionMNIST()
    img = fmnist.get_test_image(2)
    cv2.imwrite('tests/output/fashion/test_train_then_test.png', img)
    class_index, class_name = fmnist.test(img)
    class_names = fmnist.get_class_names()
    assert class_name == class_names[class_index]
    fmnist.save_model('tests/output/fashion/test_train_then_test.h5')


def test_load_weights_then_test(setup_output_dir_for_fashion_tests):
    fmnist = f.FashionMNIST('logs/fit', 'tests/data/fashion/test_train_then_test.h5')
    img = cv2.imread('tests/data/fashion/test_train_then_test.png')
    greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    class_index, class_name = fmnist.test(greyscale)
    class_names = fmnist.get_class_names()
    assert class_name == class_names[class_index]


def test_run_fashion_model(setup_output_dir_for_fashion_tests):
    f.run_fashion_model('logs/fit',
                        'tests/data/fashion/test_train_then_test.h5',
                        'tests/output/fashion/test_run_fashion_model.h5',
                        'tests/data/fashion/test_train_then_test.png'
                        )
