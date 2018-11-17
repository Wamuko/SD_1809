import Sensor

WaterThreshold = 60
LuminosityThreshold = 900
TempertureMinRelax = 15
TempertureMaxRelax = 30


class Plant:
    def __init__(
            self,
            display_name,
            name,
            sensor_buffer,
            speech_center,
            water_threshold=WaterThreshold,
            luminosity_threshold=LuminosityThreshold,
            temperture_min_relax=TempertureMinRelax,
            temperture_max_relax=TempertureMaxRelax,
    ):
        self.display_name = display_name
        self.name = name
        self.__sensor_buf = sensor_buffer
        self.__speech_center = speech_center
        self.water_threshold = water_threshold
        self.luminosity_threshold = luminosity_threshold
        self.temperture_min_relax = temperture_min_relax
        self.temperture_max_relax = temperture_max_relax
        self.push_message = None

        self.__sensor_buf.start(Sensor.loop)

    def update(self):
        return None

    # Lineに出力すべきテキストを生成します
    def chat(self, text):
        return self.__speech_center.make_response(self, user_text=text)

    # 初回生成時の挨拶を返します
    def say_nice_to_meet_you(self):
        return self.__speech_center.say_nice_to_meet_you(self)

    # 呼び出し時の挨拶を生成します
    def say_hello(self):
        return self.__speech_center.say_hello(self)

    # 別れの挨拶を生成します
    def say_see_you(self):
        return self.__speech_center.respond_see_you(self)

    # 天気予報のメッセージをプッシュします
    def report_weather_forecast(self, postal_code):
        self.push_message(
            self.__speech_center.report_weather_forecast(postal_code))


    def sense_condition(self):
        """新しいセンサ値を取得します"""
        self.__sensor_buf.get_current_condition()

    def needWater(self):
        hum, _ = self.__sensor_buf.get_current_condition(False)
        print("hum %d" % hum)
        return hum >= self.water_threshold

    def needLuminesity(self):
        _, lum = self.__sensor_buf.get_current_condition(False)
        print("lum %d" % lum)
        return lum < self.luminosity_threshold

    # センサーバッファのfetchspanを書き換えます
    def set_beacon_buf_span(self, check_beacon_eco_time):
        if check_beacon_eco_time:
            self.__sensor_buf.fetch_span = self.__sensor_buf.ECO_FETCH_SPAN
        else:
            self.__sensor_buf.fetch_span = self.__sensor_buf.DEFAULT_FETCH_SPAN
