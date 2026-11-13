
import os

from pathlib import Path
from datetime import datetime
from win32_setctime import setctime


def edit_filesystem(file_path: Path, target_date: datetime) -> Path:
    """
    Modify creation, access, and modification timestamps of an existing Windows file.
    """

    if os.name != "nt":
        raise OSError("Filesystem timestamp editing requires Windows.")

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    timestamp = target_date.timestamp()
    setctime(str(file_path), timestamp)         # Changes Created
    os.utime(file_path, (timestamp, timestamp)) # Changes Accessed and Modified

    return file_path


# (Get-Item -LiteralPath "C:\forensics\vaja_5\fotografija_E1168970.jpg").LastAccessTime