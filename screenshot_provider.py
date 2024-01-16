import asyncio


class ScreenshotProvider:
    def __init__(self, device_queues):
        self.device_queues = device_queues
        self.screenshot_task = None

    async def setup(self, devices):
        # Собираем все очереди от устройств
        for device in devices:
            # Если устройство еще не имеет ключа screenshot_queue, создаем его
            if 'screenshot_queue' not in self.device_queues[device]:
                self.device_queues[device]['screenshot_queue'] = asyncio.Queue()

    async def take_screenshots(self):
        # Выполняем сборку перед началом работы
        await self.setup(self.device_queues.keys())

        while True:
            for device, queues in self.device_queues.items():
                # Делаем скриншот
                screenshot = await device.screencap()
                # print(f"Screenshot made for device {device.serial}")

                # Отправляем скриншот в очередь для дальнейшей обработки
                await queues['screenshot_queue'].put({'image': screenshot})
                # print(f"Put screenshot in queue for device {device.serial}")

            # Выводим количество скриншотов в каждой очереди для отладки
            # for device, queues in self.device_queues.items():
            #     screenshot_queue = queues.get('screenshot_queue')
            #     if screenshot_queue:
            #         print(f"Device {device.serial} - Number of screenshots in queue: {screenshot_queue.qsize()}")

            # Пауза 5 секунд перед следующим скриншотом
            await asyncio.sleep(5)

    def start(self):
        # Запуск асинхронной задачи
        print("Task started for screenshot_task")
        self.screenshot_task = asyncio.create_task(self.take_screenshots())
        return self.screenshot_task  # Возвращаем созданную задачу

    async def stop(self):
        # Остановка асинхронной задачи
        if self.screenshot_task:
            self.screenshot_task.cancel()
            await asyncio.gather(self.screenshot_task, return_exceptions=True)
