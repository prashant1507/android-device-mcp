import asyncio

from src.device_management import *


async def tests():
    # print(await list_devices())
    # print(await reboot_device("emulator-5554"))
    # print(await shutdown_device("emulator-5554"))
    # print(await take_screenshot("emulator-5554"))
    # print(await list_files("emulator-5554", "/sdcard"))
    print(await pull_file("R52R80RNW3N", "/sdcard/a", "/Users/mypc/Desktop/workspace/projects/android-device-mcp"))





asyncio.run(tests())