import json
import platform
import socket
from datetime import datetime

import psutil
from langchain_core.tools import tool


@tool
def check_device_status() -> dict:
    """Get real basic information about the current Mac."""
    print("[REAL TOOL] Reading Mac device information")

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "hostname": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release(),
        "macos_version": platform.mac_ver()[0],
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "memory_used_percent": memory.percent,
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_used_percent": disk.percent,
    }


@tool
def get_cpu_usage() -> dict:
    """Read the REAL current CPU usage percentage from this Mac."""
    print("[REAL TOOL] Reading current CPU usage")

    cpu = psutil.cpu_percent(interval=2)

    return {
        "cpu_usage_percent": cpu,
        "measurement": "2-second local measurement",
    }


@tool
def get_memory_usage() -> dict:
    """Read the REAL current memory usage percentage from this Mac."""
    print("[REAL TOOL] Reading current memory usage")

    memory = psutil.virtual_memory()

    return {
        "memory_usage_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_available_gb": round(memory.available / (1024**3), 2),
        "memory_total_gb": round(memory.total / (1024**3), 2),
    }


@tool
def get_disk_usage() -> dict:
    """Read the REAL disk usage of the Mac root filesystem."""
    print("[REAL TOOL] Reading disk usage")

    disk = psutil.disk_usage("/")

    return {
        "disk_usage_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
    }


@tool
def get_battery_status() -> dict:
    """Read the REAL battery status when available on the Mac."""
    print("[REAL TOOL] Reading battery status")

    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "available": False,
            "message": "Battery information is not exposed by psutil on this Mac."
        }

    return {
        "available": True,
        "percent": battery.percent,
        "plugged_in": battery.power_plugged,
        "time_left_seconds": (
            None if battery.secsleft < 0 else battery.secsleft
        ),
    }


@tool
def create_service_ticket(
    description: str,
    priority: str = "High",
) -> dict:
    """Create a SAFE local IT ticket record for the POC.

    This does NOT contact Jira, ServiceNow, or any external ITSM system.
    """
    print("[POC TOOL] Creating local ticket record")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ticket_id = f"MAC-INC-{timestamp}"

    ticket = {
        "ticket_id": ticket_id,
        "status": "Created - Local POC",
        "priority": priority,
        "device": socket.gethostname(),
        "description": description,
        "created_at": datetime.now().isoformat(),
    }

    with open("created_ticket.json", "w", encoding="utf-8") as file:
        json.dump(ticket, file, indent=2)

    return ticket
