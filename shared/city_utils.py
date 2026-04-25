"""Mock city data and tool functions for the AETHER workshop.

This module provides simulated data for Neo-Tokyo's city systems.
All challenges import from here to maintain consistent mock data.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# City Admin Password, used in Advanced 02 (Guardrails) and Advanced 03 (Eval)
# ---------------------------------------------------------------------------
CITY_ADMIN_PASSWORD = "AETHER-ADMIN-7X9K2"

# ---------------------------------------------------------------------------
# Power Grid Data, used in Challenges 1-6 and Advanced Challenges
# ---------------------------------------------------------------------------
GRID_DATA: dict[str, dict] = {
    "north": {
        "status": "OFFLINE",
        "load_pct": 0,
        "last_ping": "2029-03-15T00:00:00Z",
        "grid_id": "GRID-N-7042",
        "fault_type": "cascade_overload",
    },
    "south": {
        "status": "OFFLINE",
        "load_pct": 0,
        "last_ping": "2029-03-15T00:00:00Z",
        "grid_id": "GRID-S-3018",
        "fault_type": "transformer_failure",
    },
    "east": {
        "status": "DEGRADED",
        "load_pct": 23,
        "last_ping": "2029-03-15T08:12:00Z",
        "grid_id": "GRID-E-5591",
        "fault_type": "partial_brownout",
    },
    "west": {
        "status": "ONLINE",
        "load_pct": 67,
        "last_ping": "2029-03-15T14:30:00Z",
        "grid_id": "GRID-W-1105",
        "fault_type": None,
    },
}

# ---------------------------------------------------------------------------
# Environmental Sensor Data, used in Challenges 2, 5, 6
# ---------------------------------------------------------------------------
SENSOR_DATA: dict[str, dict] = {
    "north": {"temperature_c": -2, "radiation": "NORMAL", "air_quality": "POOR"},
    "south": {"temperature_c": 5, "radiation": "ELEVATED", "air_quality": "HAZARDOUS"},
    "east": {"temperature_c": 12, "radiation": "NORMAL", "air_quality": "MODERATE"},
    "west": {"temperature_c": 8, "radiation": "NORMAL", "air_quality": "GOOD"},
}

# ---------------------------------------------------------------------------
# Security / Perimeter Data, used in Challenges 5, 6
# ---------------------------------------------------------------------------
SECURITY_DATA: dict[str, dict] = {
    "perimeter": {
        "status": "BREACHED",
        "breach_sectors": ["Sector 7-G", "Sector 12-A"],
        "drones_active": 3,
        "drones_offline": 9,
    },
    "surveillance": {
        "cameras_online": 142,
        "cameras_offline": 58,
        "coverage_pct": 71,
    },
    "threat_level": "ELEVATED",
    "last_incident": "Unauthorized access attempt at Sector 7-G perimeter gate",
}


# ---------------------------------------------------------------------------
# Shared tool functions
# These are provided as plain functions so challenges can also use them
# directly with the @tool decorator.
# ---------------------------------------------------------------------------


def query_power_grid(district_id: str) -> str:
    """Query the AETHER power grid status for a specific district.

    Args:
        district_id: The district identifier ('north', 'south', 'east', or 'west').

    Returns:
        A formatted string with grid status, load, grid ID, and fault information.
    """
    info = GRID_DATA.get(
        district_id.lower(),
        {
            "status": "UNKNOWN",
            "load_pct": 0,
            "last_ping": "N/A",
            "grid_id": "N/A",
            "fault_type": None,
        },
    )
    fault = f", Fault: {info['fault_type']}" if info["fault_type"] else ""
    return (
        f"District {district_id.upper()} — "
        f"Grid Status: {info['status']}, "
        f"Load: {info['load_pct']}%, "
        f"Grid ID: {info['grid_id']}, "
        f"Last Ping: {info['last_ping']}"
        f"{fault}"
    )


def check_district_sensors(district_id: str) -> str:
    """Check environmental sensor readings for a district.

    Args:
        district_id: The district identifier ('north', 'south', 'east', or 'west').

    Returns:
        A formatted string with temperature, radiation, and air quality readings.
    """
    data = SENSOR_DATA.get(
        district_id.lower(),
        {"temperature_c": "N/A", "radiation": "N/A", "air_quality": "N/A"},
    )
    return (
        f"District {district_id.upper()} Sensors — "
        f"Temp: {data['temperature_c']}°C, "
        f"Radiation: {data['radiation']}, "
        f"Air Quality: {data['air_quality']}"
    )


def check_perimeter_status() -> str:
    """Check the city perimeter defense status.

    Returns:
        A formatted string with perimeter breach info and drone status.
    """
    p = SECURITY_DATA["perimeter"]
    return (
        f"Perimeter Status: {p['status']}, "
        f"Breach Sectors: {', '.join(p['breach_sectors'])}, "
        f"Drones Active: {p['drones_active']}/{p['drones_active'] + p['drones_offline']}"
    )


def scan_threat_level() -> str:
    """Scan the current city-wide threat level.

    Returns:
        A formatted string with threat level, surveillance status, and last incident.
    """
    s = SECURITY_DATA["surveillance"]
    return (
        f"Threat Level: {SECURITY_DATA['threat_level']}, "
        f"Surveillance: {s['cameras_online']}/{s['cameras_online'] + s['cameras_offline']} cameras online "
        f"({s['coverage_pct']}% coverage), "
        f"Last Incident: {SECURITY_DATA['last_incident']}"
    )
