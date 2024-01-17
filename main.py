import asyncio
import json
import time

from adb_connection import AdbConnection
from image_reader import ImageReader
from command_handler import CommandHandler

CONFIG_FILE = "config.json"


async def main():
    allowed_devices = await load_config()
    num_devices = int(input("Enter the number of devices to connect: "))

    adb_connection = AdbConnection()
    await adb_connection.connect_device(num_devices)
    devices = adb_connection.get_connected_devices()

    print("Allowed Devices:", allowed_devices)

    if devices:
        # Создаем общий словарь для хранения очередей от всех устройств
        device_queues = {}

        # Заполняем словарь устройствами только для разрешенных устройств
        for device in devices:
            if device.serial in allowed_devices:
                device_queues[device] = {}

        # Создаем экземпляры классов, передавая общий словарь
        image_reader = ImageReader(CONFIG_FILE, device_queues)
        command_handler = CommandHandler(device_queues)

        try:
            # Запускаем задачи
            image_reader.start()
            command_handler.start()

            # Ожидаем завершения всех задач
            await asyncio.gather(image_reader.image_reader_task, command_handler.command_handler_task)

        except asyncio.CancelledError:
            pass
        finally:
            # Останавливаем задачи перед выходом
            await image_reader.stop()
            await command_handler.stop()


async def load_config():
    print('Loading config file...')
    start_time = time.time()
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)

    # Получаем список устройств
    devices_config = config.get("devices", {})

    # Пример получения allowed_devices
    allowed_devices = list(devices_config.keys())

    elapsed_time = time.time() - start_time
    print(f"Config file loaded in {elapsed_time:.4f} seconds.")
    return allowed_devices


if __name__ == '__main__':
    asyncio.run(main())
