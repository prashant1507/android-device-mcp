from src.adb_manager import run_adb


async def list_devices(timeout: float = 5.0):
    """List connected Android devices with detailed information"""
    try:
        code, out, err = await run_adb("devices", "-l", timeout=timeout)
        if code != 0:
            raise RuntimeError(f"Failed to list devices: {err.strip()}")
        return await device_details(out)
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

            code, out, err = await run_adb("-s", device_id, "shell", "getprop")
            if code == 0 and out:
                props = {}
                for line in out.split('\n'):
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

                code, serial_no, err = await run_adb("-s", device_id, "get-serialno")
                code, device_state, err = await run_adb("-s", device_id, "get-state")

                # Device Information
                info['device'] = {
                    'model': props.get('ro.product.model', 'Unknown'),
                    'manufacturer': props.get('ro.product.manufacturer', 'Unknown'),
                    'brand': props.get('ro.product.brand', 'Unknown'),
                    'device_name': props.get('ro.product.device', 'Unknown'),
                    'serial': serial_no,
                    'state': device_state
                }

                # Hardware Information
                info['hardware'] = {
                    'cpu_abi': props.get('ro.product.cpu.abi', 'Unknown'),
                    'hardware': props.get('ro.hardware', 'Unknown'),
                }

            # Battery Information
            code, out, err = await run_adb("-s", device_id, "shell", "dumpsys", "battery")
            if code == 0 and out.strip():
                raw_data = {}
                for line in out.split('\n'):
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
