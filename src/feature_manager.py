import sklearn
import warnings
from collections import Counter

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVC
from tsfresh.transformers import RelevantFeatureAugmenter

from src.constants.paths_generator import CachePaths, ResultsPaths
from src.plotter.plotter import Plotter as p

# warnings.simplefilter(action='ignore', category=FutureWarning)
import logging

from src.evaluation.classification import cmc_curve

logging.basicConfig(level=logging.ERROR)

import tsfresh
import pandas as pd
import numpy as np

import src.data_manager as dm
from src.constants.literals import *
import src.utility.chronometer as Chronom
from src.utility import utils


# pd.options.display.max_rows = 10000#

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

        # self.extract_features()

    @staticmethod
    def _extract_features(tseries: pd.DataFrame, labels):
        return tsfresh.extract_relevant_features(tseries, labels,
                                                 column_id=OBSERVATION_ID,
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
        return pd.Series(self.data.items)

    @staticmethod
    def tseries_train_test_split(tseries, items, observation_ids, test_size=0.35):
        obs_train, obs_test, y_train, y_test = train_test_split(observation_ids,
                                                                items,
                                                                stratify=items,
                                                                test_size=test_size)

        tseries_train = tseries.loc[tseries[OBSERVATION_ID].isin(obs_train)]
        tseries_test = tseries.loc[tseries[OBSERVATION_ID].isin(obs_test)]

        x_train = pd.DataFrame(index=y_train.index)
        x_test = pd.DataFrame(index=y_test.index)

        return x_train, x_test, tseries_train, tseries_test, y_train, y_test


if __name__ == '__main__':
    f = FeaturesManager.get_instance(DATASET_NAME_0, renew_cache=False)
    d = f.data.tseries_movement_points

    x_train, x_test, tseries_train, tseries_test, y_train, y_test = f.tseries_train_test_split(d,
                                                                                               f.get_classes(),
                                                                                               f.data.observation_ids)
    # print(x_train.shape)
    # print(x_test.shape)
    # print(tseries_train.shape)
    # print(tseries_test.shape)
    # print(y_train.shape)
    # print(y_test.shape)
    # print(tseries_test.head())

    classifier = SVC(C=7500, gamma=1e-07, probability=True)
    pipeline = make_pipeline(RelevantFeatureAugmenter(column_id=OBSERVATION_ID,
                                                      column_sort=TIME,
                                                      n_jobs=12,
                                                      ml_task='classification'),
                             RobustScaler(),
                             classifier)


    print(">>>Fitting")
    print("Tseries train", tseries_train.shape)
    print("xtrain train", x_train.shape)
    print("ytrain train", y_train.shape)
    pipeline.set_params(relevantfeatureaugmenter__timeseries_container=tseries_train)
    pipeline.fit(x_train, y_train)

    print(">>> Predicting")
    print("Tseries test", tseries_test.shape)
    print("xtest test", x_test.shape)
    pipeline.set_params(relevantfeatureaugmenter__timeseries_container=tseries_test)
    y_pred = pipeline.predict(x_test)


    print(">>>Probas")
    print("y_pred", len(y_pred))
    print("y_test", len(y_test))
    y_proba = pipeline.predict_proba(x_test)

    print(sklearn.metrics.classification_report(y_test, y_pred))

    ranks, cms_values = cmc_curve(y_test, y_proba, pipeline.classes_)
    p.cmc(ResultsPaths.cmc(DATASET_NAME_0, "new_ersion"), ranks, cms_values)

    for p, y in zip(y_proba, y_test):
        predictions = list(zip(p, classifier.classes_))
        print("{}:\t{}".format(y, [x for _, x in sorted(predictions, key=lambda x: x[0], reverse=True)]))

# features = f.features[MOVEMENT_POINTS]
    # print(f.data.tseries_movement_points.head())
    # print(len(set(f.data.tseries_movement_points[ITEM_ID])))
    #
    # print("Data: ", f.data.tseries_movement_points.shape)
    # print("Features: ", features.shape)
    # print("Labels: ", f.get_classes().shape)
    #
    # for x in f.data.files_name:
    #     print(x)
    #     import sklearn.model_selection
    #
    #     xtrain, xtest, y_train, y_test = sklearn.model_selection.train_test_split(
    #         features, f.get_classes(),
    #         stratify=f.get_classes(),
    #         random_state=42,
    #         test_size=0.35)
    #     print(len(f.get_classes()))
    #     TUNED_PARAMETERS = [{'kernel': ['rbf'], 'gamma':
    #         ['auto', 0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
    #                          'C': [0.001, 0.1, 1, 10, 100, 500, 1000, 2500, 5000, 7500, 10000]}]
    #     CV = 3
    #
    #     # v = GridSearchCV(SVC(), TUNED_PARAMETERS, cv=CV, refit=True, n_jobs=-1)
    #     v = SVC(C=7500, gamma=1e-07, probability=True)
    #     predictor = make_pipeline(sklearn.preprocessing.RobustScaler(), v)
    #     print("Fitting")
    #     predictor.fit(xtrain, y_train)
    #
    #     print("Predictions")
    #     predictions = predictor.predict(xtest)
    #     probas = predictor.predict_proba(xtest)
    #
    #     print(sklearn.metrics.classification_report(y_test, predictions))
    #     print(len(v.classes_))
    #     print(Counter(f.get_classes()))
    #
    #     print(cmc_curve(y_test, probas, predictor.classes_))
    #     a,b =cmc_curve(y_test, probas, predictor.classes_)
    #     for x in zip(a,b):
    #         print(x)
    #     print("start")
    #     print(a)
    #     print(b)
    #     print("end")
    #     print(len(a))
    #     print(len(b))
    #
    #     from src.plotter.plotter import Plotter as p
    #     p.cmc(ResultsPaths.cmc(DATASET_NAME_0, "old_version"), a, b)
    # #    print(v.best_estimator_)
