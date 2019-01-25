import itertools
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import src.utility.chronometer as chronometer
import src.data.json_wrapper as jw
from ..plotter import _appareance


class Plotter:
    #
    # def simplePlot(self,
    #                path,
    #                xaxes,
    #                yaxes,
    #                colors,
    #                labels,
    #                lws = None,
    #                linestyles = None,
    #                xlabel,
    #                ylabel,
    #                title,
    #                xlow=-0.005,
    #                ylow=-0.005,
    #                xhigh=1,
    #                yhigh=1.01,
    #                legendpos="lower right",
    #                yscale=True,
    #                xscale=True,
    #                integer_x=False):
    #     assert len(xaxes) == len(yaxes)
    #     assert not colors or len(colors) == len(xaxes), "{}, {}".format(len(colors), len(xaxes))
    #     assert not labels or len(labels) == len(xaxes)
    #     assert not lws or len(lws) == len(xaxes)
    #     assert not linestyles or len(linestyles) == len(xaxes), "{}, {}".format(len(linestyles), len(xaxes))
    #
    #     _appareance.set_ggplot_style()
    #
    #     fig = plt.figure()
    #
    #
    #
    #     for i, (x, y) in enumerate(zip(xaxes, yaxes)):
    #         plt.plot(x, y,
    #                  color=colors[i] if colors else None,
    #                  lw=lws[i] if lws else None,
    #                  label=labels[i] if labels else None,
    #                  linestyle=linestyles[i] if linestyles else None)
    #     if xscale:
    #         plt.xlim([xlow, xhigh])
    #     if yscale:
    #         plt.ylim([ylow, yhigh])
    #     if integer_x:
    #         plt.axes().xaxis.set_major_locator(MaxNLocator(integer=True))
    #
    #     plt.xlabel(xlabel)
    #     plt.ylabel(ylabel)
    #     plt.title(title)
    #     plt.legend(loc=legendpos)
    #     plt.savefig(path, dpi=400)
    #     # plt.show()
    #     plt.close(fig)

    @staticmethod
    def cmc(filename, ranks, cms_values, color='darkorange', label=None):
        # labels = ["{} (rr = {:.4f})".format(svm_name, cmc_values[1])] todo copia
        _appareance.set_ggplot_style()

        fig = plt.figure()

        ax = fig.add_subplot(111)

        ax.plot(ranks, cms_values,
                color=color,
                label="recognition rate: {:.4f}".format(cms_values[0]))

        ax.set_xlabel("Rank")
        ax.set_ylabel("Probability of Recognition")
        ax.set_title("Cumulative Match Characteristic")
        ax.set_ylim([0, 1.005])
        ax.set_xlim([0, len(ranks) + 1])

        ax.legend(loc="lower right")

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fig.savefig(filename, dpi=400)

