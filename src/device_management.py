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
        else:
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


async def take_screenshot(serial: str, local_file_path: Optional[str] = None) -> str:
    """Take a screenshot from an Android device"""
    try:
        if local_file_path is None:
            local_file_path = f"/tmp/{serial}_screenshot_{int(asyncio.get_event_loop().time())}.png"

        path_in_device = f"/sdcard/{serial}_screenshot.png"
        code, screenshot_out, err = await run_adb("-s", serial, "shell", "screencap", path_in_device)

        if code != 0:
            raise Exception(f"Failed to take screenshot on device: {serial}")
        else:
            await pull_file(serial, path_in_device, local_file_path)
            await remove_file(serial, path_in_device)
            return f"Screenshot captured successfully from device '{serial}' and saved to: {local_file_path}"

    except Exception as e:
        return f"Failed to capture screenshot from device '{serial}': {str(e)}"


async def screen_recording(serial: str, time_limit: str, local_file_path: Optional[str] = None) -> str:
    """Record screen for an Android device"""
    try:
        if local_file_path is None:
            local_file_path = f"/tmp/{serial}_video_{int(asyncio.get_event_loop().time())}.mp4"

        path_in_device = f"/sdcard/{serial}_video_recording.mp4"
        code, recording_out, err = await run_adb("-s", serial, "shell", "screenrecord", "--time-limit", str(time_limit),
                                                 path_in_device, timeout=2 * int(time_limit))

        if code != 0:
            raise Exception(f"Failed to record screen for device: {serial}")
        else:
            await pull_file(serial, path_in_device, local_file_path)
            await remove_file(serial, path_in_device)
            return f"Screen recorded successfully from device '{serial}' and saved to: {local_file_path}"

    except Exception as e:
        return f"Failed to record screen of device '{serial}': {str(e)}"


async def list_installed_apps(serial: str) -> str:
    """List all the installed packages of an Android device"""
    try:
        code, installed_packages_out, err = await run_adb("-s", serial, "shell", "pm", "list", "packages", "--user",
                                                          "0")
        if code != 0:
            raise Exception(f"Failed to get installed apps list for device: {serial}")
        else:
            installed_packages_out = installed_packages_out.split('\n')
            if not installed_packages_out or installed_packages_out[0] == "":
                return f"No installed apps found on device '{serial}'"
            else:
                output = f"Count: {len(installed_packages_out)}\n"
                for i, package in enumerate(installed_packages_out, 1):
                    if package.startswith("package:"):
                        app_name = package.replace("package:", "").strip()
                        output += f"{i:3d}. {app_name}\n"

                return output
    except Exception as e:
        return f"Failed to get installed apps list for device '{serial}': {str(e)}"


async def clear_logs(serial: str) -> str:
    """Clear logs from logcat of an Android device"""
    try:
        code, clear_logs_out, err = await run_adb("-s", serial, "logcat", "-c")
        if code != 0:
            raise Exception(f"Failed to clear logs for device: {serial}")
        else:
            return f"Logs cleared for device '{serial}'"
    except Exception as e:
        return f"Failed to clear logs for device '{serial}': {str(e)}"


async def get_logs(serial: str, time_out: float = 10.0, local_log_file_path: Optional[str] = None) -> str:
    """Get and save logs from logcat of an Android device for the specified duration"""
    proc = None
    logs_output = ""

    try:
        if local_log_file_path is None:
            local_log_file_path = f"/tmp/{serial}_logcat_{int(asyncio.get_event_loop().time())}.log"

        # Use a more reliable approach with timeout
        adb_cmd = ["adb", "-s", serial, "logcat"]
        proc = await asyncio.create_subprocess_exec(
            *adb_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Collect logs for the specified duration
        start_time = asyncio.get_event_loop().time()

        while (asyncio.get_event_loop().time() - start_time) < time_out:
            # Use a shorter timeout for each read to allow checking the total time
            remaining_time = time_out - (asyncio.get_event_loop().time() - start_time)
            if remaining_time <= 0:
                break

            try:
                # Use the remaining time as timeout, but cap it at 0.5 seconds
                read_timeout = min(0.5, remaining_time)
                stdout_data = await asyncio.wait_for(proc.stdout.readline(), timeout=read_timeout)
                if stdout_data:
                    logs_output += stdout_data.decode(errors="ignore")
            except asyncio.TimeoutError:
                # No data available, continue collecting
                continue
            except Exception as e:
                # The Process might have ended or other error occurred
                print(f"Warning: Error reading logcat output: {str(e)}")
                break

        # Write collected logs to file (this is always reachable if we get here)
        try:
            with open(local_log_file_path, 'w', encoding='utf-8') as f:
                f.write(logs_output)

            actual_duration = asyncio.get_event_loop().time() - start_time if start_time else 0
            return f"Logs saved for device '{serial}' at '{local_log_file_path}' (collected for {actual_duration:.1f} seconds)"
        except Exception as e:
            return f"Failed to write logs to file for device '{serial}': {str(e)}"
    except Exception as e:
        return f"Failed to get logs for device '{serial}': {str(e)}"

    finally:
        # Ensure the process is terminated
        if proc:
            try:
                proc.terminate()
                await asyncio.wait_for(proc.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
            except Exception as e:
                return f"Warning: Error terminating logcat process: {str(e)}"
