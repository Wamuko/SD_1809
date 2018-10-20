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
        self.plants = self.json_data["plants"]

    def load(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        f = open(name, 'r', encoding="utf-8")
        data = json.load(f)
        return data

    def plant_exists(self, displayed_plant_name):
        # jsonデータの中にいるかチェック
        print(self.plants)
        return self.plants.has_key(displayed_plant_name)

    def add_plant(self, 
                    displayed_plant_name, 
                    name="", 
                    water_threshold=600,
                    luminosity_threshold=700,
                    temperture_min_relax=15,
                    temperture_max_relax=30):
        # 受け取った名前をリストに格納
        ys = cl.OrderedDict()
        obj = { 
            displayed_plant_name: {
                "name": name, 
                "water_threshold": water_threshold, 
                "luminosity_threshold": luminosity_threshold,
                "temperture_min_relax": temperture_min_relax,
                "temperture_max_relax": temperture_max_relax
            }
        }
        self.json_data["plants"].append(obj)
        ys = self.json_data
        #print(self.json_data)

        self.save_json(ys)

    def reanimate_plant(self, name):
        pass

    def remove_plant(self, displayed_plant_name):
        ys = cl.OrderedDict()
        self.json_data["plants"] = self.json_data["plants"].pop(displayed_plant_name, None)
        ys = self.json_data
        self.save_json(ys)

    def save_json(self, ys):
        # jsonに書き込み
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        fw = open(name, 'w', encoding="utf-8")
        json.dump(ys, fw, indent=4)
