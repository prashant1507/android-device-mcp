import asyncio


async def run_adb(*args, timeout: float = 30.0) -> (int, str, str):
    """Execute ADB command"""
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
        raise TimeoutError("ADB command timed out")
    return proc.returncode, stdout.decode(errors="ignore").strip(), stderr.decode(errors="ignore").strip()


async def ensure_adb_server(timeout: float = 30.0):
    """Ensure ADB server is running"""
    command = ["adb", "start-server"]
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        raise TimeoutError("ADB command timed out")