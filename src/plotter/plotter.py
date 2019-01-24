import itertools
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import src.utility.chronometer as chronometer
import src.data.json_wrapper as jw


def get_title(jsonobj: jw.ItemData):
    return "{} {} - {} {}".format(
        utils.prettify_name(jsonobj.session_data.name),
        utils.prettify_name(jsonobj.session_data.surname),
        jsonobj.item_index,
        utils.prettify_name(jsonobj.item))



class Plotter:
    def __init__(self, dataset_name):
        self.dataset_name=dataset_name
        self.results_folder = utils.BUILD_RESULTS_FOLDER(dataset_name)

    def _get_path_hand(self, modality, handwriting):
        path = utils.BUILD_RESULTS_HAND_FOLDER(self.results_folder, modality, handwriting)
        utils.mkdir(path)
        return path

    def get_desc(self, desc, balanced):
        return  "{}_{}".format("balanced" if balanced else "notbalanced", desc)

    def simplePlot(self, path, xaxes, yaxes, colors, labels, lws, linestyles, xlabel, ylabel, title, xlow=-0.005, ylow=-0.005, xhigh=1, yhigh=1.01, legendpos="lower right", yscale=True, xscale=True, integer_x=False):
        assert len(xaxes) == len(yaxes)
        assert not colors or len(colors) == len(xaxes), "{}, {}".format(len(colors), len(xaxes))
        assert not labels or len(labels) == len(xaxes)
        assert not lws or len(lws) == len(xaxes)
        assert not linestyles or len(linestyles) == len(xaxes), "{}, {}".format(len(linestyles), len(xaxes))

        set_ggplot_style()

        fig = plt.figure()

        for i, (x, y) in enumerate(zip(xaxes, yaxes)):
            plt.plot(x, y,
                     color=colors[i] if colors else None,
                     lw=lws[i] if lws else None,
                     label=labels[i] if labels else None,
                     linestyle=linestyles[i] if linestyles else None)
        if xscale:
            plt.xlim([xlow, xhigh])
        if yscale:
            plt.ylim([ylow, yhigh])
        if integer_x:
            plt.axes().xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(loc=legendpos)
        plt.savefig(path, dpi=400)
        # plt.show()
        plt.close(fig)

    def plotRoc(self, svm_name, fpr, tpr, auc_score, handwriting, balanced, pathname):
        xaxes = [fpr] + [[0,1]]
        yaxes = [tpr] + [[0,1]]
        colors = ['darkorange', 'navy']
        labels = ["{} (area = {:.4f})".format(svm_name, auc_score), None]
        linestyles = [None, "--"]

        self.simplePlot(utils.BUILD_RESULTS_PATH(self._get_path_hand(VERIFICATION, handwriting), handwriting, pathname, self.get_desc("roc", balanced)),
                        xaxes, yaxes, colors, labels, None, linestyles, "False Positive Rate", "True Positive Rate", "Receiver Operating Characteristic - {}".format(
                utils.prettify_name(handwriting)))

    def plotRocs(self, svm_name, fpr, tpr, auc_score, handwriting, balanced, pathname):
        assert isinstance(svm_name, list)
        assert isinstance(auc_score, list)
        xaxes = fpr + [[0, 1]]
        yaxes = tpr + [[0, 1]]
        colors = [None for _ in svm_name] + ["navy"]
        labels = ["{} (area = {:.4f})".format(svm_name, auc_score) for svm_name, auc_score in zip(svm_name, auc_score)] + [None]
        linestyles = [None for _ in svm_name] + ["--"]
        self.simplePlot(utils.BUILD_RESULTS_PATH(self._get_path_hand(VERIFICATION, handwriting), handwriting, pathname, self.get_desc("roc", balanced)),
                        xaxes, yaxes, colors, labels, None, linestyles, "False Positive Rate", "True Positive Rate", "Receiver Operating Characteristic - {}".format(
                utils.prettify_name(handwriting)))


    def plotFRRvsFPR(self, svm_name, thresholds, frr, fpr, handwriting, balanced, pathname):
        xaxes = [thresholds, thresholds]
        yaxes = [frr, fpr]
        colors = ['darkorange', 'navy']
        lws = [2, 2]
        labels = ["FRR - {}".format(svm_name), "FPR - {}".format(svm_name)]
        self.simplePlot(utils.BUILD_RESULTS_PATH(self._get_path_hand(VERIFICATION, handwriting), handwriting, pathname, self.get_desc("frrVSfpr", balanced)),
                        xaxes, yaxes, colors, labels, lws, None, "Thresholds", "Errors Rate", "FRR vs FPR - {}".format(
                utils.prettify_name(handwriting)), legendpos="upper center")



    def plotCMCs(self, svm_name, rank, cmcvalues, handwriting, pathname):
        assert isinstance(svm_name, list)
        labels = ["{} (rr = {:.4f})".format(s, r[1]) for s, r in zip(svm_name, cmcvalues)]
        self.simplePlot(
            utils.BUILD_RESULTS_PATH(self._get_path_hand(IDENTIFICATION, handwriting), handwriting, pathname, "cmc"),
            rank, cmcvalues, None, labels, None, None, "Rank", "Cms Values", "Cumulative Match Curve - {}".format(
                utils.prettify_name(handwriting)),
            xscale=False,
            yscale=False,
            integer_x=True)

    def plotCMC(self, svm_name, rank, cmc_values, handwriting, pathname):
        xaxes = [rank]
        yaxes = [cmc_values]
        colors = ['darkorange']
        labels = ["{} (rr = {:.4f})".format(svm_name, cmc_values[1])]
        self.simplePlot(
            utils.BUILD_RESULTS_PATH(self._get_path_hand(IDENTIFICATION, handwriting), handwriting, pathname, "cmc"),
            xaxes, yaxes, colors, labels, None, None, "Rank", "Cms Values", "Cumulative Match Curve - {}".format(
                utils.prettify_name(handwriting)),
            xscale=False,
            yscale=False,
            integer_x=True)



class ChartCreator:

    def __init__(self, dataset_name, dataframe, wordid_userid_dataframe, user_data_dataframe,
                 word_id=None, name=None, surname=None, handwriting=None, word_number=None, label=utils.MOVEMENT_POINTS):
        self.word_dataframe, word_id = get_word_data(dataframe[label], wordid_userid_dataframe, user_data_dataframe, word_id,
                                            name, surname, handwriting, word_number)
        self.info = utils.get_infos(wordid_userid_dataframe, user_data_dataframe, word_id)
        utils.mkdir(utils.BUILD_PICS_FOLDER(dataset_name))

        self.dataset_name = dataset_name
        self.dataframe = dataframe
        self.word_id = word_id
        self.label = label
        self.height = self.info[utils.HEIGHT_PIXELS]
        self.width = self.info[utils.WIDTH_PIXELS]
        self.title = get_title(self.info)

    def plot2dataframe(self, xaxes=utils.X, yaxes=utils.Y):
        set_white_chart()
        path = utils.BUILD_CHART2D_PATH(self.dataset_name, self.info[utils.NAME], self.info[utils.SURNAME],
                                        self.info[utils.ITEM_INDEX], self.info[utils.HANDWRITING], self.label)
        chrono = chronometer.Chrono("Plotting 2D Chart for: {}...".format(self.title))
        if os.path.isfile(path):
            chrono.millis("already exixst")
            return

        ax = None
        colors = itertools.cycle(plt.rcParams['axes.prop_cycle'])
        for i, component in enumerate(g for _, g in self.word_dataframe.groupby(utils.COMPONENT)):
            ax = component[["x", "y", utils.TIME]].plot(x=xaxes, y=yaxes, kind="scatter", c=next(colors)['color'],
                                                        ax=ax if ax else None)

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)

        # plt.title(self.title)
        plt.axes().set_aspect('equal')
        plt.axes().invert_yaxis()

        utils.mkdir(utils.BUILD_CHART2D_FOLDER_PATH(self.dataset_name))
        plt.savefig(path, dpi=400)
        chrono.millis()
