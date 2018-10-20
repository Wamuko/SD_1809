WaterThreshold = 60
LuminosityThreshold = 900
TempertureMinRelax = 15
TempertureMaxRelax = 30


class Plant:
    def __init__(self,
                 name,
                 sensor_buffer,
                 speech_center,
                 water_threshold=WaterThreshold,
                 luminosity_threshold=LuminosityThreshold,
                 temperture_min_relax=TempertureMinRelax,
                 temperture_max_relax=TempertureMaxRelax):
        self.name = name
        self.__sensor_buf = sensor_buffer
        self.__speech_center = speech_center
        self.water_threshold = water_threshold
        self.luminosity_threshold = luminosity_threshold
        self.temperture_min_relax = temperture_min_relax
        self.temperture_max_relax = temperture_max_relax

    # Lineに出力すべきテキストを生成します
    def chat(self, text):
        return self.__speech_center.make_text(self, user_text=text)