import asyncio
import numpy as np
from PIL import Image
import cv2
import io


class Rally:
    def __init__(self, device,level, unit_type):
        self.device = device
        self.level = level
        self.unit_type = unit_type
        self.delay = 0.8
        self.process_rally_command_task = None

    async def test_process(self):
        print(f"Starting test_process for {self.device.serial}")

        for i in range(10):
            print(f"Processing test for {self.device.serial} ......... {i}")

        print(f"def test_process finished for {self.device.serial}")

    async def start(self):
        self.process_rally_command_task = await asyncio.create_task(self.test_process())
        return self.process_rally_command_task

    async def stop(self):
        if self.process_rally_command_task:
            self.process_rally_command_task.cancel()
            await asyncio.gather(self.process_rally_command_task, return_exceptions=True)