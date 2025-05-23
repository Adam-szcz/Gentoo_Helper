"""
disk_utils.py
-------------
Functions for detecting disks and partitions in Gentoo Helper.
"""

# ——— Standard library ———
import json
import subprocess

# ——— Third-party ———
try:
    import parted
except ImportError:
    parted = None


def list_disks():
    """
    Return a list of dicts for each disk, e.g.:
      { 'path': '/dev/sda', 'model': 'XYZ', 'vendor': 'ACME', 'size': '931G' }

    If python-parted is available, use it; otherwise fall back to lsblk JSON.
    """
    # 1) Use parted if available
    if parted:
        try:
            disks = []
            for dev in parted.getAllDevices():
                if dev.type == parted.DEVICE_TYPE.disk:
                    # size in bytes, convert to human-readable string
                    sz = dev.getSize() * dev.sectorSize
                    for unit in ('B', 'K', 'M', 'G', 'T'):
                        if sz < 1024.0:
                            size_str = f"{int(sz)}{unit}"
                            break
                        sz /= 1024.0

                    disks.append({
                        'path': dev.path,
                        'model': (dev.model or "").strip(),
                        'vendor': "",  # parted.Device has no vendor info
                        'size': size_str
                    })
            return disks
        except Exception:
            # if parted fails for any reason, fall back to lsblk
            pass

    # 2) Fallback: use lsblk JSON output
    result = subprocess.run(
        ['lsblk', '-J', '-o', 'NAME,TYPE,SIZE,MODEL,VENDOR'],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout)
    disks = []

    for blk in data.get('blockdevices', []):
        if blk.get('type') == 'disk':
            # coerce possible None to empty string before strip()
            model = (blk.get('model') or "").strip()
            vendor = (blk.get('vendor') or "").strip()
            size = blk.get('size') or ""

            disks.append({
                'path': f"/dev/{blk.get('name')}",
                'model': model,
                'vendor': vendor,
                'size': size
            })

    return disks


def list_partitions(disk_path):
    """
    Return a list of partition paths for the given disk, e.g.:
      ['/dev/sda1', '/dev/sda2', ...]
    """
    out = subprocess.check_output(
        ['lsblk', '-ln', '-o', 'NAME,TYPE', disk_path],
        text=True
    )
    partitions = []
    for line in out.splitlines():
        name, typ = line.split()
        if typ == 'part':
            partitions.append(f"/dev/{name}")
    return partitions
