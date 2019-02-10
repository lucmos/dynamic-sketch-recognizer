import sklearn

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import SVC
from tsfresh.transformers import RelevantFeatureAugmenter

from src.constants.paths_generator import CachePaths, ResultsPaths

# warnings.simplefilter(action='ignore', category=FutureWarning)
import logging

from src.evaluation.classification import save_cmc_curve, save_confusion_matrix, save_prfs_matrix

logging.basicConfig(level=logging.ERROR)

import pandas as pd

import src.data_manager as dm
from src.constants.literals import *
from src.utility.chronometer import Chrono
from src.utility import utils


# pd.options.display.max_rows = 10000#

class Learner:
    version = "1.4"

    TUNED_PARAMETERS = [{'kernel': ['rbf'],
                         'gamma': ['auto', 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8],
                         'C': [0.001, 1, 100, 1000, 2500, 4000, 4500, 5000, 5500,
                               6000, 7000, 7500, 8000]}]
    TEST_SIZE = 0.35

    # FDR_LEVEL = 0.15

    # If AUGMENTER changes, even the name of the optional parameter in pipeline.set_params must change
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
        _instance.fit_predict()
        utils.save_pickle(_instance, CachePaths.learner(dataset_name, Learner.version), override=True)
        c.millis("Saving into: {}".format(CachePaths.learner(dataset_name, Learner.version)))
        return _instance

    def __init__(self, dataset_name):
        self.data = dm.DataManager(dataset_name)

        self.x_train = None
        self.x_test = None
        self.tseries_train = None
        self.tseries_test = None
        self.y_train = None
        self.y_test = None

        self.classes = None
        self.y_test = None
        self.y_pred = None
        self.y_proba = None

    def get_timeseries(self):
        return self.data.observation_ids, self.data.tseries_movement_points  # todo prova a concatenarle
        # return self.data.observation_ids, self.data.tseries_touch_up_points  # todo prova a concatenarle

    def get_labels(self):
        return pd.Series(self.data.items)

    def fit_predict(self):

        c = Chrono("Splitting into train/set...")
        obs_ids, tseries = self.get_timeseries()
        self.x_train, self.x_test, self.tseries_train, self.tseries_test, self.y_train, self.y_test = self.tseries_train_test_split(
            tseries,
            self.get_labels(),
            self.data.observation_ids)
        c.millis()

        print("Tseries train", self.tseries_train.shape)
        print("xtrain train", self.x_train.shape)
        print("ytrain train", self.y_train.shape)
        print("Tseries test", self.tseries_test.shape)
        print("xtest test", self.x_test.shape)
        print("y_test", len(self.y_test))

        c = Chrono("Building pipeline...")
        pipeline = self.build_pipeline()
        c.millis()

        c = Chrono("Fitting pipeline...")
        pipeline.set_params(augmenter__timeseries_container=self.tseries_train)
        pipeline.fit(self.x_train, self.y_train)
        c.millis()

        c = Chrono("Predicting classes...")
        pipeline.set_params(augmenter__timeseries_container=self.tseries_test)
        self.y_pred = pipeline.predict(self.x_test)
        c.millis()

        c = Chrono("Predicting probas..")
        self.y_proba = pipeline.predict_proba(self.x_test)
        c.millis()

        self.classes = self.get_classifier(pipeline).classes_

        self.evaluate()

        b = "Best estimator:\n" + str(self.get_classifier(pipeline).best_estimator_)
        utils.save_string(b, ResultsPaths.best_params(self.data.dataset_name, Learner.version), override=True)

        # save parameters
        utils.save_json(Learner.TUNED_PARAMETERS, ResultsPaths.parameters(self.data.dataset_name, "tuned_parameters_{}".format(Learner.version)))
        utils.save_json(Learner.TEST_SIZE, ResultsPaths.parameters(self.data.dataset_name, "test_size_{}".format(Learner.version)))
        utils.save_string(str(pipeline.named_steps), ResultsPaths.parameters(self.data.dataset_name, "pipeline_{}".format(Learner.version)))

    @staticmethod
    def tseries_train_test_split(tseries, items, observation_ids, test_size=TEST_SIZE):
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
        return RobustScaler() #todo prova senza o con standard scaler

    @staticmethod
    def classifier():
        return GridSearchCV(SVC(probability=True), Learner.TUNED_PARAMETERS, cv=4, refit=True, n_jobs=-1)
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

    @staticmethod
    def get_feature_augmenter(pipeline):
        assert pipeline
        return pipeline.named_steps[Learner.AUGMENTER]

    @staticmethod
    def get_scaler(pipeline):
        assert pipeline
        return pipeline.named_steps[Learner.SCALER]

    @staticmethod
    def get_classifier(pipeline):
        assert pipeline
        return pipeline.named_steps[Learner.CLASSIFIER]

    def evaluate(self):
        r = sklearn.metrics.classification_report(self.y_test, self.y_pred)
        utils.save_string(r, ResultsPaths.classification_report(self.data.dataset_name, Learner.version), override=True)

        save_cmc_curve(ResultsPaths.cmc(self.data.dataset_name, Learner.version), self.y_test, self.y_proba, self.classes)
        save_confusion_matrix(ResultsPaths.confusion_matrix(self.data.dataset_name, Learner.version), self.y_test, self.y_pred, self.classes)
        save_prfs_matrix(ResultsPaths.prfs_matrix(self.data.dataset_name, Learner.version), self.y_test, self.y_pred, self.classes)

        out = {}
        for p, y in zip(self.y_proba, self.y_test):
            predictions = list(zip(p, self.classes))
            if y not in out:
                out[y] = []
            out[y].append([x for _, x in sorted(predictions, key=lambda x: x[0], reverse=True)])
        utils.save_json(out, ResultsPaths.ranking(self.data.dataset_name, Learner.version))


if __name__ == '__main__':
    print("RESULTS TIME: {}".format(ResultsPaths.get_time()))
    l = Learner.get_instance(DATASET_NAME_0, renew_cache=True)

