# -*- coding: utf-8 -*-
import json
import os
import collections as cl

DIR_DATA = "./data/user_data.json"


class UserData:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        f = open(name, 'r', encoding="utf-8")
        self.json_data = json.load(f)
        self.postal_code = self.json_data["postal_code"]
        self.plant_names = self.json_data["plant_names"]

    def load(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        f = open(name, 'r', encoding="utf-8")
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
        #print(self.json_data)

        self.save_json(ys)

    def reanimate_plant(self, name):
        pass

    def remove_plant(self, plant_name):
        ys = cl.OrderedDict()
        self.json_data["plant_names"].remove(plant_name)
        ys = self.json_data
        self.save_json(ys)

    def save_json(self, ys):
        # jsonに書き込み
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        fw = open(name, 'w', encoding="utf-8")
        json.dump(ys, fw, indent=4)
