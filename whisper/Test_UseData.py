# -*- coding: utf-8 -*-
from UserData import UserData

data = UserData()

print(data.json_data)
print(data.plant_exists("チューリップ"))
print("\n")
print(data.plant_exists("チューリップちゃん"))
print("\n")

data.add_plant("たんぽぽ")

print(data.json_data)
print(data.plants)

data.remove_plant("たんぽぽ")

print(data.json_data)
print(data.plants)
