from collections import Counter
from pathlib import Path
from fastapi import UploadFile
import string

def parse_text_into_words(text: str) -> list[tuple[str, int]]:
    # Remove pontuação do início e final de cada palavra
    words = text.lower().strip().split()
    cleaned_words = [word.strip(string.punctuation) for word in words]

    # Filtra palavras vazias que podem resultar da limpeza
    cleaned_words = [word for word in cleaned_words if word]

    return list(Counter(cleaned_words).items())

def parse_text_into_pages(text: str, words_per_page: int) -> list[str]:
    words = text.lower().strip().split()
    pages = [' '.join(words[i:i+words_per_page]) for i in range(0, len(words), words_per_page)]
    return pages

def get_text_total_words(text: str) -> int:
    words = text.lower().strip().split()
    cleaned_words = [word.strip(string.punctuation) for word in words]
    cleaned_words = [word for word in cleaned_words if word]
    unique_words = set(cleaned_words)
    return len(unique_words)

def save_upload_file(upload: UploadFile, base_dir: str, basename: str) -> str:
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
            chunk = upload.file.read(50024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    return str(path)
