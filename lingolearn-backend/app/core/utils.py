from collections import Counter

def parse_text_into_words(text:str) -> list[tuple[str, int]]:
    words = text.lower().strip().split()
    return list(Counter(words).items())

def parse_text_into_pages(text: str, words_per_page: int) -> list[str]:
    words = text.lower().strip().split()
    pages = [' '.join(words[i:i+words_per_page]) for i in range(0, len(words), words_per_page)]
    return pages

def get_text_total_words(text:str) -> int:
    words = text.lower().strip().split()
    unique_words = set(words)
    return len(unique_words)