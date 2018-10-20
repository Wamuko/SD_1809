# -*- coding: utf-8 -*-
import json
import os

DIR_DATA = "./data/user_data.json"

class UserData:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        name = os.path.normpath(os.path.join(base, DIR_DATA))
        f = open(name, 'r', encoding="utf-8")
        self.json_data = json.load(f)
        print(self.json_data)

    def plant_exists(self, plant_name):
        # jsonデータの中にいるかチェック
        return True
