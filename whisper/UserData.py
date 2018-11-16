# -*- coding: utf-8 -*-
import json
import os
import collections as cl
import ResponseDict
from Plant import Plant
from SpeechCenter import ExampleResponce
from SensorBuffer import SensorBuffer

DIR_DATA = "./data/user_data.json"


class UserData:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'r', encoding="utf-8") as f:
            self.json_data = json.load(f)
            self.postal_code = self.json_data["postal_code"]
            self.use_line_beacon = self.json_data["use_line_beacon"]
            self.plants = self.json_data["plants"]

    # obsolete
    def load(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'r', encoding="utf-8") as f:
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
        obj = self.json_data["plants"][displayed_plant_name] = {
            "display_name": displayed_plant_name,
            "name": name,
            "water_threshold": water_threshold,
            "luminosity_threshold": luminosity_threshold,
            "temperture_min_relax": temperture_min_relax,
            "temperture_max_relax": temperture_max_relax
        }
        ys = self.json_data
        # print(self.json_data)

        self.save_json(ys)
        return self.__create_plant(obj)

    def reanimate_plant(self, display_name):
        if self.plant_exists(display_name):
            return self.__create_plant(self.json_data["plants"][display_name])
        else:
            return None

    def remove_plant(self, displayed_plant_name):
        ys = cl.OrderedDict()
        if (displayed_plant_name in self.json_data["plants"]):
            del (self.json_data["plants"][displayed_plant_name])
        ys = self.json_data
        self.save_json(ys)

    def set_postal_code(self, postal_code):
        ys = cl.OrderedDict()
        self.json_data["postal_code"] = postal_code
        ys = self.json_data
        self.save_json(ys)

    def set_use_line_beacon(self, use_line_beacon):
        ys = cl.OrderedDict()
        self.json_data["use_line_beacon"] = use_line_beacon
        ys = self.json_data
        self.save_json(ys)

    def set_user_id(self, user_id):
        ys = cl.OrderedDict()
        self.json_data["user_id"] = user_id
        ys =self.json_data
        self.save_json(ys)

    def save_json(self, ys):
        # jsonに書き込み
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        with open(name, 'w', encoding="utf-8") as fw:
            json.dump(ys, fw, indent=4)

    def list_plant_name(self):
        return tuple(self.plants.keys())

        
    def __create_plant(self, json_object):
        kls = ExampleResponce
        center = ExampleResponce()
        ex = center.examples
        ex["調子はどう？"] = kls.respond_health
        ex["水はいる？"] = kls.respond_water_demand
        ex["日当たりはどう？"] = kls.respond_light_demand

        # ex["気温はどう？"] = kls.respond_temperture

        res = Plant(json_object["name"], json_object["display_name"],
                    SensorBuffer(), center, json_object["water_threshold"],
                    json_object["luminosity_threshold"],
                    json_object["temperture_min_relax"],
                    json_object["temperture_max_relax"])

        return res


if __name__ == "__main__":
    ud = UserData()
    print(ud.plant_exists("チューリップちゃん"))
    print(ud.reanimate_plant("チューリップちゃん"))

    print(ud.reanimate_plant("チューリップちゃ"))
