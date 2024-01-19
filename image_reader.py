import time
import io
import numpy as np
import easyocr
from PIL import Image
import asyncio
from regex_extractor import RegexExtractor


class ImageReader:
    def __init__(self, config_obj, device_queues):
        print('ImageReader Class initializing...')
        start_time = time.time()
        self.lang = ["ru", "en"]
        self.device_queues = device_queues
        self.roi_config = None
        self.allowed_commands = None
        self.config_obj = config_obj
        self.reader = None
        self.top_left_1 = None
        self.bottom_right_1 = None
        self.top_left_2 = None
        self.bottom_right_2 = None
        self.image_reader_task = None
        self.regex_extractor = RegexExtractor()
        elapsed_time = time.time() - start_time
        print(f"ImageReader Class initialized in {elapsed_time:.4f} seconds.")

    async def setup(self, devices):
        # Загружаем общий конфиг
        await self.apply_config()
        self.reader = easyocr.Reader(self.lang)

        # Собираем все очереди от устройств
        for device in devices:
            self.device_queues[device]['command_queue'] = asyncio.Queue()
            self.device_queues[device]['cropped_images_queue'] = asyncio.Queue()
            self.device_queues[device]['extracted_text_queue'] = asyncio.Queue()

    async def handle_image_reader_tasks(self):
        # Выполняем сборку перед началом работы
        await self.setup(self.device_queues.keys())

        # Запускаем асинхронные задачи
        await asyncio.gather(
            *[self.cropped_images_to_queue(device, device_queues) for device, device_queues in self.device_queues.items()],
            *[self.extract_text_from_cropped_images(device, device_queues) for device, device_queues in self.device_queues.items()],
            *[self.process_extracted_text(device, device_queues) for device, device_queues in self.device_queues.items()])

    async def cropped_images_to_queue(self, device, device_queues):
        while True:
            await asyncio.sleep(5)  # Ждем 5 секунд между итерациями

            try:
                screenshot = await device.screencap()
                img = Image.open(io.BytesIO(screenshot))
                cropped_images = self.crop_image(img)

                # Добавляем обрезанные изображения в очередь
                await device_queues['cropped_images_queue'].put(cropped_images)

            except Exception as e:
                print(f"An error occurred while processing screenshot for device {device.serial}: {e}")

    async def extract_text_from_cropped_images(self, device, device_queues):
        while True:
            await asyncio.sleep(1)  # Ждем 1 секунду между итерациями

            try:
                if 'cropped_images_queue' in device_queues and not device_queues['cropped_images_queue'].empty():
                    # Получаем кортеж изображений из очереди
                    cropped_images = await device_queues['cropped_images_queue'].get()

                    # Проходим в цикле по изображениям и конвертируем их в массивы NumPy
                    extracted_text = []
                    for img in cropped_images:
                        img_np = np.array(img)

                        # Извлекаем текст из каждого изображения
                        text = self.reader.readtext(img_np, detail=0)
                        extracted_text.append(text)

                    # Распознанный текст возвращается как кортеж в extracted_text
                    extracted_text_tuple = tuple(extracted_text)

                    # Добавляем extracted_text в очередь extracted_text_queue
                    await device_queues['extracted_text_queue'].put(extracted_text_tuple)

            except Exception as e:
                print(f"An error occurred while processing cropped images for device {device.serial}: {e}")

    async def process_extracted_text(self, device, device_queues):
        # Обработка команд в тексте
        allowed_commands = self.allowed_commands.get(device.serial, [])  # Получаем разрешенные команды для устройства

        while True:
            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

            # Проверяем наличие очереди и её не пустоту
            if 'extracted_text_queue' in device_queues and not device_queues['extracted_text_queue'].empty():
                # Получаем кортеж текстов из очереди
                extracted_text = await device_queues['extracted_text_queue'].get()

                # Обработка каждой строки текста
                for text_line in extracted_text:
                    concatenated_text = ' '.join(text_line)
                    # print(f"Concatenated string: {concatenated_text}")

                    # Проверяем, есть ли разрешенные команды в тексте
                    for command in allowed_commands:
                        if command.lower() in concatenated_text.lower():
                            if command == "ручки":
                                result = await self.regex_extractor.extract_help_command(concatenated_text)
                            elif command == "пехи":
                                result = await self.regex_extractor.extract_rally_command(concatenated_text)
                            else:
                                result = None

                            if result:
                                await device_queues['command_queue'].put({'text': result})
                                print(f"Text-command put in queue for device {device.serial}: {result}")
                                print(
                                    f"Number of text-commands in queue for device {device.serial}: {device_queues['command_queue'].qsize()}")

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

    async def apply_config(self):
        print('Applying config file...')
        start_time = time.time()

        # Загрузка общих параметров конфигурации
        self.roi_config = self.config_obj.get('roi')
        self.calculate_roi_dimensions()

        # Загрузка команд для каждого устройства
        devices_config = self.config_obj.get('devices', {})
        self.allowed_commands = {}
        for device, device_data in devices_config.items():
            commands = device_data.get('commands', [])
            self.allowed_commands[device] = commands

        elapsed_time = time.time() - start_time
        print(f"Config file applied in {elapsed_time:.4f} seconds.")

    def start(self):
        # Запуск асинхронной задачи
        print("Task started for image_reader_task")
        self.image_reader_task = asyncio.create_task(self.handle_image_reader_tasks())
        return self.image_reader_task  # Возвращаем созданную задачу

    async def stop(self):
        # Остановка асинхронной задачи
        if self.image_reader_task:
            self.image_reader_task.cancel()
            await asyncio.gather(self.image_reader_task, return_exceptions=True)
