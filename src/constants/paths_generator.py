import os
import time


from .io_constants import RES_FOLDER, ANIMATION_FOLDER_NAME, GIF2D_FOLDER_NAME, DECOMPOSITION_3D_FOLDER_NAME, \
    GIF_EXTENSION, \
    PNG_EXTENSION, GIF3D_FOLDER_NAME, PLOT2D_FOLDER_NAME, DATA_VISUALIZATION, CACHE_FOLDER_NAME, CACHE_FEATURES, \
    RESULTS_FOLDER_NAME, CMC_FOLDER_NAME, CACHE_LEARNER, CLASSIFICATION_REPORT, TXT_EXTENSION, PREDICTIONS_RANKING, \
    BEST_PARAMS, PARAMETERS
from .io_constants import ROOT_FOLDER
from .io_constants import OUTPUT_FOLDER_NAME
from .io_constants import PICS_FOLDER_NAME
from .io_constants import PICKLE_EXTENSION


class Paths:
    @staticmethod
    def dataset_folder(dataset_name):
        return os.path.join(RES_FOLDER, dataset_name)

    @staticmethod
    def output_folder(dataset_name):
        return os.path.join(ROOT_FOLDER, OUTPUT_FOLDER_NAME, dataset_name)


class DataVisPaths:
    # folders
    @staticmethod
    def data_visualization_folder(dataset_name):
        return os.path.join(Paths.output_folder(dataset_name), DATA_VISUALIZATION)

    @staticmethod
    def pics_folder(dataset_name):
        return os.path.join(DataVisPaths.data_visualization_folder(dataset_name), PICS_FOLDER_NAME)

    @staticmethod
    def animation_folder(dataset_name):
        return os.path.join(DataVisPaths.data_visualization_folder(dataset_name), ANIMATION_FOLDER_NAME)

    @staticmethod
    def plot2d_folder(datset_name):
        return os.path.join(DataVisPaths.pics_folder(datset_name), PLOT2D_FOLDER_NAME)

    @staticmethod
    def gif2d_folder(datset_name):
        return os.path.join(DataVisPaths.animation_folder(datset_name), GIF2D_FOLDER_NAME)

    @staticmethod
    def decomposition3d_folder(datset_name):
        return os.path.join(DataVisPaths.animation_folder(datset_name), DECOMPOSITION_3D_FOLDER_NAME)

    @staticmethod
    def gif3d_folder(datset_name):
        return os.path.join(DataVisPaths.animation_folder(datset_name), GIF3D_FOLDER_NAME)

    #files
    @staticmethod
    def file(folder_path, fname, extension, subfolder=None):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def gif(datset_name, subfolder, fname):
        return DataVisPaths.file(DataVisPaths.gif2d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def gif3d(datset_name, subfolder, fname):
        return DataVisPaths.file(DataVisPaths.gif3d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def decomposition_gif3d(datset_name, subfolder, fname):
        return DataVisPaths.file(DataVisPaths.decomposition3d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def plot2d(datset_name, subfolder, fname):
        return DataVisPaths.file(DataVisPaths.plot2d_folder(datset_name), fname, PNG_EXTENSION, subfolder=subfolder)


class CachePaths:
    @staticmethod
    def cache_folder(dataset_name):
        return os.path.join(ROOT_FOLDER, CACHE_FOLDER_NAME, dataset_name)

    @staticmethod
    def cache_file(folder_path, subfolder, fname, extension):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def features(dataset_name, fname):
        return CachePaths.cache_file(CachePaths.cache_folder(dataset_name), CACHE_FEATURES, fname, PICKLE_EXTENSION)

    @staticmethod
    def learner(dataset_name, fname):
        return CachePaths.cache_file(CachePaths.cache_folder(dataset_name), CACHE_LEARNER, fname, PICKLE_EXTENSION)


class ResultsPaths:

    TIME = None

    @staticmethod
    def get_time():
        if ResultsPaths.TIME is None:
            ResultsPaths.TIME = time.strftime('%d.%m.%Y_%H.%M')
        return ResultsPaths.TIME


    @staticmethod
    def results_folder(dataset_name):

        return os.path.join(Paths.output_folder(dataset_name), RESULTS_FOLDER_NAME, ResultsPaths.get_time())

    @staticmethod
    def result_file(folder_path, subfolder, fname, extension):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def cmc(dataset_name, fname):
        return ResultsPaths.result_file(ResultsPaths.results_folder(dataset_name), CMC_FOLDER_NAME, fname, PNG_EXTENSION)

    @staticmethod
    def classification_report(dataset_name, fname):
        return ResultsPaths.result_file(ResultsPaths.results_folder(dataset_name), CLASSIFICATION_REPORT, fname, TXT_EXTENSION)

    @staticmethod
    def ranking(dataset_name, fname):
        return ResultsPaths.result_file(ResultsPaths.results_folder(dataset_name), PREDICTIONS_RANKING, fname, TXT_EXTENSION)

    @staticmethod
    def parameters(dataset_name, fname):
        return ResultsPaths.result_file(ResultsPaths.results_folder(dataset_name), PARAMETERS, fname, TXT_EXTENSION)

    @staticmethod
    def best_params(dataset_name, fname):
        return ResultsPaths.result_file(ResultsPaths.results_folder(dataset_name), BEST_PARAMS, fname, TXT_EXTENSION)

# BUILD_DATAFRAME_PICKLE_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_GENERATED_FOLDER(dataset_name), file,
#                                                                          DATAFRAME, PICKLE_EXTENSION)
# BUILD_DATAFRAME_CSV_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_CSV_FOLDER(dataset_name), file,
#                                                                       DATAFRAME, CSV_EXTENSION)
#
# BUILD_FEATURE_PICKLE_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_GENERATED_FOLDER(dataset_name), file,
#                                                                        FEATURE, PICKLE_EXTENSION)
# BUILD_FEATURE_CSV_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_CSV_FOLDER(dataset_name), file,
#                                                                     FEATURE, CSV_EXTENSION)
#
# PATHS_FUN = {DATAFRAME:
#                  {PICKLE_EXTENSION: BUILD_DATAFRAME_PICKLE_PATH,
#                   CSV_EXTENSION: BUILD_DATAFRAME_CSV_PATH},
#              FEATURE:
#                  {PICKLE_EXTENSION: BUILD_FEATURE_PICKLE_PATH,
#                   CSV_EXTENSION: BUILD_FEATURE_CSV_PATH}}







# BUILD_RESULTS_HAND_FOLDER = lambda res, modality, hand: os.path.join(res, modality, hand)
# BUILD_RESULTS_PATH = lambda results_folder, handwriting, name, desc: BUILD_FILE_PATH(results_folder, handwriting + "_" + name, desc, PNG_EXTENSION)
