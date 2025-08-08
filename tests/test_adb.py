import asyncio

from src.device import list_devices


async def list_devices_tool():
    """
    Return list of connected devices (adb).
    """
    a = await list_devices()
    return a

result = asyncio.run(list_devices_tool())
print(result)