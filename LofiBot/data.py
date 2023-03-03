import os


class DataManager:
    def __init__(self):
        self.ids = set(os.listdir("../ressources"))
