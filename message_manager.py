import asyncio
import io
import numpy as np
import cv2
import os
from PIL import Image
from enum import Enum


class MessageType(Enum):
    START = "OK! Please press help. Starting in few seconds..."
    FINISH = "If you need more, please ask me for help again."


class MessageManager:
    def __init__(self, device):
        self.image_folder = 'img/message_manager'
        self.image_info = {}
        self.device = device
        self.delay = 0.8
        self.load_images()

    def load_images(self):
        for filename in os.listdir(self.image_folder):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                template_path = os.path.join(self.image_folder, filename)

                # Преобразование шаблона в ч\б
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                # Добавление в словарь
                self.image_info[image_name] = {'template': template, 'coord': None}

    async def send_message(self, message_type):
        await self.click_chat_box()
        await self.click_text_input()

        message_text = message_type.value

        await self.device.shell('input text "{}"'.format(message_text))
        await self.click_ok_btn()
        await self.click_send_btn()
        await self.click_exit_btn()

    async def click_chat_box(self):
        await asyncio.sleep(self.delay)
        coord = 600, 30
        await self.device.shell(f"input tap {coord[0]} {coord[1]}")
        print(f"chat_box CLICKED {self.device.serial}")

    async def click_text_input(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'text_input'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        # Получаем скриншот от устройства
        screenshot = await self.device.screencap()

        # Ищем шаблон на скриншоте и возвращаем количество совпадений
        loc = await self.get_template_match_locations(screenshot, template)

        # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = await self.get_coord(template_name, template, loc, btn_offset)

            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"text_input CLICKED {self.device.serial}")
        else:
            print(f"text_input MISMATCH {self.device.serial}")

    async def click_ok_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'ok_btn'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        # Получаем скриншот от устройства
        screenshot = await self.device.screencap()

        # Ищем шаблон на скриншоте и возвращаем количество совпадений
        loc = await self.get_template_match_locations(screenshot, template)

        # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = await self.get_coord(template_name, template, loc, btn_offset)

            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"ok_btn CLICKED {self.device.serial}")
        else:
            print(f"ok_btn MISMATCH {self.device.serial}")

    async def click_send_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'send_btn'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        # Получаем скриншот от устройства
        screenshot = await self.device.screencap()

        # Ищем шаблон на скриншоте и возвращаем количество совпадений
        loc = await self.get_template_match_locations(screenshot, template)

        # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = await self.get_coord(template_name, template, loc, btn_offset)

            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"send_btn CLICKED {self.device.serial}")
        else:
            print(f"send_btn MISMATCH {self.device.serial}")

    async def click_exit_btn(self):
        await asyncio.sleep(self.delay)
        is_clicked = False
        # Имя шаблона в папке шаблонов
        template_name = 'exit_btn'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        while not is_clicked:
            # Получаем скриншот от устройства
            screenshot = await self.device.screencap()

            # Ищем шаблон на скриншоте и возвращаем количество совпадений
            loc = await self.get_template_match_locations(screenshot, template)

            # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
            if loc[0].size > 0:
                # Берем координаты из словаря, если они есть
                coord = await self.get_coord(template_name, template, loc, btn_offset)

                await self.device.shell(f"input tap {coord[0]} {coord[1]}")
                is_clicked = True
                print(f"exit_btn CLICKED {self.device.serial}")
            else:
                print(f"exit_btn MISMATCH {self.device.serial}")

    async def get_template_match_locations(self, screenshot, template):
        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(screenshot))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)
        return loc

    async def get_coord(self, template_name, template, loc, btn_offset):
        coord = self.image_info[template_name]['coord']

        # Если координаты отсутствуют, получаем их и сохраняем в словарь
        if coord is None:
            coord = await self.calculate_coord(loc, template)
            # Добавляем отступы к координатам, если нажимать нужно левее\правее шаблона
            coord = (coord[0] + btn_offset[0], coord[1] + btn_offset[1])
            self.image_info[template_name]['coord'] = coord
        return coord

    async def calculate_coord(self, loc, template):
        # Отмечаем совпадающую область на изображении (можно убрать в боевом коде)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(im_array, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

        # Получение координат центра первого совпадения
        first_match_center = (int(loc[1][0] + template.shape[1] / 2), int(loc[0][0] + template.shape[0] / 2))
        # print(f"Center coordinates of the first match for {image_name}:", first_match_center)
        return first_match_center
