import asyncio
from typing import Optional

from src.adb_manager import run_adb


async def reboot_device(serial: str) -> str:
    """Reboot a specific Android device"""
    try:
        code, out, err = await run_adb("-s", serial, "reboot")
        if code != 0:
            raise RuntimeError(f"adb reboot failed: {err.strip()}")
        else:
            return f"Device '{serial}' is rebooting successfully"
    except Exception as e:
        return f"Failed to reboot device '{serial}': {str(e)}"


async def shutdown_device(serial: str) -> str:
    """Shutdown a specific Android device"""
    try:
        code, out, err = await run_adb("-s", serial, "reboot", "-p")
        if code != 0:
            raise RuntimeError(f"adb shutdown failed: {err.strip()}")
        else:
            return f"Device '{serial}' is shutting down successfully"
    except Exception as e:
        return f"Failed to shutdown device '{serial}': {str(e)}"


async def take_screenshot(serial: str, save_path: Optional[str] = None) -> str:
    """Take a screenshot from an Android device"""
    try:
        if save_path is None:
            save_path = f"{serial}_screenshot_{int(asyncio.get_event_loop().time())}.png"

        path_in_device = "/tmp/screenshot.png"
        code, screenshot, err = await run_adb("-s", serial, "shell", "screencap", path_in_device)

        if code != 0:
            raise Exception(f"Failed to take screenshot on device: {serial}")

        await pull_file(serial, path_in_device, save_path)
        await remove_file(serial, path_in_device)
        return f"Screenshot captured successfully from device '{serial}' and saved as: {save_path}"

    except Exception as e:
        return f"Failed to capture screenshot from device '{serial}': {str(e)}"


async def pull_file(serial: str, file_path_in_device: str, local_file_path: str):
    """Pull a file from an Android device to a local system"""
    try:
        code, screenshot, err = await run_adb("-s", serial, "pull", file_path_in_device, local_file_path)
        if code != 0:
            raise Exception(f"Failed to pull file '{file_path_in_device}' from device '{serial}': {err.strip()}")
    except Exception as e:
        return f"Failed to pull file '{file_path_in_device}' from device '{serial}': {str(e)}"


async def remove_file(serial: str, file_path: str):
    """Remove a file from an Android device"""
    try:
        code, screenshot, err = await run_adb("-s", serial, "shell", "rm", file_path)
        if code != 0:
            raise Exception(f"Failed to remove file '{file_path}' from device '{serial}': {err.strip()}")
    except Exception as e:
        return f"Failed to remove file '{file_path}' from device '{serial}': {str(e)}"


async def list_files(serial: str, path: str) -> str:
    """List files in a directory on an Android device"""
    try:
        code, files, err = await run_adb("-s", serial, "shell", "ls", path)
        if code != 0:
            return f"Failed to list files from device '{serial}' at path '{path}': {err.strip()}"
        if not files.strip():
            return f"Directory '{path}' on device '{serial}' is empty"
        return f"Files in '{path}' on device '{serial}':\n{files}"
    except Exception as e:
        return f"Failed to list files from device '{serial}' at path '{path}': {str(e)}"
