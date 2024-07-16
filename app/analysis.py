class ImgAnalysis:
    def __init__(self, img):
        self.img = img

    def __call__(self, *args, **kwargs):
        i = self.img
        return "Nice IMG"
