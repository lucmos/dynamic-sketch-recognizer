import os
import time

from .io_constants import BASE_FOLDER, ANIMATION_FOLDER_NAME, CHART2D_FOLDER_NAME, CHART3D_FOLDER_NAME, GIF_EXTENSION, \
    PNG_EXTENSION
from .io_constants import _RES_SUFFIX
from .io_constants import ROOT_FOLDER
from .io_constants import OUTPUT_FOLDER_NAME
from .io_constants import GENERATED_FOLDER_NAME
from .io_constants import CSV_FOLDER_NAME
from .io_constants import PICS_FOLDER_NAME
from .io_constants import PICKLE_EXTENSION
from .io_constants import DATAFRAME
from .io_constants import CSV_EXTENSION
from .io_constants import FEATURE


class FolderPaths:
    @staticmethod
    def dataset_folder(dataset_name):
        return os.path.join(BASE_FOLDER, dataset_name)

    @staticmethod
    def output_folder():
        return os.path.join(ROOT_FOLDER, OUTPUT_FOLDER_NAME)

    @staticmethod
    def dataset_output_folder(dataset_name):
        return os.path.join(FolderPaths.output_folder(), "output_" + dataset_name)

    @staticmethod
    def results_folder(dataset_name):
        return os.path.join(FolderPaths.dataset_output_folder(dataset_name), time.strftime('%H-%M_%d-%m-%Y'))

    @staticmethod
    def pics_folder(dataset_name):
        return os.path.join(FolderPaths.output_folder(), PICS_FOLDER_NAME, dataset_name)

    @staticmethod
    def gifs_folder(datset_name):
        return os.path.join(FolderPaths.pics_folder(datset_name), ANIMATION_FOLDER_NAME)

    @staticmethod
    def chart2d_folder(datset_name):
        return os.path.join(FolderPaths.pics_folder(datset_name), CHART2D_FOLDER_NAME)

    @staticmethod
    def chart3d_folder(datset_name, subfolder):
        return os.path.join(FolderPaths.pics_folder(datset_name), CHART3D_FOLDER_NAME, subfolder)


# BUILD_GENERATED_FOLDER = lambda dataset_name: os.path.join(BUILD_RES_FOLDER(dataset_name), GENERATED_FOLDER)
# BUILD_CSV_FOLDER = lambda dataset_name: os.path.join(BUILD_RES_FOLDER(dataset_name), CSV_FOLDER)


class FilePaths:
    @staticmethod
    def file(folder_path, fname, extension, subfolder=None):
        if not subfolder:
            return os.path.join(folder_path, fname + extension)
        return os.path.join(folder_path, subfolder, fname + extension)

    @staticmethod
    def gif(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.gifs_folder(datset_name), fname, GIF_EXTENSION, subfolder=subfolder)

    @staticmethod
    def chart2d(datset_name, fname):
        return FilePaths.file(FolderPaths.chart2d_folder(datset_name), fname, PNG_EXTENSION)

    @staticmethod
    def chart3d(datset_name, subfolder, fname):
        return FilePaths.file(FolderPaths.chart3d_folder(datset_name, fname), fname, GIF_EXTENSION, subfolder=subfolder)


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
