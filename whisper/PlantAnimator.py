"""
植物とLine側の「電話交換手」の役割を果たします
"""


class PlantAnimator:
    def __init__(self, user_data):
        self.user_data = user_data
        self.__plant = None

    """
    要求された名前の植物
    """

    def connect(self, name):
        self.__plant = self.user_data.reanimate_plant(name)
