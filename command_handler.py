import asyncio
from collections import deque
from construction import Construction


class CommandHandler:
    def __init__(self, device_queues):
        self.device_queues = device_queues
        self.command_handler_task = None
        self.device_command_data = {}  # Словарь для хранения данных по каждому устройству
        # self.constructions = {}  # Добавлен словарь для хранения Construction

    async def setup(self, devices):
        # Инициализируем структуру данных для каждого устройства
        for device in devices:
            self.device_command_data[device] = {
                'in_process': None,  # Текущая выполняемая команда
                'pending': deque()  # Очередь ожидающих выполнения команд
            }

    async def handle_commands(self):
        # Выполняем сборку перед началом работы
        await self.setup(self.device_queues.keys())

        # Запускаем асинхронные задачи
        await asyncio.gather(
            self.add_commands_to_pending(),
            self.process_pending_commands(),
            *[self.execute_device_commands(device, device_data) for device, device_data in self.device_command_data.items()]
        )

    async def add_commands_to_pending(self):
        while True:
            # Проверяем наличие команд в каждой очереди для устройств
            for device, queues in self.device_queues.items():
                if 'command_queue' in queues and not queues['command_queue'].empty():
                    # Получаем команду из очереди
                    command_data = await queues['command_queue'].get()

                    # Проверяем, есть ли команда уже в in_process или pending
                    if not (command_data == self.device_command_data[device]['in_process'] or command_data in
                            self.device_command_data[device]['pending']):
                        # Добавляем команду в очередь ожидания (pending) для соответствующего устройства
                        self.device_command_data[device]['pending'].append(command_data)
                        print(f"Adding command to pending for device {device.serial}: {command_data}")
                    else:
                        print(f"Command {command_data} already exists in pending for device {device.serial}")

            # Выводим содержимое pending для каждого устройства
            for device, data in self.device_command_data.items():
                print(f"Pending commands for device {device.serial}: {data['pending']}")

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    async def process_pending_commands(self):
        while True:
            # Перебираем устройства и обрабатываем их команды
            for device, data in self.device_command_data.items():
                if not data['in_process'] and data['pending']:
                    # Получаем команду из очереди ожидания (pending)
                    command_data = data['pending'].popleft()

                    # Устанавливаем команду в in_process
                    data['in_process'] = command_data
                    print(f"Processing command for device {device.serial}: {command_data}")

            # Выводим содержимое in_process для каждого устройства
            for device, data in self.device_command_data.items():
                print(f"In Process commands for device {device.serial}: {data['in_process']}")

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    async def execute_device_commands(self, device, device_data):
        # data = self.device_command_data[device_data]

        while True:
            if device_data['in_process'] and "ручки" in device_data['in_process']['text']:
                count = device_data['in_process']['text'][1]
                construction = Construction(device, count)
                await construction.start()
                device_data['in_process'] = None

                # Добавь другие условия и методы обработки команд здесь

            await asyncio.sleep(1)  # Небольшая задержка для снижения нагрузки

    def start(self):
        # Запуск асинхронной задачи
        print("Task started for command_handler_task")
        self.command_handler_task = asyncio.create_task(self.handle_commands())
        return self.handle_commands  # Возвращаем созданную задачу

    async def stop(self):
        # Остановка асинхронной задачи
        if self.command_handler_task:
            self.command_handler_task.cancel()
            await asyncio.gather(self.command_handler_task, return_exceptions=True)
