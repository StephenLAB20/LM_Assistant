import asyncio
import numpy as np
from PIL import Image
import cv2
import io
import os


class Construction:
    def __init__(self, device, count):
        self.image_folder = 'img/construction'
        self.image_info = {}
        self.device = device
        self.count = count
        self.delay = 1
        self.load_images()
        self.process_help_command_task = None

    def load_images(self):
        for filename in os.listdir(self.image_folder):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                template_path = os.path.join(self.image_folder, filename)

                # Загрузка шаблона
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                # Рассчитывание и установка координат
                # coord = self.calculate_coordinates(image_name)

                # Добавление в словарь
                self.image_info[image_name] = {'template': template, 'coord': None}

    # TODO
    async def screenshot(self, l_button_coord, r_button_coord):
        await asyncio.sleep(1)
        result = await self.device.screencap()

        im = Image.open(io.BytesIO(result))
        # im.show()

        rgb_im = im.convert("RGB")
        rgb_l_button = rgb_im.getpixel(l_button_coord)
        rgb_r_button = rgb_im.getpixel(r_button_coord)

        print(self.device.serial, "New screenshot made!")
        return rgb_l_button, rgb_r_button

    async def check_equipment(self):
        await self.click_loupe_icon()
        await self.click_farm_icon()
        await self.click_primary_upgrade_btn()
        is_equipped = await self.check_warning_icon()
        return is_equipped

    async def apply_equipment(self):
        await self.click_warning_icon()
        await self.click_warning_change_btn()
        await self.click_construction_equip_btn()

    async def process_help_command(self):
        print(f"Starting checking equipment for {self.device.serial}")
        is_equipped = await self.check_equipment()

        if not is_equipped:
            await self.apply_equipment()
        else:
            await self.execute_help_command()

    async def click_loupe_icon(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон loupe из словаря
        template = self.image_info['loupe_icon']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['loupe_icon']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('loupe_icon', loc, template, im_array)
                self.image_info['loupe_icon']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_farm_icon(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['farm_icon']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['farm_icon']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('farm_icon', loc, template, im_array)
                self.image_info['farm_icon']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_primary_upgrade_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['primary_upgrade_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['primary_upgrade_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('primary_upgrade_btn', loc, template, im_array)
                self.image_info['primary_upgrade_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def check_warning_icon(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['warning_icon']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['warning_icon']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('warning_icon', loc, template, im_array)
                self.image_info['warning_icon']['coord'] = coord
            return False
        else:
            return True

    async def click_warning_icon(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['warning_icon']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['warning_icon']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('warning_icon', loc, template, im_array)
                self.image_info['warning_icon']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_warning_change_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['warning_change_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['warning_change_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('warning_change_btn', loc, template, im_array)
                self.image_info['warning_change_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_construction_equip_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['construction_equip_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['construction_equip_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('construction_equip_btn', loc, template, im_array)
                # Добавляем 500 к x-координате, так как шаблон взят левее самой кнопки (кнопка мигает, изменяет цвет)
                coord = (coord[0] + 500, coord[1])
                self.image_info['construction_equip_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_secondary_upgrade_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['secondary_upgrade_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['secondary_upgrade_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('secondary_upgrade_btn', loc, template, im_array)
                self.image_info['secondary_upgrade_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_help_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['help_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['help_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('help_btn', loc, template, im_array)
                self.image_info['help_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_cancel_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['cancel_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['cancel_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('cancel_btn', loc, template, im_array)
                self.image_info['cancel_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_confirm_cancel_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон из словаря
        template = self.image_info['confirm_cancel_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['confirm_cancel_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('confirm_cancel_btn', loc, template, im_array)
                self.image_info['confirm_cancel_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def click_exit_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон loupe из словаря
        template = self.image_info['exit_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['exit_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('exit_btn', loc, template, im_array)
                self.image_info['exit_btn']['coord'] = coord

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")

    async def check_exit_btn(self):
        await asyncio.sleep(self.delay)
        # Получаем скриншот от устройства
        result = await self.device.screencap()

        # Преобразуем скриншот в нужный формат
        im = Image.open(io.BytesIO(result))
        im_array = np.array(im)
        im_gray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)

        # Берем шаблон loupe из словаря
        template = self.image_info['exit_btn']['template']

        # Ищем шаблон на скриншоте
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

        # Установка порога для совпадения
        threshold = 0.8
        loc = np.where(res >= threshold)

        # Если есть хотя бы одно совпадение
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = self.image_info['exit_btn']['coord']

            # Если координаты отсутствуют, получаем их и сохраняем в словарь
            if coord is None:
                coord = await self.get_coords('exit_btn', loc, template, im_array)
                self.image_info['exit_btn']['coord'] = coord
                return False
        else:
            return True

    async def click_twice_exit_btn(self):
        while not await self.check_exit_btn():
            await asyncio.sleep(self.delay)
            await self.click_exit_btn()
            # await asyncio.sleep(1)  # Пауза между повторными нажатиями

    async def get_coords(self, image_name, loc, template, im_array):
        # Отмечаем совпадающую область на изображении (можно убрать в боевом коде)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(im_array, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

        # Получение координат центра первого совпадения
        first_match_center = (int(loc[1][0] + template.shape[1] / 2), int(loc[0][0] + template.shape[0] / 2))
        # print(f"Center coordinates of the first match for {image_name}:", first_match_center)
        return first_match_center

    async def execute_help_command(self):
        print(f"Executing help command for device {self.device.serial}...")

        for i in range(self.count + 1):
            print(f"Executing help command for device {self.device.serial}..........{i}")
            await self.click_secondary_upgrade_btn()
            await self.click_help_btn()
            await self.click_cancel_btn()
            await self.click_confirm_cancel_btn()

            # await asyncio.sleep(0)
        await self.click_twice_exit_btn()
        # await asyncio.sleep(0)

    async def start(self):
        self.process_help_command_task = await asyncio.create_task(self.process_help_command())
        return self.process_help_command_task

    async def stop(self):
        if self.process_help_command_task:
            self.process_help_command_task.cancel()
            await asyncio.gather(self.process_help_command_task, return_exceptions=True)
