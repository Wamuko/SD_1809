from Plant import Plant

class PseudoPlant(Plant):
    def __init__(self, display_name, name, speech_center):
        self.display_name = display_name
        self.name = name
        self.__speech_center = speech_center
        self.dry = True
        self.bright = True

    def report_wether_forecast(self, postal_code):
        return self.__speech_center.report_wether_forecast(postal_code)

    

    