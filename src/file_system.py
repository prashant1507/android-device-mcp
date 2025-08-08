from typing import Optional

from src.adb_manager import run_adb


async def pull_file(serial: str, file_path_in_device: str, local_folder: Optional[str] = None):
    """Pull a file from an Android device to a local system"""
    try:
        if local_folder is None:
            local_folder = "/tmp"
        code, screenshot, err = await run_adb("-s", serial, "pull", file_path_in_device, local_folder)
        if code != 0:
            raise Exception(f"Failed to pull file '{file_path_in_device}' from device '{serial}': {err.strip()}")
        else:
            return f"File pulled successfully to '{local_folder}'"
    except Exception as e:
        return f"Failed to pull file '{file_path_in_device}' from device '{serial}': {str(e)}"


async def push_file(serial: str, local_file: str, folder_path_in_device: str):
    """Push a file to an Android device from a local system"""
    try:
        code, screenshot, err = await run_adb("-s", serial, "push", local_file, folder_path_in_device)
        if code != 0:
            raise Exception(f"Failed to push file '{local_file}' to device '{serial}': {err.strip()}")
        else:
            return f"File pushed successfully to '{folder_path_in_device}'"
    except Exception as e:
        return f"Failed to push file '{local_file}' to device '{serial}': {str(e)}"


async def remove_file(serial: str, file_path_in_device: str):
    """Remove a file from an Android device"""
    try:
        code, screenshot, err = await run_adb("-s", serial, "shell", "rm", file_path_in_device)
        if code != 0:
            raise Exception(f"Failed to remove file '{file_path_in_device}' from device '{serial}': {err.strip()}")
        else:
            return f"File removed successfully '{file_path_in_device}'"
    except Exception as e:
        return f"Failed to remove file '{file_path_in_device}' from device '{serial}': {str(e)}"


async def list_files(serial: str, file_path_in_device: str) -> str:
    """List files in a directory on an Android device"""
    try:
        code, files, err = await run_adb("-s", serial, "shell", "ls", file_path_in_device)
        if code != 0:
            return f"Failed to list files from device '{serial}' at path '{file_path_in_device}': {err.strip()}"
        if not files.strip():
            return f"Directory '{file_path_in_device}' on device '{serial}' is empty"
        return f"Files in '{file_path_in_device}' on device '{serial}':\n{files}"
    except Exception as e:
        return f"Failed to list files from device '{serial}' at path '{file_path_in_device}': {str(e)}"
