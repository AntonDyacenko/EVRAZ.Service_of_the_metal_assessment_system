import random


class ImgAnalysis:
    def __init__(self, img):
        self.img = img
        self.model0 = self.load_model()
        self.model1 = self.load_model()
        self.model2 = self.load_model()
        self.result = self.predict()

    def load_model(self):
        return random.randint(0, 1)

    def predict(self):
        return f"model0: {self.model0}, model1: {self.model1}, model2: {self.model2}"

    def __call__(self, *args, **kwargs):
        i = self.img
        return self.result
