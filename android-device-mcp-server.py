from mcp.server.fastmcp import FastMCP

from src.device import list_devices
from src.device_management import reboot_device, shutdown_device, take_screenshot, list_files

mcp = FastMCP("android-device-mcp")


@mcp.tool(name="list_devices", title="List Devices",
          description="List all connected Android devices with their serial numbers and detailed info using ADB.")
async def list_devices_tool():
    """Returns a list of connected Android devices with serial numbers and detailed information."""
    return await list_devices()


@mcp.tool(name="reboot_device", title="Reboot Device",
          description="Reboot a specific Android device using its serial number via ADB.")
async def reboot_device_tool(serial: str):
    """Reboots the Android device identified by the given serial number."""
    return await reboot_device(serial)


@mcp.tool(name="shutdown_device", title="Shutdown Device",
          description="Shut down a specific Android device using its serial number via ADB.")
async def shutdown_device_tool(serial: str):
    """Shuts down the Android device identified by the given serial number."""
    return await shutdown_device(serial)


@mcp.tool(name="take_screenshot", title="Take Screenshot",
          description="Capture a screenshot from an Android device using its serial number via ADB.")
async def take_screenshot_tool(serial: str):
    """Captures a screenshot from the Android device identified by the given serial number."""
    return await take_screenshot(serial)

@mcp.tool(name="list_files", title="List Files",
          description="List all files in a given directory on an Android device using its serial number. This uses ADB to access the device.")
async def list_files_tool(serial: str, path: str):
    """Lists all files in the specified directory on the Android device identified by the serial number."""
    return await list_files(serial, path)


# @mcp.tool(name="pull_file",
#           description="#######Capture a screenshot from a specific Android device using its serial number.")
# async def pull_file_tool(serial: str, file_path):
#     """Take a screenshot of a specific Android device"""
#     return await take_screenshot(serial)