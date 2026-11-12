
import shutil
import subprocess

from pathlib import Path
from datetime import datetime


def edit_image(file_path: Path, target_date: datetime) -> Path:
    """
    Modify JPEG EXIF timestamps using ExifTool.

    Creates a modified copy while preserving the original file.
    """

    # Check if ExifTool is installed
    exiftool = shutil.which("exiftool")

    if not exiftool:
        raise RuntimeError( "ExifTool is not installed or is not available in PATH." )

    # Format date for EXIF metadata
    formatted_date = target_date.strftime("%Y:%m:%d %H:%M:%S")

    # Modify EXIF timestamps
    try:
        subprocess.run(
            [
                exiftool,
                "-overwrite_original",
                f"-AllDates={formatted_date}",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError as error:
        file_path.unlink(missing_ok=True)

        raise RuntimeError( error.stderr.strip() or "Failed to update EXIF metadata.") from error

    return file_path

# exiftool -time:all -G1 -a -s "fotografija_E1168970.jpg"