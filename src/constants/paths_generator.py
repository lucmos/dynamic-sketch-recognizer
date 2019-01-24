import os
import time

from .io_constants import RES_FOLDER, ANIMATION_FOLDER_NAME, GIF2D_FOLDER_NAME, DECOMPOSITION_3D_FOLDER_NAME, \
    GIF_EXTENSION, \
    PNG_EXTENSION, GIF3D_FOLDER_NAME, PLOT2D_FOLDER_NAME, DATA_VISUALIZATION, CACHE_FOLDER_NAME, CACHE_FEATURES
from .io_constants import _RES_SUFFIX
from .io_constants import ROOT_FOLDER
from .io_constants import OUTPUT_FOLDER_NAME
from .io_constants import GENERATED_FOLDER_NAME
from .io_constants import CSV_FOLDER_NAME
from .io_constants import PICS_FOLDER_NAME
from .io_constants import PICKLE_EXTENSION
from .io_constants import DATAFRAME
from .io_constants import CSV_EXTENSION


class FolderPaths:
    @staticmethod
    def dataset_folder(dataset_name):
        return os.path.join(RES_FOLDER, dataset_name)

    @staticmethod
    def output_folder(dataset_name):
        return os.path.join(ROOT_FOLDER, OUTPUT_FOLDER_NAME, dataset_name)

    @staticmethod
    def cache_folder(dataset_name):
        return os.path.join(ROOT_FOLDER, CACHE_FOLDER_NAME, dataset_name)

    @staticmethod
    def results_folder(dataset_name):
        return os.path.join(FolderPaths.output_folder(dataset_name), time.strftime('%H-%M_%d-%m-%Y'))

    @staticmethod
    def data_visualization_folder(dataset_name):
        return os.path.join(FolderPaths.output_folder(dataset_name), DATA_VISUALIZATION)

    @staticmethod
    def pics_folder(dataset_name):
        return os.path.join(FolderPaths.data_visualization_folder(dataset_name), PICS_FOLDER_NAME)

    @staticmethod
    def animation_folder(dataset_name):
        return os.path.join(FolderPaths.data_visualization_folder(dataset_name), ANIMATION_FOLDER_NAME)

    @staticmethod
    def plot2d_folder(datset_name):
        return os.path.join(FolderPaths.pics_folder(datset_name), PLOT2D_FOLDER_NAME)

    @staticmethod
    def gif2d_folder(datset_name):
        return os.path.join(FolderPaths.animation_folder(datset_name), GIF2D_FOLDER_NAME)

    @staticmethod
    def decomposition3d_folder(datset_name):
        return os.path.join(FolderPaths.animation_folder(datset_name), DECOMPOSITION_3D_FOLDER_NAME)

    @staticmethod
    def gif3d_folder(datset_name):
        return os.path.join(FolderPaths.animation_folder(datset_name), GIF3D_FOLDER_NAME)


class FilePaths:
    @staticmethod
    def file(folder_path, fname, extension, subfolder=None):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def gif(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.gif2d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def gif3d(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.gif3d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def decomposition_gif3d(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.decomposition3d_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def plot2d(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.plot2d_folder(datset_name), fname, PNG_EXTENSION, subfolder=subfolder)


class CachePaths:
    @staticmethod
    def cache_file(folder_path, subfolder, fname, extension):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def features(dataset_name, fname):
        return CachePaths.cache_file(FolderPaths.cache_folder(dataset_name), CACHE_FEATURES, fname, PICKLE_EXTENSION)

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
