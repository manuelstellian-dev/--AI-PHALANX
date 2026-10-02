"""
polis.sysinfo — host resource sensing (replaces psutil).

Reads the Linux kernel interface (/proc) directly; on other platforms it
degrades to what the standard library exposes (os.cpu_count, os.getloadavg,
os.sysconf, shutil.disk_usage). The public functions mirror the subset of the
psutil API that Helot and Shield Bearer use, so their logic is unchanged.

Formulas (identical to psutil's definitions):
- cpu_percent = 100 · (Δbusy / Δtotal) over the sampling interval, where
  busy = total − idle − iowait (from /proc/stat)
- memory percent = 100 · (total − available) / total (MemAvailable)
- disk percent = 100 · used / (used + free)
"""

import os
import shutil
import socket
import struct
import sys
import time
from collections import namedtuple
from typing import List, Optional, Tuple


class Error(Exception):
    """Base error for sensing failures."""


class AccessDenied(Error):
    """The kernel refused access to the requested information."""


svmem = namedtuple("svmem", ["total", "available", "percent", "used", "free"])
sdiskusage = namedtuple("sdiskusage", ["total", "used", "free", "percent"])
addr = namedtuple("addr", ["ip", "port"])
sconn = namedtuple("sconn", ["fd", "family", "type", "laddr", "raddr", "status", "pid"])

# /proc/net/tcp state codes (include/net/tcp_states.h)
TCP_STATES = {
    "01": "ESTABLISHED", "02": "SYN_SENT", "03": "SYN_RECV", "04": "FIN_WAIT1",
    "05": "FIN_WAIT2", "06": "TIME_WAIT", "07": "CLOSE", "08": "CLOSE_WAIT",
    "09": "LAST_ACK", "0A": "LISTEN", "0B": "CLOSING",
}

_last_cpu_times: Optional[Tuple[int, int]] = None


def cpu_count() -> int:
    """Number of logical CPUs."""
    return os.cpu_count() or 1


def _read_cpu_times() -> Optional[Tuple[int, int]]:
    """(busy, total) jiffies from the aggregate 'cpu' line of /proc/stat."""
    try:
        with open("/proc/stat", encoding="ascii") as f:
            fields = [int(x) for x in f.readline().split()[1:]]
    except (OSError, ValueError):
        return None
    total = sum(fields[:8])  # user nice system idle iowait irq softirq steal
    idle = fields[3] + (fields[4] if len(fields) > 4 else 0)
    return total - idle, total


def cpu_percent(interval: Optional[float] = None) -> float:
    """
    System-wide CPU utilization in percent.

    Args:
        interval: Seconds to sample (blocking). None or 0 compares with the
            previous call, like psutil (the first such call returns 0.0).
    """
    global _last_cpu_times
    if interval:
        start = _read_cpu_times()
        time.sleep(interval)
        end = _read_cpu_times()
    else:
        start, end = _last_cpu_times, _read_cpu_times()
    if end is not None:
        _last_cpu_times = end
    if start is None or end is None:
        if end is None and hasattr(os, "getloadavg"):
            # Non-Linux fallback: 1-minute load per core, as a percentage
            return round(min(100.0, 100.0 * os.getloadavg()[0] / cpu_count()), 1)
        return 0.0
    d_busy, d_total = end[0] - start[0], end[1] - start[1]
    if d_total <= 0:
        return 0.0
    return round(100.0 * d_busy / d_total, 1)


def virtual_memory() -> svmem:
    """Physical memory statistics (bytes; percent in use)."""
    info = {}
    try:
        with open("/proc/meminfo", encoding="ascii") as f:
            for line in f:
                key, _, rest = line.partition(":")
                info[key] = int(rest.split()[0]) * 1024
        total = info["MemTotal"]
        available = info.get("MemAvailable", info.get("MemFree", 0))
        free = info.get("MemFree", 0)
    except (OSError, KeyError, ValueError, IndexError):
        page = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096
        total = page * os.sysconf("SC_PHYS_PAGES") if hasattr(os, "sysconf") else 0
        available = page * os.sysconf("SC_AVPHYS_PAGES") if hasattr(os, "sysconf") else 0
        free = available
    used = total - available
    percent = round(100.0 * used / total, 1) if total else 0.0
    return svmem(total, available, percent, used, free)


def disk_usage(path: str) -> sdiskusage:
    """Disk usage of the filesystem containing `path`."""
    usage = shutil.disk_usage(path)
    denominator = usage.used + usage.free
    percent = round(100.0 * usage.used / denominator, 1) if denominator else 0.0
    return sdiskusage(usage.total, usage.used, usage.free, percent)


def _decode_address(hex_addr: str, family: int) -> addr:
    ip_hex, port_hex = hex_addr.split(":")
    port = int(port_hex, 16)
    raw = bytes.fromhex(ip_hex)
    if family == socket.AF_INET:
        ip = socket.inet_ntop(socket.AF_INET, struct.pack("<I", struct.unpack(">I", raw)[0]))
    else:
        # IPv6: four 32-bit words, each in host (little-endian) order
        words = struct.unpack(">4I", raw)
        ip = socket.inet_ntop(socket.AF_INET6, struct.pack("<4I", *words))
    return addr(ip, port)


def net_connections(kind: str = "inet") -> List[sconn]:
    """
    Socket connections from /proc/net/{tcp,tcp6,udp,udp6}.

    Args:
        kind: "inet" (TCP and UDP, IPv4 and IPv6), "tcp" or "udp"

    Raises:
        AccessDenied: /proc/net is not readable (e.g. restricted container)
    """
    sources = {
        "tcp": [("tcp", socket.AF_INET, socket.SOCK_STREAM), ("tcp6", socket.AF_INET6, socket.SOCK_STREAM)],
        "udp": [("udp", socket.AF_INET, socket.SOCK_DGRAM), ("udp6", socket.AF_INET6, socket.SOCK_DGRAM)],
    }
    tables = sources["tcp"] + sources["udp"] if kind == "inet" else sources[kind]
    if not sys.platform.startswith("linux"):
        return []
    connections: List[sconn] = []
    for name, family, sock_type in tables:
        path = f"/proc/net/{name}"
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="ascii") as f:
                next(f)
                for line in f:
                    parts = line.split()
                    local = _decode_address(parts[1], family)
                    remote = _decode_address(parts[2], family)
                    status = TCP_STATES.get(parts[3], "NONE") if sock_type == socket.SOCK_STREAM else "NONE"
                    raddr = () if remote.port == 0 and remote.ip in ("0.0.0.0", "::") else remote
                    connections.append(sconn(-1, family, sock_type, local, raddr, status, None))
        except PermissionError as e:
            raise AccessDenied(str(e)) from e
    return connections
