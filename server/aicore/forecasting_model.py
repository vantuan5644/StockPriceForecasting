import abc


class Forecaster(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def forecast(self, horizon: int):
        """Multi-step forecasting with a given horizon"""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        """Update model"""
        raise NotImplementedError
