# -*- coding: utf-8 -*-
import json
import pandas as pd

import src.utility.chronometer as Chronom
import src.json_wrapper as jw
from src.constants.io_constants import BASE_FOLDER, JSON_EXTENSION

from src.constants.paths_generator import FolderPaths, FilePaths
from src.constants.literals import  *
from src.plotter import data_visualization
from src.utils import natural_keys

FILE_BLACK_LIST = [CONFIGURATION_FILE]


class DataManager:

    def __init__(self, dataset_name, update_data=False):
        self.dataset_name = dataset_name

        # one per item
        self.json_objs = []
        self.files_name = []
        self.users_ids = []
        self.observation_id = []
        self.items = []

        # one per point for each item
        self.tseries_movement_points = pd.DataFrame(
            columns=[ITEM_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y])

        self.tseries_touch_up_points = pd.DataFrame(
            columns=[ITEM_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y])

        self.tseries_touch_down_points = pd.DataFrame(
            columns=[ITEM_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y])

        self.series_sampled_points = pd.DataFrame(
            columns=[ITEM_ID,
                     COMPONENT,
                     X,
                     Y])

        self._read_data()
        self._generate_example_charts()
        self.shift_offsets = {}

        # print(self.tseries_touch_down_points)
        # print(self.tseries_touch_up_points)
        # print(self.tseries_movement_points)
        # print(self.series_sampled_points)
        # {word_id: (minX, minY) }

    def _read_data(self):
        assert os.path.isdir(FolderPaths.dataset_folder(self.dataset_name)), \
            "Insert the dataset \"" + self.dataset_name + "\" in: " + BASE_FOLDER

        chrono = Chronom.Chrono("Reading json files...")
        observation_id = 0
        for root, dirs, files in os.walk(FolderPaths.dataset_folder(self.dataset_name), True, None, False):
            for json_file in sorted(files, key=natural_keys):
                if (json_file and json_file.endswith(JSON_EXTENSION)
                        and json_file not in FILE_BLACK_LIST):
                    json_path = os.path.realpath(os.path.join(root, json_file))
                    self._add_itemdata(json_path, json_file, observation_id)
                    observation_id += 1
        chrono.millis("read {} files".format(observation_id))

    def _add_itemdata(self, json_path, json_name, observation_id):
        with open(json_path, 'r') as f:
            itemdata = jw.item_data_from_dict(json.load(f))

            self.json_objs.append(itemdata)
            self.items.append(itemdata.item)
            self.observation_id.append(observation_id)
            self.users_ids.append(self.get_userid(itemdata))
            self.files_name.append(json_name)

            self.tseries_movement_points = self.tseries_movement_points.append(
                pd.DataFrame([{ITEM_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.movement_points]),
                ignore_index=True, sort=True)

            self.tseries_touch_down_points = self.tseries_touch_down_points.append(
                pd.DataFrame([{ITEM_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.touch_down_points]),
                ignore_index=True, sort=True)

            self.tseries_touch_up_points = self.tseries_touch_up_points.append(
                pd.DataFrame([{ITEM_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.touch_up_points]),
                ignore_index=True, sort=True)

            self.series_sampled_points = self.series_sampled_points.append(
                pd.DataFrame([{ITEM_ID: observation_id,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.sampled_points]),
                ignore_index=True, sort=True)

    # def _group_compute_offsets(self, group):
    #     minX = group[X].min()
    #     minY = group[Y].min()
    #     self.shift_offsets[group[ITEM_ID].iloc[0]] = (minX, minY)
    #
    # def _group_shift_x(self, group):
    #     m = self.shift_offsets[group[ITEM_ID].iloc[0]][0]
    #     group[X] = group[X] - m
    #     return group
    #
    # def _group_shift_y(self, group):
    #     m = self.shift_offsets[group[ITEM_ID].iloc[0]][1]
    #     group[Y] = group[Y] - m
    #     return group
    #
    # def _group_shift_xy(self, group):
    #     return self._group_shift_x(self._group_shift_y(group))
    #
    # def _shift(self):
    #     chrono = Chronom.Chrono("Shifting dataframes...")
    #     self.data_frames[MOVEMENT_POINTS].groupby(ITEM_ID).apply(self._group_compute_offsets)
    #
    #     f = {X: self._group_shift_x,
    #          Y: self._group_shift_y,
    #          XY: self._group_shift_xy}
    #
    #     for l in INITIAL_POINTS_SERIES_TYPE:
    #         for dir in [X, Y, XY]:
    #             self.data_frames[GET_SHIFTED_POINTS_NAME(dir, l)] = self.data_frames[l].groupby(ITEM_ID).apply(f[dir])
    #     chrono.millis()

    @staticmethod
    def get_userid(item_data: jw.ItemData):
        return "{}_{}_{}_{}_({})".format(
                                    item_data.item,
                                    item_data.item_index,
                                    item_data.session_data.name,
                                    item_data.session_data.surname,
                                    item_data.session_data.date)

    @staticmethod
    def get_item_tseries(dataframe, item_id):
        """
        Retrieve a single tseries given an id,
        from the dataframe that contains all the time series.

        :param dataframe: the dataframe containing all the tseries
        :param item_id: the item to retrieve
        :return: the tseries of the item identified by item_id
        """
        return dataframe.loc[dataframe[ITEM_ID] == item_id]

    def _generate_example_charts(self):

        from src.plotter.data_visualization import TimeSeries2DGIF

        examples = [
            "pesce_Flavia_ischiboni_40.json",
            "candela_flavia_ischiboni_10.json"
        ]
        dataframe = self.tseries_movement_points
        for ex in examples:
            item_id = self.files_name.index(ex)
            item_data: jw.ItemData = self.json_objs[item_id]

            tseries = DataManager.get_item_tseries(dataframe, item_id)

            h = item_data.session_data.device_data.heigth_pixels
            w = item_data.session_data.device_data.width_pixels

            fname = FilePaths.plot2d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            data_visualization.TimeSeries2D(tseries, fname, height=h, width=w)

            fname = FilePaths.gif(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            data_visualization.TimeSeries2DGIF(tseries, fname, height=h, width=w)

            fname = FilePaths.gif3d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            data_visualization.TimeSeries3DGIF(tseries, fname, height=h, width=w)

            fname = FilePaths.decomposition_gif3d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            data_visualization.TimeSeriesDecomposition3DGIF(tseries, fname, height=h, width=w)


if __name__ == "__main__":
    d = DataManager(DATASET_NAME_0, update_data=False)

    # a = get_wordidfrom_wordnumber_name_surname(d[WORDID_USERID], d[USERID_USERDATA], "Rita", "Battilocchi" , BLOCK_LETTER, 31)
    # print(get_infos(d[WORDID_USERID], d[USERID_USERDATA], a))
    # d._generate_example_charts()

    # import src.json_wrapper as jw
    # j = "../res/TouchRecorder/aereo/luca_moschella_21.01.2019.10.51/aereo_Luca_Moschella_0.json"
    # with open(j, 'r') as f:
    #     s = jw.itemdata_from_dict(json.load(f))
    #     s.sampled_points
    #     print(s)
    # tseries_movement_points = pd.DataFrame(columns=[ITEM_ID,
    #                                                 TIME,
    #                                                 COMPONENT,
    #                                                 X,
    #                                                 Y])
