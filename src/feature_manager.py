import warnings

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

from src.constants.paths_generator import CachePaths

# warnings.simplefilter(action='ignore', category=FutureWarning)
import logging
logging.basicConfig(level=logging.ERROR)

import tsfresh
import pandas
import numpy as np

import src.data_manager as dm
from src.constants.literals import *
import src.utility.chronometer as Chronom
from src.utility import utils


class FeaturesManager:

    version = "1.1"

    TSERIES_NAMES = [
        MOVEMENT_POINTS,
        TOUCH_DOWN_POINTS,
        TOUCH_UP_POINTS]

    # FDR_LEVEL = 0.15

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
        # self.labels = np.asarray((range(len(self.data.items))))

        self.features = {x: None for x in FeaturesManager.TSERIES_NAMES}

        self.extract_features()

    @staticmethod
    def _extract_features(tseries: pandas.DataFrame, labels):
        return tsfresh.extract_relevant_features(tseries, labels,
                                                 column_id=ITEM_ID,
                                                 column_sort=TIME,
                                                 n_jobs=12,
                                                 ml_task='classification')

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
        return np.asarray(self.data.items)


if __name__ == '__main__':
    f = FeaturesManager.get_instance(DATASET_NAME_0, renew_cache=False)
    features = f.features[MOVEMENT_POINTS]

    # print(f.data.tseries_movement_points.head())
    # print(len(set(f.data.tseries_movement_points[ITEM_ID])))
    #
    # print("Data: ", f.data.tseries_movement_points.shape)
    # print("Features: ", features.shape)
    # print("Labels: ", f.get_classes().shape)
    #
    # for x in f.data.files_name:
    #     print(x)
    import sklearn.model_selection
    xtrain, xtest, y_train, y_test = sklearn.model_selection.train_test_split(features, f.get_classes(),
                                                                                  random_state=42,
                                                                                  test_size=0.42)

    print(f.get_classes())
    print(len(f.get_classes()))
    TUNED_PARAMETERS = [{'kernel': ['rbf'], 'gamma': ['auto', 0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6],
                     'C': [0.001, 0.1, 1, 10, 100, 500, 1000, 5000, 10000]}]
    CV = 5

    predictor = make_pipeline(sklearn.preprocessing.RobustScaler(),
                              GridSearchCV(SVC(), TUNED_PARAMETERS, cv=CV, n_jobs=-1))
    print("Fitting")
    predictor.fit(xtrain, y_train)

    print("Predictions")
    predictions = predictor.predict(xtest)

    print(sklearn.metrics.classification_report(y_test, predictions))

