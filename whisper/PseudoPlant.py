from Plant import Plant

class PseudoPlant(Plant):
    def __init__(self, display_name, name, speech_center):
        self.display_name = display_name
        self.name = name
        self.__speech_center = speech_center
        self.dry = True
        self.dark = True

    def report_wether_forecast(self, postal_code):
        return self.__speech_center.report_wether_forecast(postal_code)

    def needWater(self):
        return self.dry

    def needLuminesity(self):
        return self.dark

<<<<<<< HEAD

import SpeechCenter 

dis_name = "ダミー001"
name = "ダミー001"
kls = SpeechCenter.ExampleResponce 
center = kls()
ex = center.examples
ex["調子はどう？"] = kls.respond_health
ex["水はいる？"] = kls.respond_water_demand
ex["日当たりはどう？"] = kls.respond_light_demand
ex["気温はどう？"] = kls.respond_temperture

plant = PseudoPlant(dis_name, name, center)


=======
        
>>>>>>> Clova

    