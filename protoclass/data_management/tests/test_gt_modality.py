""" Test the class T2W modality. """

import numpy as np
import os

from numpy.testing import assert_equal
from numpy.testing import assert_array_equal
from numpy.testing import assert_raises
from numpy.testing import assert_warns

from nose.tools import assert_true

from protoclass.data_management import GTModality


def test_path_list_no_dir():
    """ Test either if an error is raised when the directory does not
    exist. """
    # Create a dummy named directory
    path_data = 'None'
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']
    # Create an object to handle the data
    gt_mod = GTModality()

    # We can pass a list of unknown path
    path_data_list = [path_data, path_data]
    assert_raises(ValueError, gt_mod.read_data_from_path,
                  label, path_data_list)


def test_path_list_wrong_type():
    """ Test either an error is raised if the type in the list is
    not string. """
    # Create a dummy named directory
    path_data = 'None'
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']
    # Create an object to handle the data
    gt_mod = GTModality()

    # We can a list we incorrect type
    path_data_list = [1, path_data, path_data]
    assert_raises(ValueError, gt_mod.read_data_from_path,
                  label, path_data_list)


def test_path_no_dir():
    """ Test either if an error is raised when no path is given at
    any point. """
    # Create an object to handle the data
    gt_mod = GTModality()
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']

    # Check that an error is risen
    assert_raises(ValueError, gt_mod.read_data_from_path, label)


def test_path_wrong_type():
    """ Test either if an error is raised when the type of the path is not a
    string. """
    # Create a dummy type
    path_data = 1
    # Create an object to handle the data
    gt_mod = GTModality()
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']
    # Check that an error is risen
    assert_raises(ValueError, gt_mod.read_data_from_path, label, path_data)


def test_path_wrong_dir():
    """ Test if an error is raised when the directory does not exist. """

    # Create a dummy named directory
    path_data = 'None'
    # Create an object to handle the data
    gt_mod = GTModality()
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']
    # Check that an error is risen
    assert_raises(ValueError, gt_mod.read_data_from_path,
                  label, path_data)


def test_read_gt_dicom_path_list_larger_1():
    """ Test if an error is raised when the path is a list and an item contain
    more than one serie. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = [os.path.join(currdir, 'data', 't2w'),
                 os.path.join(currdir, 'data', 'dce')]
    # Create an object to handle the data
    gt_mod = GTModality()
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'pca']
    # Check the assert
    assert_raises(ValueError, gt_mod.read_data_from_path,
                  label, path_data)


def test_read_gt_data_path_list():
    """ Test if we can read gt series. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Check that the data have been read
    assert_true(not gt_mod.is_read())

    gt_mod.read_data_from_path(label, path_data=path_data_list)

    # Check that the data have been read
    assert_true(gt_mod.is_read())

    # Check the data here
    data = np.load(os.path.join(currdir, 'data', 'gt_path_list.npy'))
    assert_array_equal(gt_mod.data_, data)
    assert_equal(gt_mod.n_serie_, 4)


def test_read_gt_data_path_list_constructor():
    """ Test if we can read gt series. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality(path_data_list)

    # Check that the data have been read
    assert_true(not gt_mod.is_read())

    gt_mod.read_data_from_path(label)

    # Check that the data have been read
    assert_true(gt_mod.is_read())

    # Check the data here
    data = np.load(os.path.join(currdir, 'data', 'gt_path_list.npy'))
    assert_array_equal(gt_mod.data_, data)
    assert_equal(gt_mod.n_serie_, 4)


def test_read_gt_data():
    """ Test either if an error is raised when the length of the label list
    is different from the number of GT read. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg']
    # Create an object to handle the data
    gt_mod = GTModality()

    assert_raises(ValueError, gt_mod.read_data_from_path,
                  label, path_data_list)


def test_read_gt_path():
    """ Test if we can read data from the same folder organized with
    different serie ID. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'dce')

    # Give the list for the ground_truth
    label = ['prostate', 'pz']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    gt_mod.read_data_from_path(label, path_data=path_data)

    # Check the data here
    data = np.load(os.path.join(currdir, 'data', 'gt_path.npy'))
    assert_array_equal(gt_mod.data_, data)
    assert_equal(gt_mod.n_serie_, 2)


def test_dce_path_data_warning():
    """ Test either if a warning is raised if the path will be overriden. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality(path_data_list)

    # Check that a warning is raised when reading the data with a data path
    # after specifying one previously.
    assert_warns(UserWarning, gt_mod.read_data_from_path,
                 label, path_data_list)


def test_extract_not_read():
    """Test either if an error is raised when the data have not been read and
    an attempt to extract the gt is performed."""

    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    label = 'prostate'
    assert_raises(ValueError, gt_mod.extract_gt_data, label)


def test_extract_no_label_known():
    """Test either if an error is raised when no corresponding gt category
    is found."""

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    gt_mod.read_data_from_path(label, path_data=path_data_list)

    # Try to extract a wrong label
    label_extr = 'rnd'
    assert_raises(ValueError, gt_mod.extract_gt_data, label_extr)


def test_extract_wrong_output_type():
    """ Test either if an error is raised if the type of output is unknown. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    gt_mod.read_data_from_path(label, path_data=path_data_list)

    # Extract the prostate indexes
    label_extr = 'prostate'
    assert_raises(ValueError, gt_mod.extract_gt_data, label_extr, 'rnd')


def test_extract_index():
    """ Test if the indexes of a GT will be well extracted. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    gt_mod.read_data_from_path(label, path_data=path_data_list)

    # Extract the prostate indexes
    label_extr = 'prostate'
    idx_prostate = gt_mod.extract_gt_data(label_extr, 'index')
    data = np.load(os.path.join(currdir, 'data', 'extract_gt_index.npy'))
    # Check each table
    for idx_arr, test_arr in zip(idx_prostate, data):
        assert_array_equal(idx_arr, test_arr)


def test_extract_data():
    """ Test if the data of a GT will be well extracted. """

    # Load the data with only a single serie
    currdir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(currdir, 'data', 'gt_folders')
    path_data_list = [os.path.join(path_data, 'prostate'),
                      os.path.join(path_data, 'cg'),
                      os.path.join(path_data, 'pz'),
                      os.path.join(path_data, 'cap')]
    # Give the list for the ground_truth
    label = ['prostate', 'cg', 'pz', 'cap']
    # Create an object to handle the data
    gt_mod = GTModality()

    # Read the data
    gt_mod.read_data_from_path(label, path_data=path_data_list)

    # Extract the prostate indexes
    label_extr = 'prostate'
    data_prostate = gt_mod.extract_gt_data(label_extr, 'data')
    data = np.load(os.path.join(currdir, 'data', 'extract_gt_data.npy'))
    # Check each table
    assert_array_equal(data_prostate, data)
