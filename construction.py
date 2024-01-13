import asyncio
from PIL import Image
import io


class Construction:
    def __init__(self, device, count):
        self.device = device
        self.count = count
        self.delay = 0.7
        self.process_help_command_task = None

    async def screenshot(self, l_button_coord, r_button_coord):
        await asyncio.sleep(1)
        result = await self.device.screencap()

        im = Image.open(io.BytesIO(result))
        # im.show()

        rgb_im = im.convert("RGB")
        rgb_l_button = rgb_im.getpixel(l_button_coord)
        rgb_r_button = rgb_im.getpixel(r_button_coord)

        print(self.device.serial, "New screenshot made!")
        return rgb_l_button, rgb_r_button

    async def check_equipment(self):
        await self.click_loupe_icon()
        await self.click_farm_icon()
        await self.click_research_btn()
        is_equipped = await self.check_warning_icon()
        return is_equipped

    async def apply_equipment(self):
        await self.click_warning_icon()
        await self.click_change_btn()
        await self.click_apply_btn()

    async def process_help_command(self):
        print(f"Starting checking equipment for {self.device.serial}")
        is_equipped = await self.check_equipment()

        if not is_equipped:
            await self.apply_equipment()
        else:
            await self.execute_help_command()

    async def click_loupe_icon(self):
        l_button_coord = (400, 190)
        r_button_coord = (670, 430)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (24, 106, 164) and rgb_r_button != (215, 191, 99):
            await self.device.shell(f"input tap {l_button_coord[0]} {l_button_coord[1]}")
            # print(self.device.serial, "click_loupe_icon CLICKED")
        # else:
        # print(self.device.serial, "click_loupe_icon NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_farm_icon(self):
        l_button_coord = (400, 190)
        r_button_coord = (670, 430)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (24, 106, 164) and rgb_r_button == (212, 189, 99):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_farm_icon CLICKED")
        # else:
        #     print(self.device.serial, "click_farm_icon NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_research_btn(self):
        l_button_coord = (830, 620)
        r_button_coord = (1030, 630)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (50, 117, 133) and rgb_r_button == (175, 117, 42):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_research_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_research_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def check_warning_icon(self):
        l_button_coord = (840, 550)
        r_button_coord = (720, 600)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (173, 10, 7) and rgb_r_button == (177, 119, 37):
            # print(self.device.serial, "check_warning_icon FALSE")
            await asyncio.sleep(self.delay)
            return False
        else:
            # print(self.device.serial, "click_warning_icon NOT MATCH")
            await asyncio.sleep(self.delay)
            return True

    async def click_warning_icon(self):
        l_button_coord = (840, 550)
        r_button_coord = (720, 600)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (173, 10, 7) and rgb_r_button == (177, 119, 37):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_warning_icon CLICKED")
        # else:
        #     print(self.device.serial, "click_warning_icon NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_change_btn(self):
        l_button_coord = (860, 120)
        r_button_coord = (530, 430)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (255, 190, 58) and rgb_r_button == (176, 118, 38):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_change_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_change_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_apply_btn(self):
        l_button_coord = (810, 560)
        r_button_coord = (1100, 650)
        # Берем цвет с другой, но нажимаем эту, эта мигает и меняет цвета
        click_button_coord = (1100, 550)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (54, 120, 128) and rgb_r_button == (140, 98, 57):
            await self.device.shell(f"input tap {click_button_coord[0]} {click_button_coord[1]}")
        #     print(self.device.serial, "click_apply_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_apply_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_upgrade_btn(self):
        l_button_coord = (540, 610)
        r_button_coord = (880, 610)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (51, 117, 133) and rgb_r_button == (175, 117, 41):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_upgrade_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_upgrade_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_help_btn(self):
        l_button_coord = (540, 640)
        r_button_coord = (880, 640)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (50, 116, 132) and rgb_r_button == (171, 81, 39):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_help_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_help_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_cancel_btn(self):
        l_button_coord = (540, 640)
        r_button_coord = (880, 640)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (50, 116, 132) and rgb_r_button == (16, 99, 165):
            await self.device.shell(f"input tap {l_button_coord[0]} {l_button_coord[1]}")
        #     print(self.device.serial, "click_cancel_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_cancel_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_confirm_cancel_btn(self):
        l_button_coord = (570, 420)
        r_button_coord = (780, 420)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (163, 61, 61) and rgb_r_button == (47, 115, 132):
            await self.device.shell(f"input tap {r_button_coord[0]} {r_button_coord[1]}")
        #     print(self.device.serial, "click_confirm_cancel_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_confirm_cancel_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_first_exit_btn(self):
        l_button_coord = (1210, 40)
        r_button_coord = (880, 610)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (151, 77, 81) and rgb_r_button == (175, 117, 41):
            await self.device.shell(f"input tap {l_button_coord[0]} {l_button_coord[1]}")
        #     print(self.device.serial, "click_exit_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_exit_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def click_second_exit_btn(self):
        l_button_coord = (1210, 40)
        r_button_coord = (1030, 640)
        rgb_l_button, rgb_r_button = await self.screenshot(l_button_coord, r_button_coord)

        if rgb_l_button == (151, 77, 81) and rgb_r_button == (175, 117, 43):
            await self.device.shell(f"input tap {l_button_coord[0]} {l_button_coord[1]}")
        #     print(self.device.serial, "click_exit_btn CLICKED")
        # else:
        #     print(self.device.serial, "click_exit_btn NOT MATCH")

        await asyncio.sleep(self.delay)

    async def execute_help_command(self):
        print(f"Executing help command for device {self.device.serial}...")

        for i in range(self.count + 1):
            print(f"Executing help command for device {self.device.serial}..........{i}")
            await self.click_upgrade_btn()
            await self.click_help_btn()
            await self.click_cancel_btn()
            await self.click_confirm_cancel_btn()

            # await asyncio.sleep(0)
        await self.click_first_exit_btn()
        await self.click_second_exit_btn()
        # await asyncio.sleep(0)

    async def start(self):
        self.process_help_command_task = await asyncio.create_task(self.process_help_command())
        return self.process_help_command_task

    async def stop(self):
        if self.process_help_command_task:
            self.process_help_command_task.cancel()
            await asyncio.gather(self.process_help_command_task, return_exceptions=True)
