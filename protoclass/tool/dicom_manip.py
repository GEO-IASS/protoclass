#title           :dicom_manip.py
#description     :This will create a header for a python script.
#author          :Guillaume Lemaitre
#date            :2015/04/20
#version         :0.1
#notes           :
#python_version  :2.7.6  
#==============================================================================

# Import the needed libraries
# Numpy library
import numpy as np
# SimpleITK library
import SimpleITK as sitk
# Joblib library
### Module to performed parallel processing
from joblib import Parallel, delayed
### Module to performed parallel processing
import multiprocessing
# OS library
import os
from os.path import join, isdir, isfile
# Import namedtuple
from collections import namedtuple

def OpenRawImageOCT(filename, size, dtype='uint8', reverse=True):
    """Function to read a raw image. The size as to be known

    Parameters
    ----------
    filename: str
        Filename of the raw image.

    size: tuple of ints (X, Y, Z)
        Tuple with 2 or 3 values depending of the dimensionality of the data.
    
    dtype: default - uint8
        Type of the raw data.

    reverse: bool
        We have maybe to return the data for more convenience.
    
    Returns
    -------
    im_numpy: ndarray
        A 2D or 3D numpy array in the order ()
    """

    from skimage import img_as_float

    size_OCT = (size[1], size[2], size[0])
    # Data are stored as (Y, Z, X)
    im_numpy = np.fromfile(filename, dtype=dtype, sep="").reshape(size_OCT)

    # We need to roll the x axis to obtain (X, Y, Z)
    im_numpy = np.rollaxis(im_numpy, 2, 0)

    # Return the data if needed
    im_numpy_cp = im_numpy.copy()
    if reverse == True:
        for sl in range(im_numpy.shape[2]):
            im_numpy[:,:,-sl] = im_numpy_cp[:,:,sl]
    
    return img_as_float(im_numpy)

def OpenOneSerieDCM(path_to_serie, reverse=False):
    """Function to read a single serie DCM to return a 3D volume

    Parameters
    ----------
    path_to_serie: str
        The path to the folder containing all the dicom images.
    reverse: bool
        Since that there is a mistake in the data we need to flip in z the gt.
        Have to be corrected in the future.
    
    Returns
    -------
    im_numpy: ndarray
        A 3D array containing the volume extracted from the DCM serie.
    """
    
    # Define the object in order to read the DCM serie
    reader = sitk.ImageSeriesReader()

    # Get the DCM filenames of the serie
    dicom_names = reader.GetGDCMSeriesFileNames(path_to_serie)

    # Set the filenames to read
    reader.SetFileNames(dicom_names)

    # Build the volume from the set of 2D images
    im = reader.Execute()

    # Convert the image into a numpy matrix
    im_numpy = sitk.GetArrayFromImage(im)

    # The Matlab convention is (Y, X, Z)
    # The Numpy convention is (Z, Y, X)
    # We have to swap these axis
    ### Swap Z and X
    im_numpy = np.swapaxes(im_numpy, 0, 2)
    im_numpy = np.swapaxes(im_numpy, 0, 1)
    
    im_numpy_cp = im_numpy.copy()
    if reverse == True:
        #print 'Inversing the GT'
        for sl in range(im_numpy.shape[2]):
            im_numpy[:,:,-sl] = im_numpy_cp[:,:,sl]

    
    return im_numpy.astype(float)

def OpenVolumeNumpy(filename, reverse_volume=False, **kwargs):
    """Function to read a numpy array previously saved

    Parameters
    ----------
    filename: str
        Filename of the numpy array *.npy.
    reverse_volume: bool
        Since that there is a mistake in the data we need to flip in z the gt.
        Have to be corrected in the future.
    
    Returns
    -------
    im_numpy: ndarray
        A 3D array containing the volume.
    """
    if filename.endswith('.npy'):

        # Open the volume
        im_numpy = np.load(filename)

        # Copy the volume temporary
        im_numpy_cp = im_numpy.copy()
        if reverse_volume == True:
            #print 'Inversing the GT'
            for sl in range(im_numpy.shape[2]):
                im_numpy[:,:,-sl] = im_numpy_cp[:,:,sl]

        return im_numpy
                
    elif filename.endswith('.npz'):

        # Get the keyword of the name of the variable to extract
        name_var_extract = kwargs.pop('name_var_extract', None)

        # Get the volume from file
        npzfile = np.load(filename)
        im_numpy = npzfile[name_var_extract]

        # Copy the volume temporary
        im_numpy_cp = im_numpy.copy()
        if reverse_volume == True:
            #print 'Inversing the GT'
            for sl in range(im_numpy.shape[2]):
                im_numpy[:,:,-sl] = im_numpy_cp[:,:,sl]

        return im_numpy


def OpenSerieUsingGTDCM(path_to_data, path_to_gt, reverse_gt=True, reverse_data=False):
    """Function to read a DCM volume and apply a GT mask

    Parameters
    ----------
    path_to_data: str
        Path containing the modality data.
    path_to_gt: str
        Path containing the gt.
    reverse_gt: bool
        Since that there is a mistake in the data we need to flip in z the gt.
        Have to be corrected in the future.
    
    Returns
    -------
    volume_data: ndarray
        A 3D array containing the volume extracted from the DCM serie.
        The data not corresponding to the GT of interest will be tagged NaN.
    """

    # Open the data volume
    volume_data = OpenOneSerieDCM(path_to_data, reverse_data)

    # Open the gt volume
    tmp_volume_gt = OpenOneSerieDCM(path_to_gt)
    volume_gt = tmp_volume_gt.copy()
    if reverse_gt == True:
        #print 'Inversing the GT'
        for sl in range(volume_gt.shape[2]):
            volume_gt[:,:,-sl] = tmp_volume_gt[:,:,sl]

    # Affect all the value which are 0 in the gt to NaN
    volume_data[(volume_gt == 0).nonzero()] = np.NaN

    # Return the volume read
    return volume_data

def OpenDataLabel(path_to_data):
    """Function to read data and label form an *.npz file

    Parameters
    ----------
    path_to_serie: str
        The path to the *.npz file.
    
    Returns
    -------
    data: ndarray
        A list of 2D matrix containing the data.
    label: ndarray
        A list of 1D vector containing the label associated to the data matrix.
    """
    
    if not (isfile(path_to_data) and path_to_data.endswith('.npz')):
        # Check that the path is in fact a file and npz format
        raise ValueError('protoclass.tool.OpenDataLabel: An *.npz file is expected.')
    else:
        # The file can be considered
        npzfile = np.load(path_to_data)

        # return the desired variable
        return (npzfile['data'], npzfile['label'])

def GetGTSamples(path_to_gt, reverse_gt=True, pos_value=255.):
    """Function to return the samples corresponding to the ground-truth

    Parameters
    ----------
    path_to_gt: str
        Path containing the gt.
    reverse_gt: bool
        Since that there is a mistake in the data we need to flip in z the gt.
        Have to be corrected in the future.
    reverse_gt: numeric or bool
        Value considered as the positive class. By default it is 255., but it could be
        1 or True
    
    Returns
    -------
    idx_gt: ndarray
        A 3D array containing the volume extracted from the DCM serie.
        The data not corresponding to the GT of interest will be tagged NaN.
    """

    # Open the gt volume
    tmp_volume_gt = OpenOneSerieDCM(path_to_gt)
    volume_gt = tmp_volume_gt.copy()
    if reverse_gt == True:
        #print 'Inversing the GT'
        for sl in range(volume_gt.shape[2]):
            volume_gt[:,:,-sl] = tmp_volume_gt[:,:,sl]

    # Get the samples that we are interested with
    return np.nonzero(volume_gt == pos_value)

def VolumeToLabelUsingGT(volume, path_to_gt, reverse_gt=True):

    return BinariseLabel(volume[GetGTSamples(path_to_gt, reverse_gt)])

def OpenResult(path_to_result):
    """Function to read results: label and roc information

    Parameters
    ----------
    path_to_result: str
        Path containing the filename of the result file.
    
    Returns
    -------
    pred_label: 1D array
        The label results for the patient considered as test.
    roc: namedtuple
        A named tuple such as roc_auc = namedtuple('roc_auc', ['fpr', 'tpr', 'thresh', 'auc'])
    """
    
    # The results are saved into a npz file
    if not (isfile(path_to_result) and path_to_result.endswith('.npz')):
        raise ValueError('protoclass.tool.dicom_manip: The result file is not an *.npz file')
    else:
        # Load the file
        npzfile = np.load(path_to_result)

        # Define our namedtuple
        roc_auc = namedtuple('roc_auc', ['fpr', 'tpr', 'thresh', 'auc'])
        roc = roc_auc._make(npzfile['roc'])
        pred_label = npzfile['pred_label']

        return (pred_label, roc)

def __VolumeMinMax__(path_patient):
    """Private function in order to return min max of a 3D volume

    Parameters
    ----------
    path_patient: str
        Path where the data are localised.
    
    Returns
    -------
    (min_int, max_int): tuple
        Return a tuple containing the minimum and maximum for the patient.
    """

    # Check if we have either a file or a directory
    if isdir(path_patient):
        # Read a volume for the current patient
        volume = OpenOneSerieDCM(path_patient)
    elif isfile(path_patient):
        volume = OpenVolumeNumpy(path_patient)

    # Return a tuple with the min and max
    return(np.min(volume), np.max(volume))

def FindExtremumDataSet(path_to_data, **kwargs):
    """Function to find the minimum and maximum intensities
       in a 3D volume

    Parameters
    ----------
    path_to_data: str
        Path containing the modality data.
    modality: str
        String containing the name of the modality to treat.
    
    Returns
    -------
    (min_int, max_int): tuple
        A tuple containing the minimum and the maximum intensities.
    """
    
    # Define the path to the modality
    path_modality = kwargs.pop('modality', 'T2W')

    # Create a list with the path name
    path_patients = []
    for dirs in os.listdir(path_to_data):
        # Create the path variable
        path_patient = join(path_to_data, dirs)
        path_patients.append(join(path_patient, path_modality))
       
    # Compute the Haralick statistic in parallel
    num_cores = multiprocessing.cpu_count()
    # Check if we have original DICOM or Numpy volume
    min_max_list = Parallel(n_jobs=num_cores)(delayed(__VolumeMinMax__)(path) for path in path_patients)
    # Convert the list into numpy array
    min_max_array = np.array(min_max_list)

    return (np.min(min_max_array), np.max(min_max_array))

def BinariseLabel(label):
    """Function to find the minimum and maximum intensities
       in a 3D volume

    Parameters
    ----------
    label: array
        Array with values usually 0. and 255. .

    Returns
    -------
    label: array
        Array with values either -1. or 1. .
    """

    label[np.nonzero(label>0)] = 1.
    label = label * 2. - 1.

    return label

def __VolumePercentilesFromPath__(path_patient, path_gt, n_landmarks=5, min_perc=2., max_perc=98.):
    """Private function in order to find the different percentiles of a dataset

    Parameters
    ----------
    path_patient: str
        Path where the data are localised.

    path_gt: str
        Path where the data are localised.
    
    n_landmarks: int (default=5)
        Number of landmarks which have to be extracted

    min_perc: float (default=2.)
        The minimum percentile of interest

    max_perc: float (default=98.)
        The maximum percentile of interest
    
    Returns
    -------
    intensities_arr: array
        Return an array with the intensities corresponding to the percentiles of interest.
    """

    # Check if we have either a file or a directory
    if isdir(path_patient):
        # Read a volume for the current patient
        volume = OpenOneSerieDCM(path_patient)
        volume_emd_gt = OpenSerieUsingGTDCM(path_patient, path_gt)
    elif isfile(path_patient):
        volume = OpenVolumeNumpy(path_patient)

    prostate_data = volume_emd_gt[np.nonzero(~np.isnan(volume_emd_gt))]

    intensities_arr = []
    # Find iteratively the different percentiles of the volume of interest
    ### Create the array of percentiles to find
    perc_arr = np.linspace(min_perc, max_perc, num=n_landmarks, endpoint=True)
    for perc in perc_arr:
        intensities_arr.append(np.percentile(prostate_data, perc))

    # Return a tuple with the min and max
    return np.array(intensities_arr)

def __VolumePercentilesFromData__(volume, n_landmarks=5, min_perc=2., max_perc=98.):
    """Private function in order to find the different percentiles of a dataset

    Parameters
    ----------
    volume: array
        Array with the data.
    
    n_landmarks: int (default=5)
        Number of landmarks which have to be extracted

    min_perc: float (default=2.)
        The minimum percentile of interest

    max_perc: float (default=98.)
        The maximum percentile of interest
    
    Returns
    -------
    intensities_arr: array
        Return an array with the intensities corresponding to the percentiles of interest.
    """

    intensities_arr = []
    # Find iteratively the different percentiles of the volume of interest
    ### Create the array of percentiles to find
    perc_arr = np.linspace(min_perc, max_perc, num=n_landmarks, endpoint=True)
    for perc in perc_arr:
        intensities_arr.append(np.percentile(volume, perc))

    # Return a tuple with the min and max
    return np.array(intensities_arr)

def FindLandmarksDataset(path_to_data, path_modality, path_gt, n_landmarks=5, min_perc=2., max_perc=98.):
    """Function to find the minimum and maximum intensities
       in a 3D volume

    Parameters
    ----------
    path_to_data: str
        Path containing the modality data.
    modality: str
        String containing the name of the modality to treat.
    
    Returns
    -------
    (min_int, max_int): tuple
        A tuple containing the minimum and the maximum intensities.
    """

    # Create a list with the path name
    path_patients = []
    path_patients_gt = []
    for dirs in os.listdir(path_to_data):
        # Create the path variable
        path_patient = join(path_to_data, dirs)
        path_patients.append(join(path_patient, path_modality))
        path_patients_gt.append(join(path_patient, path_gt))
       
    # Compute the Haralick statistic in parallel
    num_cores = multiprocessing.cpu_count()
    # Check if we have original DICOM or Numpy volume
    intensities_list = Parallel(n_jobs=num_cores)(delayed(__VolumePercentilesFromPath__)(path, path2, n_landmarks, min_perc, max_perc) 
                                                  for (path, path2) in zip(path_patients, path_patients_gt))
    # Convert the list into numpy array
    intensities_list = np.array(intensities_list)

    # We have to return the mean landmarks
    return (np.mean(intensities_list, axis=0))
