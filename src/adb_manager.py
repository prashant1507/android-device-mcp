import asyncio
from typing import Optional


async def run_adb(*args, timeout: Optional[float] = 30.0) -> (int, str, str):
    """Execute ADB command with timeout and error handling"""
    try:
        await ensure_adb_server()
        adb_cmd = ["adb"] + list(args)
        proc = await asyncio.create_subprocess_exec(
            *adb_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            raise TimeoutError(f"ADB command timed out after {timeout} seconds: {' '.join(adb_cmd)}")
        return proc.returncode, stdout.decode(errors="ignore").strip(), stderr.decode(errors="ignore").strip()
    except Exception as e:
        raise RuntimeError(f"Failed to execute ADB command {' '.join(args)}: {str(e)}")


async def ensure_adb_server(timeout: Optional[float] = 30.0):
    """Ensure ADB server is running and accessible"""
    try:
        command = ["adb", "start-server"]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            if proc.returncode != 0:
                raise RuntimeError(f"Failed to start ADB server: {stderr.decode(errors='ignore').strip()}")
        except asyncio.TimeoutError:
            proc.kill()
            raise TimeoutError(f"ADB server start timed out after {timeout} seconds")
    except Exception as e:
        raise RuntimeError(f"Failed to ensure ADB server is running: {str(e)}")
