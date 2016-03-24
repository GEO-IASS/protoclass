""" Basic class for normalization.
"""

from abc import ABCMeta, abstractmethod


class BaseNormalization(object):
    """ Basic class for normalization.

    Warning: This class should not be used directly. Use the derive classes
    instead.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """ Constructor """
        pass

    @abstractmethod
    def _validate_modality(self):
        """ Check if the provided modality is of interest with the type of
        normalization. """
        raise NotImplementedError

    @abstractmethod
    def fit(self):
        """ Method to find the parameters needed to apply the
        normalization. """
        raise NotImplementedError

    @abstractmethod
    def normalize(self):
        """ Normalize the data after fitting the data. """
        raise NotImplementedError

    @abstractmethod
    def denormalize(self):
        """ Reverse the normalization. """
        raise NotImplementedError
