"""
植物とLine側の「電話交換手」の役割を果たします
また、そのほかのシステム的な機能を担います
"""


class PlantAnimator:
    def __init__(self, user_data):
        self.user_data = user_data
        self.__plant = None

    def register_plant(self, ):
        self.__plant = self.user_data.add_plant()

    def delete_plant(self, display_name):
        if self.__plant.display_name == display_name:
            self.disconnect()
        self.user_data.remove_plant(display_name)

    # 要求された名前から対応する植物を再生します
    def connect(self, name):
        self.__plant = self.user_data.reanimate_plant(name)

    # 植物との接続を切断します
    def disconnect(self):
        self.__plant = None

    # 植物と接続しているか確認します
    def connecting(self):
        return self.__plant is None

    # Lineのテキストを植物に伝え、応答を受け取ります
    def communicate(self, text):
        return self.__plant.chat(text)

    # 植物の状態の更新をします
    def update(self):
        self.__plant.update()
