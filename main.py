
from pathlib import Path
from datetime import datetime

from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from image_editor import edit_image
from filesystem import edit_filesystem
from pdf_editor import edit_pdf


console = Console()

PURPLE = "#A78BFA"
LIGHT_PURPLE = "#D8C4FF"
GREEN = "#64DFA5"
RED = "#F87171"
BACKGROUND = "#202033"

EDITORS = {
    ".jpg": edit_image,
    ".jpeg": edit_image,
    ".pdf": edit_pdf,
}

FILE_TYPES = {
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".docx": "Word Document",
    ".xlsx": "Excel Spreadsheet",
    ".pdf": "PDF Document",
}


def panel_width():
    return min(82, console.width - 2)


def display_header():
    title = Text(
        "METADATA EDITOR",
        style=f"bold {LIGHT_PURPLE}",
        justify="center",
    )
    subtitle = Text(
        "File Metadata Manipulation Tool",
        style="#A3A7B7",
        justify="center",
    )

    console.print()
    console.print(
        Panel(
            Group(title, subtitle),
            border_style=PURPLE,
            style=f"on {BACKGROUND}",
            width=panel_width(),
            padding=(1, 2),
        )
    )


def display_section(number, title):
    console.print()
    console.print(
        f"[bold {PURPLE}]{number:02d}   {title}[/]"
    )


def get_file_path():
    display_section(1, "SELECT FILE")

    while True:
        raw_path = Prompt.ask("Full file path")
        file_path = Path(raw_path.strip().strip('"').strip("'"))

        if not file_path.is_file():
            console.print(f"[{RED}]File not found.[/]")
            continue

        extension = file_path.suffix.lower()
        if extension not in FILE_TYPES:
            console.print(f"[{RED}]Unsupported file format.[/]")
            continue

        if extension not in EDITORS:
            console.print( "[yellow]This format is not implemented yet.[/]")
            continue

        console.print( f"[{GREEN}]Detected: {FILE_TYPES[extension]}[/]")
        return file_path


def get_target_date():
    display_section(2, "TARGET TIMESTAMP")

    while True:
        value = Prompt.ask("Date (YYYY-MM-DD HH:MM)")

        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            console.print(f"[{RED}]Invalid date format.[/]")


def create_table():
    table = Table.grid(padding=(0, 2))
    table.add_column(style="#A3A7B7", width=17)
    table.add_column(style="white", overflow="fold")
    return table


def confirm_operation(file_path, target_date):
    display_section(3, "CONFIRM OPERATION")

    table = create_table()
    table.add_row("File", file_path.name)
    table.add_row("Format", FILE_TYPES[file_path.suffix.lower()])
    table.add_row("Target timestamp", target_date.strftime("%Y-%m-%d %H:%M:%S"),)

    console.print(
        Panel(
            table,
            title=f"[bold {LIGHT_PURPLE}]Operation Summary[/]",
            border_style=PURPLE,
            style=f"on {BACKGROUND}",
            width=panel_width(),
            padding=(1, 2),
        )
    )

    return Confirm.ask("Proceed?")


def display_result(file_path, target_date):
    stats = file_path.stat()

    timestamps = {
        "Created": datetime.fromtimestamp(getattr(stats, "st_birthtime", stats.st_ctime)),
        "Modified": datetime.fromtimestamp(stats.st_mtime),
        "Accessed": datetime.fromtimestamp(stats.st_atime),
    }

    table = create_table()
    all_match = True

    for label, value in timestamps.items():
        matches = abs((value - target_date).total_seconds()) < 1
        all_match = all_match and matches

        color = GREEN if matches else RED
        status = "OK" if matches else "MISMATCH"

        table.add_row(label, f"[{color}]{value:%Y-%m-%d %H:%M:%S}  {status}[/]",)

    title = "Filesystem timestamps verified" if all_match else "Check timestamps"
    border = GREEN if all_match else "yellow"

    console.print()
    console.print(
        Panel(
            table,
            title=f"[bold]{title}[/]",
            border_style=border,
            style="on #172922" if all_match else "on #302819",
            width=panel_width(),
            padding=(1, 2),
        )
    )

    console.print(f"[dim]Output: {file_path}[/]")
    console.print(
        "[dim]Verification reflects timestamps immediately "
        "after editing.[/]"
    )


def process_file(file_path, target_date):
    editor = EDITORS[file_path.suffix.lower()]

    try:
        with console.status(f"[{PURPLE}]Updating metadata...[/]"):
            output = editor(file_path, target_date) # Update internal file metadata
            edit_filesystem(output, target_date)    # Update Windows filesystem timestamps

        display_result(output, target_date)

    except Exception as error:
        console.print()
        console.print(
            Panel(
                Text(str(error), style=RED),
                title="Operation failed",
                border_style=RED,
                width=panel_width(),
            )
        )


def main():
    display_header()

    while True:
        file_path = get_file_path()
        target_date = get_target_date()

        if confirm_operation(file_path, target_date):
            process_file(file_path, target_date)
        else:
            console.print("[yellow]Operation cancelled.[/]")

        if not Confirm.ask("\nEdit another file?"):
            console.print(f"\n[{PURPLE}]Goodbye![/]")
            break


if __name__ == "__main__":
    main()
