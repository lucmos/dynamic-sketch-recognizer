# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np

import src.utility.chronometer as Chronom
import src.data.json_wrapper as jw
from src.constants.io_constants import RES_FOLDER, JSON_EXTENSION

from src.constants.paths_generator import DataVisPaths, Paths
from src.constants.literals import *
from src.plotter import tseries_visualization
from src.utility.utils import natural_keys

FILE_BLACK_LIST = [CONFIGURATION_FILE]


class DataManager:

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

        # one per item
        self.json_objs = []
        self.file_names = []
        self.file_paths = []
        self.users_ids = []
        self.observation_ids = []
        self.items = []

        # one per point for each item
        self.tseries_movement_points = pd.DataFrame(
            columns=[OBSERVATION_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y]).astype(np.dtype(float))

        self.tseries_touch_up_points = pd.DataFrame(
            columns=[OBSERVATION_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y]).astype(np.dtype(float))

        self.tseries_touch_down_points = pd.DataFrame(
            columns=[OBSERVATION_ID,
                     TIME,
                     COMPONENT,
                     X,
                     Y]).astype(np.dtype(float))

        self.series_sampled_points = pd.DataFrame(
            columns=[OBSERVATION_ID,
                     COMPONENT,
                     X,
                     Y]).astype(np.dtype(float))

        self._read_data()
        self._generate_example_charts()

        self.tseries_movement_points = DataManager.normalize_positions(self.tseries_movement_points)
        self.tseries_touch_down_points = DataManager.normalize_positions(self.tseries_touch_down_points)
        self.tseries_touch_up_points = DataManager.normalize_positions(self.tseries_touch_up_points)
        self.series_sampled_points = DataManager.normalize_positions(self.series_sampled_points)

    def _read_data(self):
        assert os.path.isdir(Paths.dataset_folder(self.dataset_name)), \
            "Insert the dataset \"" + self.dataset_name + "\" in: " + RES_FOLDER

        chrono = Chronom.Chrono("Reading json files...")
        observation_id = 0
        for root, dirs, files in os.walk(Paths.dataset_folder(self.dataset_name), True, None, False):
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
            self.observation_ids.append(observation_id)
            self.users_ids.append(self.get_userid(itemdata))
            self.file_names.append(json_name)
            self.file_paths.append(json_path)

            self.tseries_movement_points = self.tseries_movement_points.append(
                pd.DataFrame([{OBSERVATION_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.movement_points]),
                ignore_index=True, sort=True)

            self.tseries_touch_down_points = self.tseries_touch_down_points.append(
                pd.DataFrame([{OBSERVATION_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.touch_down_points]),
                ignore_index=True, sort=True)

            self.tseries_touch_up_points = self.tseries_touch_up_points.append(
                pd.DataFrame([{OBSERVATION_ID: observation_id,
                               TIME: point.time,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.touch_up_points]),
                ignore_index=True, sort=True)

            self.series_sampled_points = self.series_sampled_points.append(
                pd.DataFrame([{OBSERVATION_ID: observation_id,
                               COMPONENT: point.component,
                               X: point.x,
                               Y: point.y}
                              for point in itemdata.sampled_points]),
                ignore_index=True, sort=True)

    @staticmethod
    def _normalize_group(group):
        group[X] = group[X] - group[X].min()
        group[Y] = group[Y] - group[Y].min()
        return group

    @staticmethod
    def normalize_positions(tseries: pd.DataFrame):
        return tseries.groupby(OBSERVATION_ID).apply(DataManager._normalize_group)

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
        return dataframe.loc[dataframe[OBSERVATION_ID] == item_id]

    def _generate_example_charts(self):

        examples_file_names = [
            ("pesce_Flavia_ischiboni_40.json", "21.01.2019.16.12"),
            ("candela_flavia_ischiboni_10.json", "24.01.2019.10.52"),
        ]

        def get_itemdata(reqeuest) -> jw.ItemData:
            return self.json_objs[reqeuest]

        dataframe = self.tseries_movement_points
        for ex_name, ex_date in examples_file_names:
            item_id, = [i for i, x in enumerate(self.file_names) if x == ex_name and
                        get_itemdata(i).session_data.date == ex_date]

            item_data: jw.ItemData = self.json_objs[item_id]

            tseries = DataManager.get_item_tseries(dataframe, item_id)

            h = item_data.session_data.device_data.heigth_pixels
            w = item_data.session_data.device_data.width_pixels

            fname = DataVisPaths.plot2d(self.dataset_name, item_data.item, DataManager.get_userid(item_data) + "_normalized")
            tseries_visualization.TimeSeries2D(DataManager.normalize_positions(tseries), fname, height=h, width=w)

            fname = DataVisPaths.plot2d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            tseries_visualization.TimeSeries2D(tseries, fname, height=h, width=w)

            fname = DataVisPaths.gif(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            tseries_visualization.TimeSeries2DGIF(tseries, fname, height=h, width=w)

            fname = DataVisPaths.gif3d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            tseries_visualization.TimeSeries3DGIF(tseries, fname, height=h, width=w)

            fname = DataVisPaths.decomposition_gif3d(self.dataset_name, item_data.item, DataManager.get_userid(item_data))
            tseries_visualization.TimeSeriesDecomposition3DGIF(tseries, fname, height=h, width=w)


if __name__ == "__main__":
    d = DataManager(DATASET_NAME_0)
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
