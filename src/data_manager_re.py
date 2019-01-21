# -*- coding: utf-8 -*-
import json
import random
import pandas as pd

import src.chronometer as Chronom
import src.plotter as Plot
import src.utils as Utils
import src.json_wrapper as jw

FILE_BLACK_LIST = [Utils.CONFIGURATION_FILE]

class DataManager:
    @staticmethod
    def get_userid(item_data: jw.ItemData):
        return "{}_{}_{}_{}".format(
                                    item_data.item,
                                    item_data.session_data.name,
                                    item_data.session_data.surname,
                                    item_data.session_data.date)

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
            columns=[Utils.ITEM_ID,
                     Utils.TIME,
                     Utils.COMPONENT,
                     Utils.X,
                     Utils.Y])

        self.tseries_touch_up_points = pd.DataFrame(
            columns=[Utils.ITEM_ID,
                     Utils.TIME,
                     Utils.COMPONENT,
                     Utils.X,
                     Utils.Y])

        self.tseries_touch_down_points = pd.DataFrame(
            columns=[Utils.ITEM_ID,
                     Utils.TIME,
                     Utils.COMPONENT,
                     Utils.X,
                     Utils.Y])

        self.series_sampled_points = pd.DataFrame(
            columns=[Utils.ITEM_ID,
                     Utils.COMPONENT,
                     Utils.X,
                     Utils.Y])

        self._read_data()
        self._generate_example_charts()
        self.shift_offsets = {}

        # print(self.tseries_touch_down_points)
        # print(self.tseries_touch_up_points)
        # print(self.tseries_movement_points)
        # print(self.series_sampled_points)
        # {word_id: (minX, minY) }

    def _read_data(self):
        assert Utils.os.path.isdir(Utils.BUILD_DATASET_FOLDER(
            self.dataset_name)), "Insert the dataset \"" + self.dataset_name + "\" in: " + Utils.BASE_FOLDER

        chrono = Chronom.Chrono("Reading json files...")
        observation_id = 0
        for root, dirs, files in Utils.os.walk(Utils.BUILD_DATASET_FOLDER(self.dataset_name), True, None, False):
            for json_file in sorted(files, key=Utils.natural_keys):
                if (json_file and json_file.endswith(Utils.JSON_EXTENSION)
                        and json_file not in FILE_BLACK_LIST):
                    json_path = Utils.os.path.realpath(Utils.os.path.join(root, json_file))
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
                pd.DataFrame([{Utils.ITEM_ID: observation_id,
                               Utils.TIME: point.time,
                               Utils.COMPONENT: point.component,
                               Utils.X: point.x,
                               Utils.Y: point.y}
                              for point in itemdata.movement_points]),
                ignore_index=True)

            self.tseries_touch_down_points = self.tseries_touch_down_points.append(
                pd.DataFrame([{Utils.ITEM_ID: observation_id,
                               Utils.TIME: point.time,
                               Utils.COMPONENT: point.component,
                               Utils.X: point.x,
                               Utils.Y: point.y}
                              for point in itemdata.touch_down_points]),
                ignore_index=True)

            self.tseries_touch_up_points = self.tseries_touch_up_points.append(
                pd.DataFrame([{Utils.ITEM_ID: observation_id,
                               Utils.TIME: point.time,
                               Utils.COMPONENT: point.component,
                               Utils.X: point.x,
                               Utils.Y: point.y}
                              for point in itemdata.touch_up_points]),
                ignore_index=True)

            self.series_sampled_points = self.series_sampled_points.append(
                pd.DataFrame([{Utils.ITEM_ID: observation_id,
                               Utils.COMPONENT: point.component,
                               Utils.X: point.x,
                               Utils.Y: point.y}
                              for point in itemdata.sampled_points]),
                ignore_index=True)

    # def _group_compute_offsets(self, group):
    #     minX = group[Utils.X].min()
    #     minY = group[Utils.Y].min()
    #     self.shift_offsets[group[Utils.ITEM_ID].iloc[0]] = (minX, minY)
    #
    # def _group_shift_x(self, group):
    #     m = self.shift_offsets[group[Utils.ITEM_ID].iloc[0]][0]
    #     group[Utils.X] = group[Utils.X] - m
    #     return group
    #
    # def _group_shift_y(self, group):
    #     m = self.shift_offsets[group[Utils.ITEM_ID].iloc[0]][1]
    #     group[Utils.Y] = group[Utils.Y] - m
    #     return group
    #
    # def _group_shift_xy(self, group):
    #     return self._group_shift_x(self._group_shift_y(group))
    #
    # def _shift(self):
    #     chrono = Chronom.Chrono("Shifting dataframes...")
    #     self.data_frames[Utils.MOVEMENT_POINTS].groupby(Utils.ITEM_ID).apply(self._group_compute_offsets)
    #
    #     f = {Utils.X: self._group_shift_x,
    #          Utils.Y: self._group_shift_y,
    #          Utils.XY: self._group_shift_xy}
    #
    #     for l in Utils.INITIAL_POINTS_SERIES_TYPE:
    #         for dir in [Utils.X, Utils.Y, Utils.XY]:
    #             self.data_frames[Utils.GET_SHIFTED_POINTS_NAME(dir, l)] = self.data_frames[l].groupby(Utils.ITEM_ID).apply(f[dir])
    #     chrono.millis()

    def _generate_example_charts(self):
        examples = [
            # "aereo_b_a_0.json",
            "aereo_a_a_0.json"
        ]
        dataframe = self.tseries_movement_points
        for ex in examples:
            item_id = self.files_name.index(ex)
            Plot.GifCreator(self.dataset_name, self.users_ids[item_id], dataframe, self.json_objs[item_id], item_id, self.items[item_id], self.users_ids[item_id])
            # p = Plot.ChartCreator(Utils.DATASET_NAME_0, dataframes, dataframes[Utils.WORDID_USERID], dataframes[Utils.USERID_USERDATA], name=ex.get(Utils.NAME), surname=ex.get(Utils.SURNAME), word_number=ex.get(Utils.ITEM_INDEX))
            # p.plot2dataframe()
            # p.plot3dataframe()
            # Plot.ChartCreator(Utils.DATASET_NAME_0, dataframes, dataframes[Utils.WORDID_USERID], dataframes[Utils.USERID_USERDATA], name=ex.get(Utils.NAME), surname=ex.get(Utils.SURNAME), word_number=ex.get(Utils.ITEM_INDEX),
            #                   label=Utils.XY_SHIFTED_MOVEMENT_POINTS).plot2dataframe()


if __name__ == "__main__":
    d = DataManager(Utils.DATASET_NAME_0, update_data=False)

    # a = Utils.get_wordidfrom_wordnumber_name_surname(d[Utils.WORDID_USERID], d[Utils.USERID_USERDATA], "Rita", "Battilocchi" , Utils.BLOCK_LETTER, 31)
    # print(Utils.get_infos(d[Utils.WORDID_USERID], d[Utils.USERID_USERDATA], a))
    # d._generate_example_charts()

    # import src.json_wrapper as jw
    # j = "../res/TouchRecorder/aereo/luca_moschella_21.01.2019.10.51/aereo_Luca_Moschella_0.json"
    # with open(j, 'r') as f:
    #     s = jw.itemdata_from_dict(json.load(f))
    #     s.sampled_points
    #     print(s)
    # tseries_movement_points = pd.DataFrame(columns=[Utils.ITEM_ID,
    #                                                 Utils.TIME,
    #                                                 Utils.COMPONENT,
    #                                                 Utils.X,
    #                                                 Utils.Y])
