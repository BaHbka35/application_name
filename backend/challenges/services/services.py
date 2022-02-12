import os


def delete_existing_file(file_path: str) -> None:
    """Deletes existing file."""
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
