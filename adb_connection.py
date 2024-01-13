from ppadb.client_async import ClientAsync as AdbClient
import asyncio
import subprocess


class AdbConnection:
    def __init__(self):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = None

    async def start_adb_server(self):
        try:
            # Выполняем команду adb start-server
            subprocess.run(["adb", "start-server"], check=True)
        except subprocess.CalledProcessError:
            print("Failed to start adb server. Make sure adb is installed and in your system PATH.")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def connect_device(self, num_devices):
        await self.start_adb_server()
        self.devices = await self.client.devices()

        while len(self.devices) < num_devices:
            print(f"Waiting for {num_devices - len(self.devices)} more devices to connect...")
            await asyncio.sleep(2)
            self.devices = await self.client.devices()

        print("Connected devices:")
        for device in self.devices:
            print(device.serial)

    def get_connected_devices(self):
        return self.devices
