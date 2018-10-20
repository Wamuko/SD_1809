# -*- coding: utf-8 -*-
from UserData import UserData

data = UserData()

#print(data.plant_exists("チューリップ"))
#print("\n")
#print(data.plant_exists("チューリップちゃん"))
#print("\n")
print(data.json_data)

data.add_plant("たんぽぽマン", name="たんぽぽ", water_threshold=650)

print(data.json_data)

#print(data.json_data)
#print(data.plants)

#data.remove_plant("チューリップちゃん")

#print(data.json_data)
#print(data.plants)
#print(data.json_data)
