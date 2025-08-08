import asyncio
from typing import Optional

from src.adb_manager import run_adb
from src.file_system import pull_file, remove_file


async def list_devices(timeout: Optional[float] = 5.0):
    """List connected Android devices with detailed information"""
    try:
        code, list_devices_out, err = await run_adb("devices", "-l", timeout=timeout)
        if code != 0:
            raise RuntimeError(f"Failed to list devices: {err.strip()}")
        return await device_details(list_devices_out)
    except Exception as e:
        return f"Failed to list Android devices: {str(e)}"


async def device_details(output: str):
    devices = []
    device_id = None
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue

        try:
            info = {}
            parts = line.split()
            device_id = parts[0]

            code, properties_out, err = await run_adb("-s", device_id, "shell", "getprop")
            if code == 0 and properties_out:
                props = {}
                for line in properties_out.split('\n'):
                    if line.strip() and '[' in line and ']:' in line:
                        key = line.split('[')[1].split(']')[0]
                        value = line.split(']: [')[1].rstrip(']')
                        props[key] = value

                # OS Information
                info['os'] = {
                    'android_version': props.get('ro.build.version.release', 'Unknown'),
                    'api_level': props.get('ro.build.version.sdk', 'Unknown'),
                    'security_patch': props.get('ro.build.version.security_patch', 'Unknown'),
                    'build_number': props.get('ro.build.display.id', 'Unknown'),
                    'build_date': props.get('ro.build.date', 'Unknown')
                }

                code, serial_no_out, err = await run_adb("-s", device_id, "get-serialno")
                code, device_state_out, err = await run_adb("-s", device_id, "get-state")

                # Device Information
                info['device'] = {
                    'model': props.get('ro.product.model', 'Unknown'),
                    'manufacturer': props.get('ro.product.manufacturer', 'Unknown'),
                    'brand': props.get('ro.product.brand', 'Unknown'),
                    'device_name': props.get('ro.product.device', 'Unknown'),
                    'serial': serial_no_out,
                    'state': device_state_out
                }

                # Hardware Information
                info['hardware'] = {
                    'cpu_abi': props.get('ro.product.cpu.abi', 'Unknown'),
                    'hardware': props.get('ro.hardware', 'Unknown'),
                }

            # Battery Information
            code, dumpsys_battery_out, err = await run_adb("-s", device_id, "shell", "dumpsys", "battery")
            if code == 0 and dumpsys_battery_out:
                raw_data = {}
                for line in dumpsys_battery_out.split('\n'):
                    line = line.strip()
                    if ':' in line and not line.startswith('Current Battery Service state'):
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        raw_data[key] = value

                info['battery'] = f"{int(raw_data.get('level', 0))}%"
            else:
                info['battery'] = "Unknown"

            devices.append(info)
        except Exception as e:
            print(f"Warning: Failed to get details for device {device_id}: {str(e)}")
            continue
    return devices


async def reboot_device(serial: str) -> str:
    """Reboot a specific Android device"""
    try:
        code, reboot_out, err = await run_adb("-s", serial, "reboot")
        if code != 0:
            raise RuntimeError(f"adb reboot failed: {err.strip()}")
        else:
            return f"Device '{serial}' is rebooting successfully"
    except Exception as e:
        return f"Failed to reboot device '{serial}': {str(e)}"


async def shutdown_device(serial: str) -> str:
    """Shutdown a specific Android device"""
    try:
        code, shutdown_out, err = await run_adb("-s", serial, "reboot", "-p")
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

        path_in_device = "/sdcard/screenshot.png"
        code, screenshot_out, err = await run_adb("-s", serial, "shell", "screencap", path_in_device)

        if code != 0:
            raise Exception(f"Failed to take screenshot on device: {serial}")

        await pull_file(serial, path_in_device, save_path)
        await remove_file(serial, path_in_device)
        return f"Screenshot captured successfully from device '{serial}' and saved as: {save_path}"

    except Exception as e:
        return f"Failed to capture screenshot from device '{serial}': {str(e)}"
