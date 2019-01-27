import sklearn

import numpy as np

from .plotter import classification_plotter as perf


def save_cmc_curve(filename, y_true, y_predicted_proba, classes, color='darkorange'):
        ranks, cms_values = cmc_curve(y_true, y_predicted_proba, classes)
        perf.plot_cmc(filename, ranks, cms_values, color=color)


def save_prfs_matrix(filename, y_true, y_pred, classes):
    precision, recall, fmeasure, support = sklearn.metrics.precision_recall_fscore_support(y_true, y_pred)
    precision_avg, recall_avg, fmeasure_avg, _ = sklearn.metrics.precision_recall_fscore_support(y_true, y_pred,
                                                                                                 average="weighted")
    perf.plot_prfs_matrix(filename, classes, precision, recall, fmeasure, support, precision_avg, recall_avg,
                          fmeasure_avg)


def save_confusion_matrix(filename, y_true, y_pred, classes):
    conf_matrix = confusion_matrix(y_true, y_pred, classes)
    perf.plot_confusion_matrix(filename, classes, conf_matrix)


# ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ # ~~~ #


def precision_recall_fscore_support(y_true, y_pred, average=None):  # consider: average='weighted'
    precision_avg, recall_avg, fmeasure_avg, support = sklearn.metrics.precision_recall_fscore_support(y_true, y_pred,
                                                                                                       average=average)
    return precision_avg, recall_avg, fmeasure_avg, support


def confusion_matrix(y_true, y_pred, classes=None):
    return sklearn.metrics.confusion_matrix(y_true, y_pred, labels=classes)


def cmc_curve(y_true, y_predicted_proba, classes):
    """
    CMS (at rank k) (Cumulative Match Score (at rank k) – The probability of identification at
    rank k, or even the ratio between the number of individuals which are correctly recognized among
    the first k and the total number of individuals in the test set (probe).

    CMC (Cumulative Match Characteristic) – A Cumulative Match Characteristic (CMC) curve
    shows the CMS value for a certain number of ranks (clearly, each implying the following ones). It
    therefore reports the probability that the correct identity is returned at the first place in the
    ordered list (CMS at rank 1), or at the first or second place (CMS at rank 2), or in general among
    the first k places (CMS at rank k). If the number n of ranks in the curve equals the size of the
    gallery, we will surely have a probability value of 1 at point n.

    The CMS at rank 1 is also defined as Recognition Rate (RR).

    :param y_true: the observation's ground truth
    :param y_predicted_proba: the predicted probabilities for the classes
    :param classes: the classes ordered accordingly
    :return (ranks, values): two lists, where for each rank there is it's value
    """
    cms_values = []
    # iter through each class, rank zero makes no sense
    for rank in range(1, len(classes)):

        # This represent the probability of classifying elements in the first 'rank' positions
        cms_val_rank = 0

        # iter through the observations
        # probs are the predicted probabilities for this observation
        # y is the ground truth class for this observation
        for probs, y in zip(y_predicted_proba, y_true):

            # the index of the ground truth
            y_prob_index = np.where(classes == y)

            # we increase the count if the number of classes that would end up before the ground truth is < rank
            # i.e. we do +1 if the ground truth is within the 'rank' classes with highest probability
            if sum(1 for a in probs if a > probs[y_prob_index]) < rank:
                cms_val_rank += 1

            # # N.B An equivalent, less efficient but more readable, way of performing the computation is the following:
            #
            # # sort the observation by the class-probability
            # sorted_probs = sorted(zip(probs, classes), key=lambda x: x[0], reverse=True)
            #
            # # take the 'rank' most probable classes
            # rank_best_probs = [x for _, x in sorted_probs[0:rank]]
            #
            # # if the ground truth 'y' is within the rank best classes, we have an hit
            # if y in rank_best_probs:
            #    cms_val_rank += 1

        # divide by the number of elements in the probe by definition
        cms_values.append(cms_val_rank / float(len(y_true)))

    # the x-axis are the ranks, the y-axis are the cms values
    return list(range(1, len(classes))), cms_values
