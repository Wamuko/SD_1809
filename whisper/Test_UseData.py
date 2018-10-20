# -*- coding: utf-8 -*-
from UserData import UserData

data = UserData()

print(data.json_data)
print(data.plant_exists("チューリップ"))
print("\n")
print(data.plant_exists("hoge"))
print("\n")

data.add_plant("花たち")

print(data.json_data)
print(data.plant_names)

data.remove_plant("たんぽぽ")

print(data.json_data)
print(data.plant_names)
