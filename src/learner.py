import sklearn
import warnings
from collections import Counter

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVC
from tsfresh.transformers import RelevantFeatureAugmenter

from src.constants.paths_generator import CachePaths, ResultsPaths
from src.plotter.performances import ClassificationPerformances

# warnings.simplefilter(action='ignore', category=FutureWarning)
import logging

from src.evaluation.classification import cmc_curve

logging.basicConfig(level=logging.ERROR)

import tsfresh
import pandas as pd
import numpy as np

import src.data_manager as dm
from src.constants.literals import *
from src.utility.chronometer import Chrono
from src.utility import utils


# pd.options.display.max_rows = 10000#

class Learner:
    version = "1.1"

    # FDR_LEVEL = 0.15

    # If AUGMENTER changes, even the name of the optional parameter
    # in set params must change
    AUGMENTER = "augmenter"
    SCALER = "scaler"
    CLASSIFIER = "classifier"

    _instance = None

    @staticmethod
    def get_instance(dataset_name, renew_cache=False):
        if Learner._instance:
            return Learner._instance

        c = Chrono("Creating learner...")

        if (os.path.isfile(CachePaths.learner(dataset_name, Learner.version))
                and not renew_cache):
            p = utils.load_pickle(CachePaths.learner(dataset_name, Learner.version))
            c.millis("loaed pre-trained learner from pickle")
            return p

        _instance = Learner(dataset_name)
        utils.save_pickle(_instance, CachePaths.learner(dataset_name, Learner.version), override=True)
        c.millis("Saving into: {}".format(CachePaths.learner(dataset_name, Learner.version)))
        return _instance

    def __init__(self, dataset_name):
        self.data = dm.DataManager(dataset_name)
        self.pipeline = None

        self.fit_predict()

    def get_timeseries(self):
        return self.data.observation_ids, self.data.tseries_movement_points  # todo prova a concatenarle
        # return self.data.observation_ids, self.data.tseries_touch_up_points  # todo prova a concatenarle

    def get_classes(self):
        return pd.Series(self.data.items)

    def fit_predict(self):

        c = Chrono("Splitting into train/set...")
        obs_ids, tseries = self.get_timeseries()
        x_train, x_test, tseries_train, tseries_test, y_train, y_test = self.tseries_train_test_split(
            tseries,
            self.get_classes(),
            self.data.observation_ids)
        c.millis()

        print("Tseries train", tseries_train.shape)
        print("xtrain train", x_train.shape)
        print("ytrain train", y_train.shape)
        print("Tseries test", tseries_test.shape)
        print("xtest test", x_test.shape)

        print("y_test", len(y_test))
        # print(x_train.shape)
        # print(x_test.shape)
        # print(tseries_train.shape)
        # print(tseries_test.shape)
        # print(y_train.shape)
        # print(y_test.shape)
        # print(tseries_test.head())

        c = Chrono("Building pipeline...")
        self.pipeline = self.build_pipeline()
        c.millis()

        c = Chrono("Fitting pipeline...")
        self.pipeline.set_params(augmenter__timeseries_container=tseries_train)
        self.pipeline.fit(x_train, y_train)
        c.millis()

        c = Chrono("Predicting classes...")
        self.pipeline.set_params(augmenter__timeseries_container=tseries_test)
        y_pred = self.pipeline.predict(x_test)
        c.millis()

        c = Chrono("Predicting probas..")
        y_proba = self.pipeline.predict_proba(x_test)
        c.millis()

        # todo try to evaluate the random classifier

        r = sklearn.metrics.classification_report(y_test, y_pred)
        utils.save_string(r, ResultsPaths.classification_report(self.data.dataset_name, "some_testing"), override=True)
        print(r)

        b = "\Best estimator:\n" + str(self.get_classifier().best_estimator_)
        utils.save_string(b, ResultsPaths.best_params(self.data.dataset_name, "some_testing"), override=True)

        ranks, cms_values = cmc_curve(y_test, y_proba, self.get_classifier().classes_)
        ClassificationPerformances.cmc(ResultsPaths.cmc(DATASET_NAME_0, "some_testing"), ranks, cms_values)

        out = {}
        for p, y in zip(y_proba, y_test):
            predictions = list(zip(p, self.get_classifier().classes_))
            if y not in out:
                out[y] = []
            out[y].append([x for _, x in sorted(predictions, key=lambda x: x[0], reverse=True)])
        utils.save_json(out, ResultsPaths.ranking(self.data.dataset_name, "some_testing"))

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

    @staticmethod
    def feature_augmenter():
        return RelevantFeatureAugmenter(column_id=OBSERVATION_ID,
                                        column_sort=TIME,
                                        n_jobs=12,
                                        ml_task='classification')

    @staticmethod
    def scaler():
        return RobustScaler()

    @staticmethod
    def classifier():
        tuned_parameters = [{'kernel': ['rbf'],
                             'gamma': ['auto', 0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
                             'C': [0.001, 0.1, 1, 10, 100, 500, 1000, 2500, 4000, 4500, 5000, 5500,
                                   6000, 7000, 7500, 8000, 10000]}]

        return GridSearchCV(SVC(probability=True), tuned_parameters, cv=4, refit=True, n_jobs=-1)
        # return SVC(C=7500, gamma=1e-07, probability=True)

    @staticmethod
    def build_pipeline():
        return Pipeline(
            steps=[
                (Learner.AUGMENTER, Learner.feature_augmenter()),
                (Learner.SCALER, Learner.scaler()),
                (Learner.CLASSIFIER, Learner.classifier())
            ]
        )

    def get_feature_augmenter(self):
        assert self.pipeline
        return self.pipeline.named_steps[Learner.AUGMENTER]

    def get_scaler(self):
        assert self.pipeline
        return self.pipeline.named_steps[Learner.SCALER]

    def get_classifier(self):
        assert self.pipeline
        return self.pipeline.named_steps[Learner.CLASSIFIER]


if __name__ == '__main__':
    print("RESULTS TIME: {}".format(ResultsPaths.get_time()))
    Learner.get_instance(DATASET_NAME_0, renew_cache=True)

