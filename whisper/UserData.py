# -*- coding: utf-8 -*-
import json
import os
import collections as cl
from Plant import Plant
from SpeechCenter import ExampleResponce

DIR_DATA = "./data/user_data.json"


class UserData:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'r', encoding="utf-8") as f:
            self.json_data = json.load(f)
            self.postal_code = self.json_data["postal_code"]
            self.plant_names = self.json_data["plant_names"]

    def load(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'r', encoding="utf-8") as f:
            data = json.load(f)

        return data

    def plant_exists(self, plant_name):
        # jsonデータの中にいるかチェック
        return plant_name in self.plant_names

    def add_plant(self, plant_name):
        # 受け取った名前をリストに格納
        ys = cl.OrderedDict()
        self.json_data["plant_names"].append(plant_name)
        ys = self.json_data
        # print(self.json_data)

        self.save_json(ys)
        return self.__create_plant()

    def reanimate_plant(self, name):
        return self.__create_plant(self.json_data["plants"][name])

    def remove_plant(self, plant_name):
        ys = cl.OrderedDict()
        self.json_data["plant_names"].remove(plant_name)
        ys = self.json_data
        self.save_json(ys)

    def save_json(self, ys):
        # jsonに書き込み
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'w', encoding="utf-8") as fw:
            json.dump(ys, fw, indent=4)

    def __create_plant(self, json_object):
        kls = ExampleResponce
        center = ExampleResponce()
        ex = center.examples
        ex["調子はどう？"] = kls.respond_health
        ex["水はいる？"] = kls.respond_water_demand
        ex["日当たりはどう？"] = kls.respond_light_demand
        ex["気温はどう？"] = kls.respond_temperture

        res = Plant(json_object["name"], None, ex,
                    json_object["water_threshold"],
                    json_object["luminosity_threshold"],
                    json_object["temperture_min_relax"],
                    json_object["temperture_max_relax"])

        return res
