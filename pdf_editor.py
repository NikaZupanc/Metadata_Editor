
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4

import pikepdf


TIMEZONE = ZoneInfo("Europe/Ljubljana")


def format_pdf_date(date: datetime) -> str:
    """Convert datetime to the PDF date format."""

    offset_minutes = int(date.utcoffset().total_seconds() // 60)
    sign = "+" if offset_minutes >= 0 else "-"
    hours, minutes = divmod(abs(offset_minutes), 60)

    return ( f"D:{date:%Y%m%d%H%M%S}" f"{sign}{hours:02d}'{minutes:02d}'")


def edit_pdf(file_path: Path, target_date: datetime) -> Path:
    """Update PDF DocumentInfo and XMP timestamps."""

    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Unsupported file format.")

    # Interpret user input as Slovenia local time
    if target_date.tzinfo is None:
        target_date = target_date.replace(tzinfo=TIMEZONE)
    else:
        target_date = target_date.astimezone(TIMEZONE)

    pdf_date = format_pdf_date(target_date)

    # Modify the existing PDF
    with pikepdf.Pdf.open( file_path, allow_overwriting_input=True,) as pdf:

        # Update XMP metadata
        with pdf.open_metadata( set_pikepdf_as_editor=False ) as metadata:

            metadata["xmp:CreateDate"] = target_date
            metadata["xmp:ModifyDate"] = target_date
            metadata["xmp:MetadataDate"] = target_date

            # Preserve document identity when available
            if "xmpMM:DocumentID" not in metadata:
                metadata["xmpMM:DocumentID"] = f"uuid:{uuid4()}"

            # New identifier for the edited version
            metadata["xmpMM:InstanceID"] = f"uuid:{uuid4()}"

            metadata["xmp:CreatorTool"] = "Metadata Editor"
            metadata["pdf:Producer"] = "Metadata Editor (pikepdf)"

        # Ensure legacy DocumentInfo dates also match
        pdf.docinfo["/CreationDate"] = pikepdf.String(pdf_date)
        pdf.docinfo["/ModDate"] = pikepdf.String(pdf_date)

        # Save changes to the selected PDF path
        pdf.save()

    return file_path
