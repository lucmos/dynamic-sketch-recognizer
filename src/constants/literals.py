import os

from .global_constants import *
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

OBSERVATION_ID = "observation_id"
USER_ID = "user_id"
BLOCK_LETTER = "BLOCK_LETTERS"
ITALIC = "ITALIC"

WORDID_USERID = "wordid_userid_map"
USERID_USERDATA = "userid_userdata_map"


POINTS_WITH_WORD_ID = POINTS + [OBSERVATION_ID]
TIMED_POINTS_WITH_WORD_ID = TIMED_POINTS + [OBSERVATION_ID]

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
