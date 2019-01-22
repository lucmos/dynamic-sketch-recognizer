import os
import warnings

import matplotlib.cbook
import matplotlib.pyplot as plt


warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


# plt.style.use('ggplot')

os.putenv("MAGICK_MEMORY_LIMIT", "4294967296")

IDENTIFICATION = "Identification"
VERIFICATION = "Verification"

import matplotlib as mpl


def set_white_chart():
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('fivethirtyeight')

    mpl.rcParams["figure.facecolor"] = 'white'
    mpl.rcParams["axes.facecolor"] = 'white'
    mpl.rcParams["axes.edgecolor"] = 'white'
    mpl.rcParams["savefig.facecolor"] = 'white'

    mpl.rcParams["xtick.color"] = 'white'
    mpl.rcParams["ytick.color"] = 'white'


def set_fivethirtyeight_style():
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('fivethirtyeight')

    mpl.rcParams["figure.facecolor"] = 'white'
    mpl.rcParams["axes.facecolor"] = 'white'
    mpl.rcParams["axes.edgecolor"] = 'white'
    mpl.rcParams["savefig.facecolor"] = 'white'


def set_ggplot_style():
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('ggplot')
