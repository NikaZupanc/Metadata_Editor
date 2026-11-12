# Metadata_Editor
A Python-based CLI tool for editing and analyzing metadata and timestamps in JPEG, PDF, DOCX, and XLSX files for digital forensic research.

## Requirements

Before running the application, make sure the following dependencies are installed.

### 1. Python 3.14+

Download Python from [python.org](https://www.python.org/downloads/) or install it using PowerShell:

```powershell
winget install --id Python.Python.3.14 --exact
```

Verify the installation:

```powershell
py -3.14 --version
```

### 2. ExifTool

ExifTool is required for reading and modifying image metadata.

Install it using PowerShell:

```powershell
winget install --id OliverBetz.ExifTool --exact
```

Restart your terminal and verify the installation:

```bash
exiftool -ver
```

**Note:** ExifTool must be available in your system's `PATH`.

### 3. Git Bash

Git Bash is required to execute the provided `run.sh` script on Windows.

Download [Git for Windows](https://git-scm.com/downloads/win).

### 4. Python Dependencies

The application uses the following Python package:

- `rich` – Colored terminal interface, interactive prompts and formatted output.

Python dependencies are listed in `requirements.txt`:

```text
rich
```

They can be installed manually:

```bash
python -m pip install -r requirements.txt
```

The startup script automatically installs the currently required dependency if it is missing.

## Installation

Clone the repository:

```bash
git clone https://github.com/NikaZupanc/Metadata_Editor.git
cd Metadata_Editor
```

## Usage

Launch the application using Git Bash:

```bash
./run.sh
```

The startup script automatically:

1. Creates a Python virtual environment (`.venv`) if needed.
2. Installs the required Python dependencies.
3. Launches the interactive CLI.

Follow the on-screen instructions to select a file, specify a target timestamp and confirm the operation.

## Supported Formats

| Format | Status |
|---|---|
| JPEG (.jpg, .jpeg) | Supported |
| Word (.docx) | Planned |
| Excel (.xlsx) | Planned |
| PDF (.pdf) | Planned |

Currently, JPEG editing supports the three main EXIF date fields. Other embedded metadata and filesystem timestamps are not yet handled.

## Notes

- The original file is preserved.
- Modified files are saved with the `_modified` suffix.
- The `.venv` directory should not be committed to Git.
- Intended for educational and digital forensic research purposes.