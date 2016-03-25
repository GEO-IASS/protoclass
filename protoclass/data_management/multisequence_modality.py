""" Basic class for multisequence modality (DW).
"""

import numpy as np
import SimpleITK as sitk
import os

from abc import ABCMeta, abstractmethod

from .base_modality import BaseModality


class MultisequenceModality(BaseModality):
    """ Basic class for multisequence medical modality (DW).

    Warning: This class should not be used directly. Use the derive classes
    instead.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """ Constructor. """
        raise NotImplementedError

    @abstractmethod
    def _update_histogram(self):
        """ Method to compute histogram and statistics. """
        raise NotImplementedError

    @abstractmethod
    def read_data_from_path(self, path_data):
        """ Method allowing to read the data. """
        raise NotImplementedError
