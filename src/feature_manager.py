import warnings

from src.constants.paths_generator import CachePaths

# warnings.simplefilter(action='ignore', category=FutureWarning)
# import logging
# logging.basicConfig(level=logging.ERROR)

import tsfresh
import pandas
import numpy as np

import src.data_manager as dm
from src.constants.literals import *
import src.utility.chronometer as Chronom
from src.utility import utils


class FeaturesManager:

    version = "1.0"

    TSERIES_NAMES = [
        MOVEMENT_POINTS,
        TOUCH_DOWN_POINTS,
        TOUCH_UP_POINTS]

    _instance = None

    @staticmethod
    def get_instance(dataset_name, renew_cache=False):
        if FeaturesManager._instance:
            return FeaturesManager._instance

        c = Chronom.Chrono("Loading features...")

        if FeaturesManager.cache_present(dataset_name) and not renew_cache:
            p = utils.load_pickle(CachePaths.features(dataset_name, FeaturesManager.version))
            c.millis("from pickle")
            return p

        _instance = FeaturesManager(dataset_name)
        utils.save_pickle(_instance, CachePaths.features(dataset_name, FeaturesManager.version))
        c.millis("generated")
        return _instance

    @staticmethod
    def cache_present(dataset_name):
        return os.path.isfile(CachePaths.features(dataset_name, FeaturesManager.version))

    def __init__(self, dataset_name):
        self.data = dm.DataManager(dataset_name)
        self.labels = np.asarray((range(len(self.data.items))))

        self.features = {x: None for x in FeaturesManager.TSERIES_NAMES}

        self.extract_features()

    @staticmethod
    def _extract_features(tseries: pandas.DataFrame, labels):
        return tsfresh.extract_relevant_features(tseries, labels,
                                                 column_id=ITEM_ID, column_sort=TIME, n_jobs=4)

    def extract_features(self):
        local_features = {MOVEMENT_POINTS: self.data.tseries_movement_points,
                          TOUCH_UP_POINTS: self.data.tseries_touch_up_points,
                          TOUCH_DOWN_POINTS: self.data.tseries_touch_down_points}

        for tseries_name in FeaturesManager.TSERIES_NAMES:
            chrono = Chronom.Chrono("Extracting features from {}...".format(tseries_name))
            self.features[tseries_name] = self._extract_features(local_features[tseries_name],
                                                                 self.get_classes())
            chrono.millis()

    def get_features(self):
        return self.features

    def get_classes(self):
        return self.labels


if __name__ == '__main__':
    FeaturesManager.get_instance(DATASET_NAME_0, renew_cache=True)
