import random
import torch
import torch.nn as nn
from PIL import Image, ImageOps, ImageFilter
import torchvision.transforms as transforms


class ToGrayscaleAndEdgeDetection:
    def __call__(self, img):
        # Преобразование в одноканальный формат (черно-белый)
        img = img.convert("L")
        # Выделение краёв
        img = img.filter(ImageFilter.FIND_EDGES)
        return img


class ImgAnalysis:
    def __init__(self, img):
        self.img = img
        self.model0 = self.load_model()
        self.model1 = self.load_model()
        self.model2 = self.load_model()
        self.result = self.predict()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self):
        print(self.device)

        model = torch.hub.load('pytorch/vision:v0.10.0', 'efficentnet_b7', pretrained=True)

        # Заменяем первый сверточный слой conv1
        # Ожидаем один входной канал (черно-белое изображение)
        pretrained_conv1 = model.conv1.weight.data
        new_conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        with torch.no_grad():
            new_conv1.weight.data = pretrained_conv1.mean(dim=1, keepdim=True)
        model.conv1 = new_conv1

        # Заменяем последний fully connected слой
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 2)  # 2 классов для MNIST
        model.to(self.device)
        return model

    def predict_image(self, image_path, model, size):
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize(size),
            ToGrayscaleAndEdgeDetection(),  # Преобразование в одноканальный формат и выделение краёв
            transforms.ToTensor()
        ])

        image = Image.open(image_path)  # Преобразование в черно-белое изображение

        # Преобразование изображения в тензор и нормализация
        image_tensor = transform(image).unsqueeze(0)  # Добавляем батч размерности
        image_tensor = image_tensor.to(self.device)  # Перемещение тензора на тот же девайс, что и модель
        image_pil = transforms.ToPILImage()(image_tensor.squeeze(0).cpu())

        # Предсказание модели
        with torch.no_grad():
            output = model(image_tensor)
            _, predicted = torch.max(output.data, 1)
        return predicted.item(), image_pil

    def predict(self, image):
        one, transformed_image = predict_image(image, self.model0)
        two, _ = predict_image(image, self.model1)
        three, _ = predict_image(image, self.model2)

        if one:
            one_1 = 'бейнит'
            if two or three:
                one_1 += ', '
        else:
            one_1 = ''
        if two:
            two_1 = 'перлит'
            if three:
                two_1 += ', '
        else:
            two_1 = ''
        if three == 1:
            three_1 = 'мартенсит'
        else:
            three_1 = ''
        if not one and not two and not three:
            one_1 = 'Не найдена ни одна из структур'

        return f"{one_1}{two_1}{three_1}"

    def __call__(self, *args, **kwargs):
        i = self.img
        return self.result
