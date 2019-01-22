import os
import itertools
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import src.utility.chronometer as chronometer

from . import _appareance as aspect


class TimeSeriesGif:

    def __init__(self, tseries, filename,
                 title=None,
                 after_delay=1000,
                 height=1080,
                 width=1920,
                 time_column="time",
                 component_column="component",
                 x_column="x",
                 y_column="y"):
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
        data = a.tseries[a.tseries[a.time_column] <= i * delay_between_frames]
        if a.component_column:
            for i, group in data.groupby(a.component_column):
                if i not in a.color_map:
                    a.color_map[i] = next(a.colors_cycle)['color']
                color = a.color_map[i]
                plt.scatter(group[a.x_column], group[a.y_column], c=color, s=plt.rcParams['lines.markersize'] * 2)
        else:
            if not hasattr(a, 'c_components'):
                a.c_components = next(a.colors_cycle)['color']
            plt.scatter(data[a.x_column], data[a.y_column], c=a.c_components, s=plt.rcParams['lines.markersize'] * 2)

    def _generate_animation(self):
        chrono = chronometer.Chrono("Generating gif for: {}...".format(self.filename))
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
            plt.title(self.title)

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
                                      frames=int(frames + (self.repeat_delay/delay_between_frames)),
                                      interval=delay_between_frames,
                                      repeat=True,
                                      repeat_delay=self.repeat_delay,
                                      blit=False)

        ani.save(self.filename, writer='imagemagick')
        plt.close(fig)
        chrono.millis()
