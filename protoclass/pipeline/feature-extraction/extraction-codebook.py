#title           :detection_lbp.py
#description     :This will create a header for a python script.
#author          :Guillaume Lemaitre
#date            :2015/06/07
#version         :0.1
#notes           :
#python_version  :2.7.6  
#==============================================================================

# Import the needed libraries
# Numpy library
import numpy as np
# Panda library
import pandas as pd
# OS library
import os
from os.path import join
# SYS library
import sys

# Read the csv file with the ground truth
gt_csv_filename = '/DATA/OCT/data_organized/data.csv'
#gt_csv_filename = '/work/le2i/gu5306le/OCT/data.csv'
gt_csv = pd.read_csv(gt_csv_filename)

gt = gt_csv.values

data_filename = gt[:, 0]

# Get the good extension
radius = 1
data_filename = np.array([f + '_nlm_lbp_' + str(radius) + '.npz' for f in data_filename])

label = gt[:, 1]
label = ((label + 1.) / 2.).astype(int)

from collections import Counter

count_gt = Counter(label)

if (count_gt[0] != count_gt[1]):
    raise ValueError('Not balanced data.')
else:
    # Split data into positive and negative
    # TODO TACKLE USING PERMUTATION OF ELEMENTS
    filename_normal = data_filename[label == 0]
    filename_dme = data_filename[label == 1]

    data_folder = '/work/le2i/gu5306le/OCT/lbp_r_' + str(radius) + '_data_npz'

    for idx_test, (pat_test_norm, pat_test_dme) in enumerate(zip(filename_normal, filename_dme)):

        pat_train_norm = np.delete(filename_normal, idx_test)
        pat_train_dme = np.delete(filename_dme, idx_test)

        # Load the training data
        # Define the name of the volume
        vol_name = 'vol_lbp'
        training_data = np.concatenate(np.concatenate([np.load(f)[vol_name] for f in pat_train_norm], axis=0),
                                       np.concatenate([np.load(f)[vol_name] for f in pat_train_norm], axis=0),
                                       axis=0)
        

        
