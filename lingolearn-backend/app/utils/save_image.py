from pathlib import Path

from fastapi import UploadFile


def _save_upload_file(upload: UploadFile, base_dir: str, basename: str) -> str:
    """
    Saves an UploadFile to disk under base_dir with a sanitized basename.
    Returns the absolute path as string.
    """
    dest_dir = Path(base_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename or "").suffix or ".bin"
    path = dest_dir / f"{basename}{suffix}"
    # stream to disk
    with path.open("wb") as f:
        while True:
            chunk = upload.file.read(5024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return str(path)