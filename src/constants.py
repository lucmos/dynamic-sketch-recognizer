import os

# ***************** json fields ***************** #

DATE = "date"

MOVEMENT_POINTS = "movement_points"
TOUCH_DOWN_POINTS = "touch_down_points"
TOUCH_UP_POINTS = "touch_up_points"
SAMPLED_POINTS = "sampled_points"

ITEM_INDEX = "item_index"
ITEM = "item"

TIME = "time"
COMPONENT = "component"
X = "x"
Y = "y"

SESSION_DATA = "session_data"
NAME = "name"
SURNAME = "surname"
AGE = "age"

GENDER = "gender"
TOTAL_WORD_NUMBER = "totalWordNumber"

DEVICE_DATA = "device_data"
DEVICE_FINGERPRINT = "deviceFingerPrint"
DEVICE_MODEL = "device_model"
HEIGHT_PIXELS = "heigth_pixels"
WIDTH_PIXELS = "width_pixels"
XDPI = "xdpi"
YDPI = "ydpi"


CONFIGURATION = "configuration"
GUIDE_LINES = "guide_lines"
ITEMS = "items"
REPETITIONS = "repetitions"
REPETITIONS_LABEL = "repetitions_label"
TITLE = "title"



# Json structure

JSON_FIELDS = [
    DATE,
    MOVEMENT_POINTS,
    TOUCH_DOWN_POINTS,
    TOUCH_UP_POINTS,
    SAMPLED_POINTS,
    ITEM_INDEX,
    SESSION_DATA,
]

SESSION_DATA_FIELDS = [
    NAME,
    SURNAME,
    AGE,
    GENDER,
    TOTAL_WORD_NUMBER,
    DEVICE_DATA,
]

DEVICE_DATA_FIELDS = [
    DEVICE_FINGERPRINT,
    DEVICE_MODEL,
    HEIGHT_PIXELS,
    WIDTH_PIXELS,
    XDPI,
    YDPI,
]

POINTS = [
    COMPONENT,
    X,
    Y,
]

TIMED_POINTS = POINTS + [TIME]

# *********************************************** #

# other useful labels #
SHIFT = "_shifted_"
XY = X + Y

GET_SHIFTED_POINTS_NAME = lambda shift, x: shift + SHIFT + x
X_SHIFTED_MOVEMENT_POINTS = GET_SHIFTED_POINTS_NAME(X, MOVEMENT_POINTS)
X_SHIFTED_TOUCH_DOWN_POINTS = GET_SHIFTED_POINTS_NAME(X, TOUCH_DOWN_POINTS)
X_SHIFTED_TOUCH_UP_POINTS = GET_SHIFTED_POINTS_NAME(X, TOUCH_UP_POINTS)
X_SHIFTED_SAMPLED_POINTS = GET_SHIFTED_POINTS_NAME(X, SAMPLED_POINTS)
Y_SHIFTED_MOVEMENT_POINTS = GET_SHIFTED_POINTS_NAME(Y, MOVEMENT_POINTS)
Y_SHIFTED_TOUCH_DOWN_POINTS = GET_SHIFTED_POINTS_NAME(Y, TOUCH_DOWN_POINTS)
Y_SHIFTED_TOUCH_UP_POINTS = GET_SHIFTED_POINTS_NAME(Y, TOUCH_UP_POINTS)
Y_SHIFTED_SAMPLED_POINTS = GET_SHIFTED_POINTS_NAME(Y, SAMPLED_POINTS)
XY_SHIFTED_MOVEMENT_POINTS = GET_SHIFTED_POINTS_NAME(XY, MOVEMENT_POINTS)
XY_SHIFTED_TOUCH_DOWN_POINTS = GET_SHIFTED_POINTS_NAME(XY, TOUCH_DOWN_POINTS)
XY_SHIFTED_TOUCH_UP_POINTS = GET_SHIFTED_POINTS_NAME(XY, TOUCH_UP_POINTS)
XY_SHIFTED_SAMPLED_POINTS = GET_SHIFTED_POINTS_NAME(XY, SAMPLED_POINTS)

ITEM_ID = "item_id"
USER_ID = "user_id"
BLOCK_LETTER = "BLOCK_LETTERS"
ITALIC = "ITALIC"

WORDID_USERID = "wordid_userid_map"
USERID_USERDATA = "userid_userdata_map"

JSON_EXTENSION = ".json"
CSV_EXTENSION = ".csv"
PICKLE_EXTENSION = ".pickle"
GIF_EXTENSION = ".gif"
PNG_EXTENSION = ".png"

DATAFRAME = "dataframe"
FEATURE = "features"

POINTS_WITH_WORD_ID = POINTS + [ITEM_ID]
TIMED_POINTS_WITH_WORD_ID = TIMED_POINTS + [ITEM_ID]

INITIAL_TIMED_POINTS_SERIES_TYPE = [MOVEMENT_POINTS, TOUCH_DOWN_POINTS, TOUCH_UP_POINTS]
INITIAL_POINTS_SERIES_TYPE = INITIAL_TIMED_POINTS_SERIES_TYPE + [SAMPLED_POINTS]

TIMED_POINTS_SERIES_TYPE = INITIAL_TIMED_POINTS_SERIES_TYPE + [
    # X_SHIFTED_MOVEMENT_POINTS,
    # X_SHIFTED_TOUCH_DOWN_POINTS,
    # X_SHIFTED_TOUCH_UP_POINTS,
    #
    # Y_SHIFTED_MOVEMENT_POINTS,
    # Y_SHIFTED_TOUCH_DOWN_POINTS,
    # Y_SHIFTED_TOUCH_UP_POINTS,

    XY_SHIFTED_MOVEMENT_POINTS,
    XY_SHIFTED_TOUCH_DOWN_POINTS,
    XY_SHIFTED_TOUCH_UP_POINTS]
POINTS_SERIES_TYPE = TIMED_POINTS_SERIES_TYPE + [SAMPLED_POINTS,
                                                 # X_SHIFTED_SAMPLED_POINTS,
                                                 # Y_SHIFTED_SAMPLED_POINTS,
                                                 XY_SHIFTED_SAMPLED_POINTS]

# files constants
ROOT_FOLDER = ".."
BASE_FOLDER = "../res/"
_RES_SUFFIX = "_res/"

DATASET_NAME_0 = "TouchRecorder"
DATASET_NAME_1 = "Biotouch_sara"
DATASET_NAME_SMALL = "small"

GENERATED_FOLDER = "generated/"
OUTPUT_FOLDER = "outputs"
CSV_FOLDER = "csv/"
PICS_FOLDER = "pics/"

CONFIGURATION_FILE = "configuration.json"

import time
BUILD_DATASET_FOLDER = lambda dataset_name: os.path.join(BASE_FOLDER, dataset_name)
BUILD_RES_FOLDER = lambda dataset_name: BUILD_DATASET_FOLDER(dataset_name + _RES_SUFFIX)
BUILD_OUTPUT_FOLDER = lambda dataset_name: os.path.join(ROOT_FOLDER,  OUTPUT_FOLDER, "output_" + dataset_name)
BUILD_RESULTS_FOLDER = lambda dataset_name: os.path.join(BUILD_OUTPUT_FOLDER(dataset_name), time.strftime('%H-%M_%d-%m-%Y'))

BUILD_GENERATED_FOLDER = lambda dataset_name: os.path.join(BUILD_RES_FOLDER(dataset_name), GENERATED_FOLDER)
BUILD_CSV_FOLDER = lambda dataset_name: os.path.join(BUILD_RES_FOLDER(dataset_name), CSV_FOLDER)
BUILD_PICS_FOLDER = lambda dataset_name: os.path.join(BUILD_OUTPUT_FOLDER(dataset_name), PICS_FOLDER)

BUILD_FILE_PATH = lambda base_path, file, desc, ext: os.path.join(base_path, file + "_" + desc + ext)

BUILD_DATAFRAME_PICKLE_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_GENERATED_FOLDER(dataset_name), file,
                                                                         DATAFRAME, PICKLE_EXTENSION)
BUILD_DATAFRAME_CSV_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_CSV_FOLDER(dataset_name), file,
                                                                      DATAFRAME, CSV_EXTENSION)

BUILD_FEATURE_PICKLE_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_GENERATED_FOLDER(dataset_name), file,
                                                                       FEATURE, PICKLE_EXTENSION)
BUILD_FEATURE_CSV_PATH = lambda dataset_name, file: BUILD_FILE_PATH(BUILD_CSV_FOLDER(dataset_name), file,
                                                                    FEATURE, CSV_EXTENSION)

PATHS_FUN = {DATAFRAME:
                 {PICKLE_EXTENSION: BUILD_DATAFRAME_PICKLE_PATH,
                  CSV_EXTENSION: BUILD_DATAFRAME_CSV_PATH},
             FEATURE:
                 {PICKLE_EXTENSION: BUILD_FEATURE_PICKLE_PATH,
                  CSV_EXTENSION: BUILD_FEATURE_CSV_PATH}}



ANIMATION = "animation"
CHART2D = "chart2D"
CHART3D = "chart3D"

_folder_ANIMATION = "animation/"
_folder_CHART2D = "chart2D/"
_folder_CHART3D = "chart3D/"

def uglify(t):
    return "".join(t.lower().split())


BUILD_GIFS_FOLDER_PATH = lambda dataset_name: os.path.join(BUILD_PICS_FOLDER(dataset_name), _folder_ANIMATION)
BUILD_CHART2D_FOLDER_PATH = lambda dataset_name: os.path.join(BUILD_PICS_FOLDER(dataset_name), _folder_CHART2D)
BUILD_CHART3D_FOLDER_PATH = lambda dataset_name, name, surname, word, handwriting, label: os.path.join(BUILD_PICS_FOLDER(dataset_name), _folder_CHART3D, "charts_{}_{}_{}_{}_{}".format(uglify(name),uglify(surname),word,handwriting, label))

BUILD_GIFS_PATH =       lambda dataset_name, item, user_id,  label: BUILD_FILE_PATH(BUILD_GIFS_FOLDER_PATH(dataset_name), "item_{}_{}".format(uglify(user_id), label), ANIMATION, GIF_EXTENSION)
BUILD_CHART2D_PATH =    lambda dataset_name, item, user_id,  label: BUILD_FILE_PATH(BUILD_CHART2D_FOLDER_PATH(dataset_name), "item_{}_{}".format(uglify(user_id), label), CHART2D, PNG_EXTENSION)
BUILD_CHART3D_PATH =    lambda dataset_name, item, user_id, timescaling, label: BUILD_FILE_PATH(BUILD_CHART3D_FOLDER_PATH(dataset_name, user_id, item, label), "item_{}_{}_timescaling{}_{}".format(uglify(user_id), item, timescaling, label), CHART3D, PNG_EXTENSION)


BUILD_RESULTS_HAND_FOLDER = lambda res, modality, hand: os.path.join(res, modality, hand)
BUILD_RESULTS_PATH = lambda results_folder, handwriting, name, desc: BUILD_FILE_PATH(results_folder, handwriting + "_" + name, desc, PNG_EXTENSION)