from abc import ABC, abstractmethod

from torch.utils.data import Dataset


class ActiveDatasetWrapper(ABC, Dataset):
    """ A dataset wrapper for active learning. 

    This class is a wrapper for a dataset that can be used for active learning.
    It provides a method for creating batches of data.

    Attributes:
        dataset (Dataset): The dataset to wrap.
    """
    def __init__(self, dataset: Dataset):
        """ Constructor.

        Args:
            dataset (Dataset): The dataset to wrap.
        """
        self.dataset = dataset

    def create_batches(self, batch_size: int):
        """ Create batches of data.

        Args:
            batch_size (int): The batch size.

        Returns:
            list: The list of batches.
        """
        n_samples = len(self)
        indices = list(range(n_samples))
        indices = [indices[i:i + batch_size]
                   for i in range(0, n_samples, batch_size)]
        return [self._create_batch(idx) for idx in indices]

    @abstractmethod
    def _create_batch(self, indices: list):
        """ Create a batch of data.

        Args:
            indices (list): The indices of the batch.

        Returns:
            dict: The batch data.
        """
        pass
