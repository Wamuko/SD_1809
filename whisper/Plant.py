from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
            listen_beacon=(None, 0),
    ):
        self.display_name = display_name
        self.name = name
        self.__sensor_buf = sensor_buffer
        self.__speech_center = speech_center
        self.water_threshold = water_threshold
        self.luminosity_threshold = luminosity_threshold
        self.temperture_min_relax = temperture_min_relax
        self.temperture_max_relax = temperture_max_relax
        self.listen_beacon = listen_beacon
        self.push_message = None

        executor = ThreadPoolExecutor(2)
        self.__listening_thread = executor.submit(self.__sensor_buf.start)

    def update(self):
        return None

    # Lineに出力すべきテキストを生成します
    def chat(self, text):
        return self.__speech_center.make_response(self, user_text=text)

    # 天気予報のメッセージをプッシュします
    def report_weather_forecast(self, postal_code):
        self.push_message(
            self.__speech_center.report_weather_forecast(postal_code))

    def needWater(self):
        return self.__sensor_buf.get_humidity() >= 800

    def needLuminesity(self):
        return self.__sensor_buf.get_luminosity() < 750

    # センサーバッファのfetchspanを書き換えます
    def set_beacon_buf_span(self, now):
        if 14401 < (int(datetime.now().strftime('%s')) - self.listen_beacon[0]
                    ) and self.listen_beacon[1] is 1:
            self.__sensor_buf.fetch_span = self.__sensor_buf.ECO_FETCH_SPAN
        else:
            self.__sensor_buf.fetch_span = self.__sensor_buf.DEFAULT_FETCH_SPAN

