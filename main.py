
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from image_editor import edit_image


console = Console()

# Supported file formats and their editors
EDITORS = {
    ".jpg": edit_image,
    ".jpeg": edit_image,
    # ".docx": edit_word,
    # ".xlsx": edit_excel,
    # ".pdf": edit_pdf,
}

FILE_TYPES = {
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".docx": "Word Document",
    ".xlsx": "Excel Spreadsheet",
    ".pdf": "PDF Document",
}


def display_header():
    console.print(
        Panel(
            "[bold #C4B5FD]METADATA EDITOR[/]\n"
            "[dim]File Metadata Manipulation Tool[/]",
            border_style="#A78BFA",
            padding=(1, 4),
        )
    )


def get_file_path():
    console.print("\n[bold #A78BFA]01 / SELECT FILE[/]")

    while True:
        raw_path = Prompt.ask("Enter file path")
        file_path = Path(raw_path.strip().strip('"').strip("'"))

        if not file_path.is_file():
            console.print("[red]File not found. Try again.[/]")
            continue

        extension = file_path.suffix.lower()

        if extension not in FILE_TYPES:
            console.print("[red]Unsupported file format.[/]")
            continue

        if extension not in EDITORS:
            console.print(
                "[yellow]This format is not implemented yet.[/]"
            )
            continue

        console.print(
            f"[green]Detected: {FILE_TYPES[extension]}[/]"
        )

        return file_path


def get_target_date():
    console.print("\n[bold #A78BFA]02 / TARGET DATE[/]")

    while True:
        value = Prompt.ask(
            "Enter date and time (YYYY-MM-DD HH:MM)"
        )

        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            console.print("[red]Invalid date format. Try again.[/]")


def confirm_operation(file_path, target_date):
    console.print("\n[bold #A78BFA]03 / CONFIRM OPERATION[/]")

    table = Table(show_header=False, box=None)
    table.add_column("Property", style="dim")
    table.add_column("Value", style="white")

    table.add_row("File", file_path.name)
    table.add_row("Format", FILE_TYPES[file_path.suffix.lower()])
    table.add_row(
        "Target date",
        target_date.strftime("%Y-%m-%d %H:%M:%S"),
    )

    console.print(
        Panel(table, title="Operation Summary", border_style="#A78BFA")
    )

    return Confirm.ask("Proceed?", default=False)


def process_file(file_path, target_date):
    extension = file_path.suffix.lower()
    editor = EDITORS[extension]

    try:
        with console.status("[cyan]Updating metadata...[/]"):
            output = editor(file_path, target_date)

        console.print(
            Panel(
                f"[green]Metadata updated successfully![/]\n"
                f"[dim]Output: {output}[/]",
                border_style="green",
            )
        )

    except Exception as error:
        console.print(f"[red]Error:[/] {error}")


def main():
    display_header()

    while True:
        file_path = get_file_path()
        target_date = get_target_date()

        if confirm_operation(file_path, target_date):
            process_file(file_path, target_date)
        else:
            console.print("[yellow]Operation cancelled.[/]")

        if not Confirm.ask("\nEdit another file?", default=False):
            console.print("\n[dim]Goodbye![/]")
            break


if __name__ == "__main__":
    main()
