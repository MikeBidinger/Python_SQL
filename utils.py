import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMAT = "%Y-%m-%d"


def file_selection_dialog(
    file_types: list[tuple[str, str]] = [("All Files", "*.*")],
    title: str = "",
    initial_dir: str = "",
) -> str:
    # Display a file selection dialog
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=file_types, initialdir=initial_dir, title=title, parent=root
    )
    root.destroy()
    if file_path == "":
        quit()
    return file_path


def read_csv(
    file_path: str, delimiter: str = ";", mode: str = "r", encoding=None
) -> list[list]:
    matrix = []
    # Open the file from the given path in the specified mode
    with open(file_path, mode, encoding=encoding) as f:
        # Create a CSV reader
        reader = csv.reader(f, delimiter=delimiter)
        # Read each row from the CSV file and append it to the matrix to be returned
        for row in reader:
            matrix.append(row)
    return matrix


def read_sql(file_path: str, mode: str = "r", encoding=None) -> list[str]:
    rows = []
    # Open the file from the given path in the specified mode
    with open(file_path, mode, encoding=encoding) as f:
        # Read each row from the SQL file and append it to list to be returned
        for row in f:
            rows.append(row.rsplit("\n", 1)[0])
    return rows


def is_datetime(date_str: str):
    # Check if given string is of datetime format
    result = True
    try:
        res = bool(datetime.datetime.strptime(date_str, DATETIME_FORMAT))
    except ValueError:
        result = False
    return result


def is_date(date_str: str):
    # Check if given string is of date format
    result = True
    try:
        res = bool(datetime.datetime.strptime(date_str, DATE_FORMAT))
    except ValueError:
        result = False
    return result


def write_file(content: str, file_path: str, mode: str = "w") -> str:
    # Write given content to the specified file path
    with open(file_path, mode) as f:
        f.write(content)
    return file_path


def write_csv(
    matrix: list[list], file_path: str, delimiter: str = ";", mode: str = "w"
) -> str:
    # Write given matrix to the specified file path
    with open(file_path, mode) as f:
        csv_writer = csv.writer(f, delimiter=delimiter)
        for row in matrix:
            csv_writer.writerow(row)
    return file_path


def prompt_message(title: str, message: str):
    # Display a message box with the given title and message
    print(message)
    root = tk.Tk()
    root.wm_attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(title, message, parent=root)
    root.destroy()


def format_string(string: str) -> str:
    # Remove quotes and set to lowercase
    return unquote(string).lower()


def unquote(string: str) -> str:
    # Remove quotes from the given string if present
    result = string
    if (string.startswith('"') and string.endswith('"')) or (
        string.startswith("'") and string.endswith("'")
    ):
        result = string[1:-1]
    return result
