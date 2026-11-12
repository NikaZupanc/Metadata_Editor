
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
        raise RuntimeError(
            "ExifTool is not installed or is not available in PATH."
        )

    # Create output file path
    output_path = file_path.with_name(
        f"{file_path.stem}_modified{file_path.suffix}"
    )

    if output_path.exists():
        raise FileExistsError(
            f"Output file already exists: {output_path}"
        )

    # Format date for EXIF metadata
    formatted_date = target_date.strftime("%Y:%m:%d %H:%M:%S")

    # Preserve the original file
    shutil.copy2(file_path, output_path)

    # Modify EXIF timestamps
    try:
        subprocess.run(
            [
                exiftool,
                "-overwrite_original",
                f"-AllDates={formatted_date}",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError as error:
        output_path.unlink(missing_ok=True)

        raise RuntimeError(
            error.stderr.strip() or "Failed to update EXIF metadata."
        ) from error

    return output_path
