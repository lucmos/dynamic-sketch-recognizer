import os
import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

CMAP = sns.light_palette((210, 90, 60), n_colors=64, input="husl")


def set_ggplot_style():
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use('ggplot')


def plot_cmc(filename, ranks, cms_values, color='darkorange'):
    set_ggplot_style()

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


def plot_confusion_matrix(filename, classes, confusion_matrix):
    """
    Plots the confusion matrix using a seaborn heatmap
    :param classes: labels of the confusion matrix
    :param confusion_matrix: the confusion of matrix, in a list of list format
    """

    sns.set(style="white")
    data = pd.DataFrame(confusion_matrix, index=[i for i in range(len(classes))],
                        columns=[i for i in range(len(classes))])

    f, ax = plt.subplots(figsize=(20, 20))
    annot = data
    data = np.where(data != 0, np.log(data), 0)
    heatmap = sns.heatmap(data, xticklabels=classes, cbar=False, yticklabels=classes, cmap=CMAP,
                          square=True, annot=annot, fmt="g", linewidths=1, annot_kws={"size": 11})  # font size
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=12)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=12)
    plt.title("Confusion Matrix")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=500)
    plt.close(f)


def plot_prfs_matrix(filename, classes, precision, recall, fmeasure, support, precision_avg, recall_avg, fmeasure_avg):
    """
    Plots the precision, recall, f-measure and support for each class and the weighted average.

    :param classes:  the labels of each class
    :param precision: list of precisions
    :param recall: list of recalls
    :param fmeasure: list of fmeasures
    :param support: list of supports
    :param precision_avg: the averaged precision
    :param recall_avg: the averaged recall
    :param fmeasure_avg: the averaged fmeasure
    """
    sns.set(style="white")
    data = pd.DataFrame({"Precision": precision, "Recall": recall, "F-measure": fmeasure, "Support": support},
                        index=classes, columns=["Precision", "Recall", "F-measure", "Support"])
    avg = pd.DataFrame({"Precision": precision_avg, "Recall": recall_avg, "F-measure": fmeasure_avg}, index=["AVERAGE"],
                       columns=["Precision", "Recall", "F-measure", "Support"])

    f, ax = plt.subplots(figsize=(13, 20))

    data["Support"] = data["Support"] / sum(data["Support"])
    data = data.append(avg)
    annot = data
    data = data.apply(_normalization, axis=0)

    sns.heatmap(data, cbar=False, cmap=CMAP, annot=annot, fmt=".1%", linewidths=2.5, annot_kws={"size": 16})
    ax.xaxis.tick_top()
    ax.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
    plt.tight_layout()

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, dpi=500)


def plot(filename,
         x_values,
         y_values,
         legend_pos,
         multiple_labels,
         title,
         y_label,
         x_label,
         label_pattern=None,
         label_parametrization=None,
         ):
    """
    Plots n lines into a single plot

    :param filename: the file name
    :param x_values: a list of values for the x-axis
    :param y_values: a list of values for the y-axis
    :param multiple_labels: the label to use for each line
    :param label_pattern: a single label that can be parametrized by a single value, multiple_labels is ignored
    :param label_parametrization: determine the label used by each line, if None the label is always the same
    :param legend_pos: the position of the legend
    :param title: the title
    :param y_label: the y-label
    :param x_label: the x-label
    :return:
    """
    assert (multiple_labels is None) != (label_pattern is None)
    assert (label_pattern is None) == (label_parametrization is None)

    plt.style.use("ggplot")

    colors = ['darkorange', 'navy', "darkgreen", "tomato"]
    fig = plt.figure()
    for i in range(len(x_values)):
        curr = multiple_labels[i] if multiple_labels else label_pattern.format(label_parametrization[i])
        plt.plot(x_values[i], y_values[i], color=colors[i], lw=1.5, label=curr)

    plt.legend(loc=legend_pos)
    plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    plt.title(title)

    plt.tight_layout()
    plt.savefig(filename, dpi=500)
    plt.close(fig)


def _normalization(array):
    """
    Performs a min-max like-normalization on the array
    :param array: the array to normalize
    :return: the normalized array
    """
    minx = min(array)
    maxx = max(array)
    return [(x - minx) / (maxx - minx) if (maxx - minx) else x for x in array]
