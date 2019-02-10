# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np

import src.utility.chronometer as Chronom
import src.data.json_wrapper as jw
from src.constants.io_constants import RES_FOLDER, JSON_EXTENSION

from src.constants.paths_generator import DataVisPaths, Paths
from src.constants.literals import *
from src.visualization import tseries_visualization
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

        assert (len(self.json_objs) == len(self.file_names) == len(self.file_paths) == len(self.users_ids)
                == len(self.observation_ids) == len(self.items))

        self.generate_example_charts(dataset_name)

        self.tseries_movement_points = DataManager.normalize_positions(self.tseries_movement_points)
        self.tseries_touch_down_points = DataManager.normalize_positions(self.tseries_touch_down_points)
        self.tseries_touch_up_points = DataManager.normalize_positions(self.tseries_touch_up_points)
        self.series_sampled_points = DataManager.normalize_positions(self.series_sampled_points)

        self.tseries_movement_points = DataManager.normalize_dimensions(self.tseries_movement_points)
        self.tseries_touch_down_points = DataManager.normalize_dimensions(self.tseries_touch_down_points)
        self.tseries_touch_up_points = DataManager.normalize_dimensions(self.tseries_touch_up_points)
        self.series_sampled_points = DataManager.normalize_dimensions(self.series_sampled_points)

    def _read_data(self):
        assert os.path.isdir(Paths.dataset_folder(self.dataset_name)), "Insert the dataset \"" + self.dataset_name + "\" in: " + RES_FOLDER

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
    def _normalize_positions_group(group):
        group[X] = group[X] - group[X].min()
        group[Y] = group[Y] - group[Y].min()
        return group

    @staticmethod
    def normalize_positions(tseries: pd.DataFrame):
        return tseries.groupby(OBSERVATION_ID).apply(DataManager._normalize_positions_group)

    @staticmethod
    def _normalize_dimensions_group(group):
        group[X] = (group[X] - group[X].min()) / (group[X].max() - group[X].min())
        group[Y] = (group[Y] - group[Y].min()) / (group[Y].max() - group[Y].min())
        return group

    @staticmethod
    def normalize_dimensions(tseries: pd.DataFrame):
        return tseries.groupby(OBSERVATION_ID).apply(DataManager._normalize_dimensions_group)

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

    def generate_example_charts(self, dataset_name):

        examples_file_names = {DATASET_NAME_0: [
            ("pesce_Flavia_ischiboni_40.json", "21.01.2019.16.12"),
            ("candela_flavia_ischiboni_10.json", "24.01.2019.10.52"),
            ("balena_Federica_Spini_64.json", "24.01.2019.14.44"),
            ("barca_Federica_Spini_126.json", "25.01.2019.19.14"),
            ("busta_Federica_Spini_189.json", "25.01.2019.19.14"),
            ("busta_Matteo_Prata_6.json", "24.01.2019.15.20"),
            ("cacciavite_Federica_Spini_68.json", "24.01.2019.14.44"),
            ("sole_Irene_Tallini_53.json", "23.01.2019.13.12"),
            ("coccodrillo_giordano_ischiboni_15.json", "26.01.2019.17.36"),
            ("teschio_giordano_ischiboni_58.json", "26.01.2019.17.36"),
            ("uva_Federica_spini_121.json", "27.01.2019.23.30"),
            ("lampadina_Federica_spini_272.json", "27.01.2019.23.30"),
            ("nuvola_Luca_Moschella_36.json", "23.01.2019.09.57"),
            ("gatto_Luca_Moschella_25.json", "23.01.2019.09.57"),
            ("libro_Federica_spini_213.json", "27.01.2019.23.30"),
            ("libro_Federica_spini_274.json", "27.01.2019.23.30"),
            ("cigno_federica_spini_14.json", "22.01.2019.17.42"),
            ("chitarra_Federica_Spini_74.json", "24.01.2019.14.44"),
            ("pipistrello_Federica_Spini_225.json", "25.01.2019.19.14"),

        ],
        DATASET_NAME_2:
        [
            ("0_Luca_Moschella_40.json", "28.01.2019.11.46"),
            ("1_Federica_spini_41.json", "10.02.2019.11.14"),
            ("1_Federica_Spini_61.json", "28.01.2019.12.17"),
            ("2_Federica_Spini_72.json", "28.01.2019.12.29"),
            ("3_Federica_Spini_3.json", "28.01.2019.10.40"),
            ("4_Federica_Spini_194.json", "28.01.2019.12.29"),
            ("5_Federica_Spini_15.json", "28.01.2019.12.29"),
            ("5_Flavia_Ischiboni_35.json", "28.01.2019.15.38"),
            ("6_Luca_Moschella_36.json", "28.01.2019.12.08"),
            ("7_Luca_Moschella_27.json", "28.01.2019.11.44"),
            ("8_Luca_Moschella_48.json", "28.01.2019.12.22"),
            ("9_Federica_Spini_9.json", "28.01.2019.11.50")
        ]}

        fps_dataset = {
            DATASET_NAME_0: 60,
            DATASET_NAME_2: 20
        }

        assert dataset_name in examples_file_names

        def get_itemdata(reqeuest) -> jw.ItemData:
            return self.json_objs[reqeuest]

        dataframe = self.tseries_movement_points
        for ex_name, ex_date in examples_file_names[dataset_name]:
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
            tseries_visualization.TimeSeriesDecomposition3DGIF(tseries, fname, height=h, width=w, fps=fps_dataset[dataset_name])


if __name__ == "__main__":
    for x in [DATASET_NAME_0, DATASET_NAME_2]:
        DataManager(x)

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

    # pd.options.display.max_rows = 10000
    # print(d.tseries_movement_points)
    # print("Number of items: {}".format(len(d.items)))

