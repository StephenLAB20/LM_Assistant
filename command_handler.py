import asyncio
import time
from collections import deque
from construction import Construction
from rally import Rally


class CommandHandler:
    def __init__(self, device_queues):
        print('CommandHandler Class initializing...')
        start_time = time.time()
        self.device_queues = device_queues
        self.command_handler_task = None
        self.device_command_data = {}  # Словарь для хранения данных по каждому устройству
        # self.constructions = {}  # Добавлен словарь для хранения Construction
        elapsed_time = time.time() - start_time
        print(f"CommandHandler Class initialized in {elapsed_time:.4f} seconds.")

    async def setup(self, devices):
        # Инициализируем структуру данных для каждого устройства
        for device in devices:
            self.device_command_data[device] = {
                'previous_command': None,  # Предыдущая выполненная команда
                'in_process': None,  # Текущая выполняемая команда
                'pending': deque()  # Очередь ожидающих выполнения команд
            }

    async def handle_command_handler_tasks(self):
        # Выполняем сборку перед началом работы
        await self.setup(self.device_queues.keys())

        # Запускаем асинхронные задачи
        await asyncio.gather(
            *[self.add_commands_to_pending(device, device_queues) for device, device_queues in self.device_queues.items()],
            *[self.process_pending_commands(device, device_data) for device, device_data in self.device_command_data.items()],
            *[self.execute_device_commands(device, device_data) for device, device_data in self.device_command_data.items()]
        )

    async def add_commands_to_pending(self, device, device_queues):
        while True:
            if 'command_queue' in device_queues and not device_queues['command_queue'].empty():
                # Получаем команду из очереди
                command_data = await device_queues['command_queue'].get()

                # Проверяем, есть ли команда уже в in_process или pending
                if not (command_data == self.device_command_data[device]['in_process'] or command_data in
                        self.device_command_data[device]['pending']):
                    # Добавляем команду в очередь ожидания (pending) для соответствующего устройства
                    self.device_command_data[device]['pending'].append(command_data)
                    print(f"Adding command to pending for device {device.serial}: {command_data}")
                    # Выводим содержимое pending для каждого устройства
                    print(f"Pending commands for device {device.serial}: {self.device_command_data[device]['pending']}")
                else:
                    print(f"Command {command_data} already exists in pending for device {device.serial}")

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    async def process_pending_commands(self, device, device_data):
        while True:
            if not device_data['in_process'] and device_data['pending']:
                # Получаем команду из очереди ожидания (pending)
                command_data = device_data['pending'].popleft()

                # Устанавливаем команду в in_process
                device_data['in_process'] = command_data
                print(f"Adding command to in_process for device {device.serial}: {command_data}")

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    async def execute_device_commands(self, device, device_data):
        while True:
            if device_data['in_process'] and "ручки" in device_data['in_process']['text']:
                count = device_data['in_process']['text'][1]
                print(f"Construction class for device {device.serial}")
                construction = Construction(device, count)
                await construction.start()
                await construction.stop()
                device_data['in_process'] = None

            if device_data['in_process'] and "пехи" in device_data['in_process']['text']:
                level, unit_type = device_data['in_process']['text']
                print(f"Rally class for device {device.serial}")
                rally = Rally(device, level, unit_type)
                await rally.start()
                await rally.stop()
                device_data['in_process'] = None

                # Добавь другие условия и методы обработки команд здесь

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    def start(self):
        # Запуск асинхронной задачи
        print("Task started for command_handler_task")
        self.command_handler_task = asyncio.create_task(self.handle_command_handler_tasks())
        return self.handle_command_handler_tasks  # Возвращаем созданную задачу

    async def stop(self):
        # Остановка асинхронной задачи
        if self.command_handler_task:
            self.command_handler_task.cancel()
            await asyncio.gather(self.command_handler_task, return_exceptions=True)
