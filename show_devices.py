import asyncio
from adb_connection import AdbConnection


async def main():
    num_devices = int(input("Enter the number of devices to connect: "))

    adb_connection = AdbConnection()
    await adb_connection.connect_device(num_devices)


if __name__ == '__main__':
    asyncio.run(main())
