import json
import time
import io
import numpy as np
import easyocr
from PIL import Image
import asyncio
from regex_extractor import RegexExtractor


class ImageReader:
    def __init__(self, config_file: str, device_queues):
        print('Class initializing...')
        start_time = time.time()
        self.device_queues = device_queues
        self.roi_config = None
        self.allowed_commands = None
        self.config_file = config_file
        self.reader = None
        self.top_left_1 = None
        self.bottom_right_1 = None
        self.top_left_2 = None
        self.bottom_right_2 = None
        self.image_reader_task = None
        self.regex_extractor = RegexExtractor()
        elapsed_time = time.time() - start_time
        print(f"Class initialized in {elapsed_time:.4f} seconds.")

    async def setup(self, devices):
        # Загружаем общий конфиг
        await self.load_config()

        # Собираем все очереди от устройств
        for device in devices:
            # Если устройство еще не имеет ключа command_queue, создаем его
            if 'command_queue' not in self.device_queues[device]:
                self.device_queues[device]['command_queue'] = asyncio.Queue()

    async def get_screenshot(self):
        # Выполняем сборку перед началом работы
        await self.setup(self.device_queues.keys())

        while True:
            for device, queues in self.device_queues.items():
                # Проверяем наличие очереди и её не пустоту
                if 'screenshot_queue' in queues and not queues['screenshot_queue'].empty():
                    # Получаем скриншот из очереди
                    screenshot = await queues['screenshot_queue'].get()
                    # print(f"Screenshot get from device queue {device.serial}")
                    lang = "ru", "en"

                    if screenshot:
                        await self.extract_text(device, screenshot['image'], lang)
                else:
                    # Если очередь пуста или не существует, ждем 1 секунду
                    await asyncio.sleep(1)

    async def extract_text(self, device, screenshot, lang) -> (str, str):
        # print('Text extracting...')
        start_time = time.time()

        try:
            if self.roi_config is None:
                await self.load_config()

            img = Image.open(io.BytesIO(screenshot))

            # Обрезаем изображение согласно ROI
            cropped_images = self.crop_image(img)

            # Конвертируем обрезанные изображения в массивы NumPy
            img_np_1 = np.array(cropped_images[0])
            img_np_2 = np.array(cropped_images[1])

            if self.reader is None:
                self.reader = easyocr.Reader(lang)

            # Извлекаем текст из каждого изображения
            extracted_text_1 = self.reader.readtext(img_np_1, detail=0)
            extracted_text_2 = self.reader.readtext(img_np_2, detail=0)

            elapsed_time = time.time() - start_time

            # print(f"Text extracted in {elapsed_time:.4f} seconds. Device {device.serial}")
            # print(extracted_text_1)
            # print(extracted_text_2)

            await self.process_text(device, (extracted_text_1, extracted_text_2))

            return extracted_text_1, extracted_text_2

        except Exception as e:
            print(f"An error occurred while processing the screenshot: {e}")
            return "", ""

    async def process_text(self, device, extracted_texts):
        # Обработка команд в тексте
        allowed_commands = self.allowed_commands.get(device.serial, [])  # Получаем разрешенные команды для устройства
        # print(f"allowed_commands {allowed_commands} {device.serial}")
        for extracted_text in extracted_texts:
            concatenated_text = ' '.join(extracted_text)
            # print(f"Concatenated string: {concatenated_text}")

            # Проверяем, есть ли разрешенные команды в тексте
            for command in allowed_commands:
                if command.lower() in concatenated_text.lower():
                    result = await self.regex_extractor.extract_help_command(concatenated_text)
                    if result:
                        await self.device_queues[device]['command_queue'].put({'text': result})
                        print(f"Text-command put in queue for device {device.serial}: {result}")
                        print(f"Number of text-commands in queue for device {device.serial}: {self.device_queues[device]['command_queue'].qsize()}")

        # Выводим количество команд в каждой очереди для отладки
        # command_queue = self.device_queues[device].get('command_queue')
        # if command_queue:
            # print(f"Device {device.serial} - Number of commands in queue: {command_queue.qsize()}")

    def crop_image(self, image: Image) -> (Image, Image):
        cropped_image_1 = image.crop(
            (self.top_left_1[0], self.top_left_1[1], self.bottom_right_1[0], self.bottom_right_1[1]))
        cropped_image_2 = image.crop(
            (self.top_left_2[0], self.top_left_2[1], self.bottom_right_2[0], self.bottom_right_2[1]))

        return cropped_image_1, cropped_image_2

    def calculate_roi_dimensions(self):
        if self.roi_config:
            x = self.roi_config['x']
            y = self.roi_config['y']
            line_width = self.roi_config['line_width']
            line_height = self.roi_config['line_height']

            # Для первой области
            self.top_left_1 = (x, y)
            self.bottom_right_1 = (x + line_width, y + line_height)

            # Для второй области, начинающейся сразу под первой
            self.top_left_2 = (x, y + line_height)
            self.bottom_right_2 = (x + line_width, y + 2 * line_height)

    async def load_config(self):
        print('Loading config file...')
        start_time = time.time()
        with open(self.config_file, 'r', encoding="utf8") as file:
            config = json.load(file)

        # Загрузка общих параметров конфигурации
        self.roi_config = config.get('roi')
        self.calculate_roi_dimensions()

        # Загрузка команд для каждого устройства
        devices_config = config.get('devices', {})
        self.allowed_commands = {}
        for device, device_data in devices_config.items():
            commands = device_data.get('commands', [])
            self.allowed_commands[device] = commands

        elapsed_time = time.time() - start_time
        print(f"Config file loaded in {elapsed_time:.4f} seconds.")

    def start(self):
        # Запуск асинхронной задачи
        print("Task started for image_reader_task")
        self.image_reader_task = asyncio.create_task(self.get_screenshot())
        return self.image_reader_task  # Возвращаем созданную задачу

    async def stop(self):
        # Остановка асинхронной задачи
        if self.image_reader_task:
            self.image_reader_task.cancel()
            await asyncio.gather(self.image_reader_task, return_exceptions=True)
