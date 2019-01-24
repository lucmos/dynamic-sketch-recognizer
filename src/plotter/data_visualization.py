import os
import itertools
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import src.utility.chronometer as chronometer

from . import _appareance as aspect


class TimeSeries2D:

    def __init__(self, tseries: pd.DataFrame,
                 filename: str,
                 title: str = None,
                 height: int = 1080,
                 width: int = 1920,
                 component_column: str = "component",
                 x_column: str = "x",
                 y_column: str = "y"):
        self.tseries = tseries
        self.title = title

        self.component_column = component_column
        self.x_column = x_column
        self.y_column = y_column

        aspect.set_white_chart()

        self.width = width
        self.height = height

        self.colors_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        self.color_map = {}

        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self._generate_plot()

    def _generate_plot(self):
        chrono = chronometer.Chrono("Generating 2D plot for: {}...".format(self.filename))
        if os.path.isfile(self.filename):
            chrono.millis("already exixst")
            return

        ax = None
        colors = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        for i, component in enumerate(g for _, g in self.tseries.groupby(self.component_column)):
            ax = component[["x", "y"]].plot(x=self.x_column, y=self.y_column,
                                            kind="scatter", c=next(colors)['color'],
                                            ax=ax if ax else None)

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)

        # plt.title(self.title)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        plt.savefig(self.filename, dpi=400)
        chrono.millis()


class TimeSeries2DGIF:

    def __init__(self, tseries: pd.DataFrame, filename: str,
                 title: str = None,
                 after_delay: int = 1000,
                 height: int = 1080,
                 width: int = 1920,
                 time_column: str = "time",
                 component_column: str = "component",
                 x_column: str = "x",
                 y_column: str = "y"):
        """
        Generates a gif from a timeseries of points, the speed of the gif
        reproduces the time reported in the series.
        The timeseries must be represented in a pandas dataframe,
        it must contain the columns: time, component, x, y.

        :param tseries: pandas dataframe with the required columns
        :param filename: the full filename in which the gif will be created
        :param title: the title of the gif, None means no title
        :param after_delay: delay between loops (not working)
        :param height: the heigth of the gif in pixels
        :param width: the width of the gif in pixels
        :param time_column: the label of the time column
        :param x_column: the label of the x column
        :param y_column: the label of the y column
        :param component_column: the label of the connected component column,
                                 it can be None.
        """
        self.tseries = tseries
        self.title = title

        self.time_column = time_column
        self.component_column = component_column
        self.x_column = x_column
        self.y_column = y_column

        aspect.set_white_chart()

        self.repeat_delay = after_delay

        self.width = width
        self.height = height

        self.colors_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        self.color_map = {}

        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self._generate_animation()

    @staticmethod
    def _update_plot(i, a, delay_between_frames):
        _clean_axes(a.ax)

        data = a.tseries[a.tseries[a.time_column] <= i * delay_between_frames]
        if a.component_column:
            for i, group in data.groupby(a.component_column):
                if i not in a.color_map:
                    a.color_map[i] = next(a.colors_cycle)['color']
                color = a.color_map[i]
                a.ax.scatter(group[a.x_column], group[a.y_column], c=color, s=plt.rcParams['lines.markersize'] * 2)
        else:
            if not hasattr(a, 'c_components'):
                a.c_components = next(a.colors_cycle)['color']
            a.ax.scatter(data[a.x_column], data[a.y_column], c=a.c_components, s=plt.rcParams['lines.markersize'] * 2)

    def _generate_animation(self):
        chrono = chronometer.Chrono("Generating 2D gif for: {}...".format(self.filename))
        if os.path.isfile(self.filename):
            chrono.millis("already exixst")
            return

        fig = plt.figure()
        self.ax = fig.add_subplot(111)

        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        self.ax.xaxis.label.set_visible(False)
        self.ax.yaxis.label.set_visible(False)

        # plt.tight_layout()
        if self.title:
            self.ax.set_title(self.title)

        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()

        # the number of frames in the gif is equal to the number of points
        frames = self.tseries.shape[0]

        # get the end time
        end_time = max(self.tseries[self.time_column])
        delay_between_frames = end_time / (frames - 1)

        ani = animation.FuncAnimation(fig, self._update_plot,
                                      fargs=(self, delay_between_frames,),
                                      # workaround to repeat_delay not working
                                      frames=int(frames + (self.repeat_delay / delay_between_frames)),
                                      interval=delay_between_frames,
                                      repeat=True,
                                      repeat_delay=self.repeat_delay,
                                      blit=False)

        ani.save(self.filename, writer='imagemagick')
        plt.close(fig)
        chrono.millis()


class TimeSeries3DGIF:
    def __init__(self, tseries: pd.DataFrame, filename: str,
                 title: str = None,
                 after_delay: int = 1000,
                 height: int = 1080,
                 width: int = 1920,
                 time_column: str = "time",
                 component_column: str = "component",
                 x_column: str = "x",
                 y_column: str = "y"):
        self.tseries = tseries
        self.title = title

        self.time_column = time_column
        self.component_column = component_column
        self.x_column = x_column
        self.y_column = y_column

        aspect.set_white_chart()

        self.repeat_delay = after_delay

        self.width = width
        self.height = height

        self.colors_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        self.color_map = {}

        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self._generate_animation()

    @staticmethod
    def _update_plot(i, a, delay_between_frames):
        _clean_axes(a.ax)
        data = a.tseries[a.tseries[a.time_column] <= i * delay_between_frames]
        if a.component_column:
            for i, component in enumerate(g for _, g in data.groupby(a.component_column)):
                if i not in a.color_map:
                    a.color_map[i] = next(a.colors_cycle)['color']
                color = a.color_map[i]

                x = component[a.x_column]
                y = component[a.y_column]
                z = component[a.time_column]

                a.ax.scatter(y, x, z, c=color, s=plt.rcParams['lines.markersize'] * 2)
        else:
            if not hasattr(a, 'c_components'):
                a.c_components = next(a.colors_cycle)['color']

            x = data[a.x_column]
            y = data[a.y_column]
            z = data[a.time_column]
            a.ax.scatter(y, x, z, c=a.c_components, s=plt.rcParams['lines.markersize'] * 2)

    def _generate_animation(self):
        chrono = chronometer.Chrono("Generating 3D gif for: {}...".format(self.filename))
        if os.path.isfile(self.filename):
            chrono.millis("already exixst")
            return

        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.w_xaxis.set_pane_color((1, 1, 1, 0))
        self.ax.w_yaxis.set_pane_color((1, 1, 1, 0))
        self.ax.w_zaxis.set_pane_color((1, 1, 1, 0))

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])

        # self.ax.xaxis.set_ticks_position('none')  # tick markers
        # self.ax.yaxis.set_ticks_position('none')

        if self.title:
            self.ax.set_title(self.title)

        # plt.title(self.title)
        maxv = max(self.tseries[self.time_column])
        self.ax.set_xlim(0, self.height)
        self.ax.set_ylim(0, self.width)
        self.ax.set_zlim(0, maxv)
        self.ax.set_zlabel('\ntime', linespacing=-4)

        frames = self.tseries.shape[0]

        # get the end time
        end_time = max(self.tseries[self.time_column])
        delay_between_frames = end_time / (frames - 1)

        # ChartCreator.set_axes_equal(self.ax)
        ani = animation.FuncAnimation(fig, self._update_plot,
                                      fargs=(self, delay_between_frames),
                                      frames=int(frames + (self.repeat_delay / delay_between_frames)),
                                      interval=delay_between_frames,
                                      repeat=True,
                                      repeat_delay=self.repeat_delay,
                                      blit=False)
        ani.save(self.filename, writer='imagemagick')
        plt.close(fig)
        chrono.millis()


class TimeSeriesDecomposition3DGIF:
    def __init__(self, tseries: pd.DataFrame, filename: str,
                 scaling_rate: int = 50,
                 delay_between_frames: float = 1,
                 fps: int = 60,
                 title: str = None,
                 after_delay: int = 1000,
                 height: int = 1080,
                 width: int = 1920,
                 time_column: str = "time",
                 component_column: str = "component",
                 x_column: str = "x",
                 y_column: str = "y"):
        self.tseries = tseries
        self.scaling_rate = scaling_rate
        self.delay_between_frames = delay_between_frames
        self.fps = fps

        self.title = title

        self.time_column = time_column
        self.component_column = component_column
        self.x_column = x_column
        self.y_column = y_column

        aspect.set_white_chart()

        self.repeat_delay = after_delay

        self.width = width
        self.height = height

        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        self._generate_animation()

    @staticmethod
    def _update_plot(scaling, a, maxv):
        if scaling is None:
            return
        colors_cycle = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        _clean_axes(a.ax)

        if a.component_column:
            for i, component in enumerate(g for _, g in a.tseries.groupby(a.component_column)):
                x = component[a.x_column]
                y = component[a.y_column]
                z = component[a.time_column] / maxv * scaling
                a.ax.scatter(y, x, z, c=next(colors_cycle)['color'])
        else:
            if not hasattr(a, 'c_components'):
                a.c_components = next(a.colors_cycle)['color']
            x = a.tseries[a.x_column]
            y = a.tseries[a.y_column]
            z = a.tseries[a.time_column] / maxv * scaling
            a.ax.scatter(y, x, z, c=a.c_components)

    def _generate_animation(self):
        chrono = chronometer.Chrono("Generating 3D decomposition for: {}...".format(self.filename))
        if os.path.isfile(self.filename):
            chrono.millis("already exixst")
            return

        maxv = max(self.tseries[self.time_column])
        scaling_list = range(0, maxv + 1, self.scaling_rate)

        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.w_xaxis.set_pane_color((1, 1, 1, 0))
        self.ax.w_yaxis.set_pane_color((1, 1, 1, 0))
        self.ax.w_zaxis.set_pane_color((1, 1, 1, 0))

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])

        # self.ax.xaxis.set_ticks_position('none')  # tick markers
        # self.ax.yaxis.set_ticks_position('none')

        if self.title:
            self.ax.set_title(self.title)

        self.ax.set_xlim(0, self.height)
        self.ax.set_ylim(0, self.width)
        self.ax.set_zlim(0, maxv)
        self.ax.set_zlabel('\ntime', linespacing=-4)

        # ChartCreator.set_axes_equal(self.ax)

        # avoid bug on repeat_delay
        frozen_frames = ([None] * int(self.repeat_delay / self.delay_between_frames / self.scaling_rate))
        ani = animation.FuncAnimation(fig, self._update_plot,
                                      fargs=(self, maxv,),
                                      frames=list(scaling_list) + frozen_frames,
                                      interval=self.delay_between_frames,
                                      repeat=True,
                                      repeat_delay=self.repeat_delay,
                                      blit=False)
        ani.save(self.filename, writer='imagemagick', fps=self.fps)
        plt.close(fig)
        chrono.millis()


def _clean_axes(axes):
    for artist in axes.lines + axes.collections:
        artist.remove()
