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
        self.use_line_beacon = self.json_data["use_line_beacon"]
        self.plants = self.json_data["plants"]

    def load(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        f = open(name, 'r', encoding="utf-8")
        data = json.load(f)
        return data

    def plant_exists(self, displayed_plant_name):
        # jsonデータの中にいるかチェック
        return displayed_plant_name in self.plants

    def add_plant(self, 
                    displayed_plant_name, 
                    name="", 
                    water_threshold=600,
                    luminosity_threshold=700,
                    temperture_min_relax=15,
                    temperture_max_relax=30):
        # 受け取った名前をリストに格納
        ys = cl.OrderedDict()
        self.json_data["plants"][displayed_plant_name] = {
            "name": name, 
            "water_threshold": water_threshold, 
            "luminosity_threshold": luminosity_threshold,
            "temperture_min_relax": temperture_min_relax,
            "temperture_max_relax": temperture_max_relax
        }
        ys = self.json_data

        self.save_json(ys)

    def reanimate_plant(self, name):
        pass

    def remove_plant(self, displayed_plant_name):
        ys = cl.OrderedDict()
        if(displayed_plant_name in self.json_data["plants"]):
            del(self.json_data["plants"][displayed_plant_name])
        ys = self.json_data
        self.save_json(ys)

    def set_postal_code(self, postal_code):
        ys = cl.OrderedDict()
        self.json_data["postal_code"] = postal_code
        ys = self.json_data
        self.save_json(ys)

    def save_json(self, ys):
        # jsonに書き込み
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        fw = open(name, 'w', encoding="utf-8")
        json.dump(ys, fw, indent=4)
