# -*- coding: utf-8 -*-
from UserData import UserData

data = UserData()

#print(data.plant_exists("チューリップ"))
#print("\n")
#print(data.plant_exists("チューリップちゃん"))
#print("\n")

data.add_plant("チューリップちゃん", name="チューリップ", water_threshold=700)

#print(data.json_data)
#print(data.plants)

#data.remove_plant("チューリップちゃん")

#print(data.json_data)
#print(data.plants)
print(data.json_data)
