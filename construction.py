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
        self.delay = 0.8
        self.load_images()
        self.process_help_command_task = None

    def load_images(self):
        for filename in os.listdir(self.image_folder):
            if filename.endswith('.png'):
                image_name = os.path.splitext(filename)[0]
                template_path = os.path.join(self.image_folder, filename)

                # Преобразование шаблона в ч\б
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

                # Добавление в словарь
                self.image_info[image_name] = {'template': template, 'coord': None}

    async def check_warning(self):
        await self.click_loupe_icon()
        await self.click_farm_icon()
        await self.click_primary_upgrade_btn()
        is_warning_clicked = await self.click_warning_icon()
        return is_warning_clicked

    async def apply_equipment(self):
        await self.click_warning_change_btn()
        is_equipped = await self.click_construction_equip_btn()
        return is_equipped

    async def process_help_command(self):
        print(f"Starting checking equipment for {self.device.serial}")
        is_equipped = False

        while not is_equipped:
            is_warning_clicked = await self.check_warning()

            if is_warning_clicked:
                is_equipped = await self.apply_equipment()
            else:
                is_equipped = True

        # while not await self.check_equipment():
        #     await self.apply_equipment()

        await self.execute_help_command()
        print(f"def process_help_command finished for {self.device.serial}")

    async def click_loupe_icon(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'loupe_icon'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"loupe_icon CLICKED {self.device.serial}")
        else:
            print(f"loupe_icon MISMATCH {self.device.serial}")

    async def click_farm_icon(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'farm_icon'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        # Получаем скриншот от устройства
        screenshot = await self.device.screencap()

        # Ищем шаблон на скриншоте и возвращаем количество совпадений
        loc = await self.get_template_match_locations(screenshot, template)

        # Ищем шаблон на скриншоте и возвращаем количество совпадений
        loc = await self.get_template_match_locations(screenshot, template)

        # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
        if loc[0].size > 0:
            # Берем координаты из словаря, если они есть
            coord = await self.get_coord(template_name, template, loc, btn_offset)

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"farm_icon CLICKED {self.device.serial}")
        else:
            print(f"farm_icon MISMATCH {self.device.serial}")

    async def click_primary_upgrade_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'primary_upgrade_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"primary_upgrade_btn CLICKED {self.device.serial}")
        else:
            print(f"primary_upgrade_btn MISMATCH {self.device.serial}")

    async def click_warning_icon(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'warning_icon'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"warning_icon CLICKED {self.device.serial}")
            return True
        else:
            print(f"warning_icon MISMATCH {self.device.serial}")
            return False

    async def click_warning_change_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'warning_change_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"warning_change_btn CLICKED {self.device.serial}")
        else:
            print(f"warning_change_btn MISMATCH {self.device.serial}")

    async def click_construction_equip_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'construction_equip_btn'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (500, 0)
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"construction_equip_btn CLICKED {self.device.serial}")
            return True
        else:
            print(f"construction_equip_btn MISMATCH {self.device.serial}")
            return False

    async def click_secondary_upgrade_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'secondary_upgrade_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"click_secondary_upgrade_btn CLICKED {self.device.serial}")

    async def click_help_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'help_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"click_help_btn CLICKED {self.device.serial}")

    async def click_cancel_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'cancel_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"click_cancel_btn CLICKED {self.device.serial}")

    async def click_confirm_cancel_btn(self):
        await asyncio.sleep(self.delay)
        # Имя шаблона в папке шаблонов
        template_name = 'confirm_cancel_btn'
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

            # Выполняем команду устройства по полученным координатам
            await self.device.shell(f"input tap {coord[0]} {coord[1]}")
            print(f"click_confirm_cancel_btn CLICKED {self.device.serial}")
            return True
        else:
            return False

    async def click_exit_btn(self):
        has_exit_btn = True
        # Имя шаблона в папке шаблонов
        template_name = 'exit_btn'
        # Отступ шаблона к координатам (x, y) самой кнопки: взять влево(-), вправо (+)
        btn_offset = (0, 0)
        # Берем шаблон из словаря
        template = self.image_info[template_name]['template']

        while has_exit_btn:
            await asyncio.sleep(self.delay)
            # Получаем скриншот от устройства
            screenshot = await self.device.screencap()

            # Ищем шаблон на скриншоте и возвращаем количество совпадений
            loc = await self.get_template_match_locations(screenshot, template)

            # Если есть хотя бы одно совпадение, получаем координаты центра и выполняем команду устройства
            if loc[0].size > 0:
                # Берем координаты из словаря, если они есть
                coord = await self.get_coord(template_name, template, loc, btn_offset)

                # Выполняем команду устройства по полученным координатам
                await self.device.shell(f"input tap {coord[0]} {coord[1]}")
                has_exit_btn = True
                print(f"exit_btn CLICKED {self.device.serial}")
            else:
                has_exit_btn = False
                print(f"exit_btn MISMATCH {self.device.serial}")

    async def calculate_coord(self, loc, template):
        # Отмечаем совпадающую область на изображении (можно убрать в боевом коде)
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(im_array, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

        # Получение координат центра первого совпадения
        first_match_center = (int(loc[1][0] + template.shape[1] / 2), int(loc[0][0] + template.shape[0] / 2))
        # print(f"Center coordinates of the first match for {image_name}:", first_match_center)
        return first_match_center

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

    async def process_help_algorithm(self):
        await self.click_secondary_upgrade_btn()
        await self.click_help_btn()
        await self.click_cancel_btn()
        is_finished = await self.click_confirm_cancel_btn()
        return is_finished

    async def execute_help_command(self):
        print(f"Executing help command for device {self.device.serial}...")
        is_finished = False

        for i in range(self.count + 1):
            print(f"Executing help command for device {self.device.serial}..........{i}")
            is_finished = await self.process_help_algorithm()

        while not is_finished:
            print(f"Before close doing again process_help_algorithm() for {self.device.serial}")
            await self.process_help_algorithm()
        await self.click_exit_btn()

    async def start(self):
        self.process_help_command_task = await asyncio.create_task(self.process_help_command())
        return self.process_help_command_task

    async def stop(self):
        if self.process_help_command_task:
            self.process_help_command_task.cancel()
            await asyncio.gather(self.process_help_command_task, return_exceptions=True)
