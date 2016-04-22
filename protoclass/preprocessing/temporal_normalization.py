"""Basic class to normalize temporal modality."""

from abc import ABCMeta, abstractmethod

from .base_normalization import BaseNormalization
from ..data_management import TemporalModality
from ..utils.validation import check_modality

class TemporalNormalization(BaseNormalization):
    """Basic class to normalize temporal modality.

    Warning: This class should not be used directly. Use the derive classes
    instead.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, base_modality):
        super(TemporalNormalization, self).__init__()
        self.base_modality = base_modality
        self._validate_modality()

    def _validate_modality(self):
        """Check if the provided modality is of interest with the type of
        normalization."""

        # Check that the base modality is a subclass of TemporalModality
        if not issubclass(type(self.base_modality), TemporalModality):
            raise ValueError('The base modality provided in the constructor is'
                             ' not a TemporalModality.')
        else:
            self.base_modality_ = self.base_modality

    def _validate_modality_gt(self, modality, ground_truth, cat):
        """Check the consistency of the modality with the ground-truth."""
        raise NotImplementedError

    @abstractmethod
    def fit(self, modality):
        """Find the parameters needed to apply the normalization.

        Parameters
        ----------
        modality : object
            Object inherated from TemporalModality.

        Returns
        -------
        self : object
             Return self.

        """
        # Check that the class of modality is the same than the template
        # modality
        check_modality(modality, self.base_modality_)

        return self

    @abstractmethod
    def normalize(self, modality):
        """ Method to normalize the given modality using the fitted parameters.

        Parameters
        ----------
        modality: object of type StandaloneModality
            The modality object from which the data need to be normalized.

        Returns
        -------
        modality: object of type StandaloneModality
            The modality object in which the data will be normalized.
        """
        # Check that the class of modality is the same than the template
        # modality
        check_modality(modality, self.base_modality_)

        return self

    @abstractmethod
    def denormalize(self, modality):
        """ Method to denormalize the given modality using the
        fitted parameters.

        Parameters
        ----------
        modality: object of type StandaloneModality
            The modality object from which the data need to be normalized.

        Returns
        -------
        modality: object of type StandaloneModality
            The modality object in which the data will be normalized.
        """
        # Check that the class of modality is the same than the template
        # modality
        check_modality(modality, self.base_modality_)

        return self
