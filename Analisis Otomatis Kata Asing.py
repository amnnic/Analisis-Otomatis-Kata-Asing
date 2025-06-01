import re

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    shift = {}

    for i in range(m):
        shift[pattern[i]] = m - i - 1

    for i in range(256):
        if chr(i) not in shift:
            shift[chr(i)] = m

    i = m - 1
    while i < n:
        j = m - 1
        while j >= 0 and text[i] == pattern[j]:
            i -= 1
            j -= 1

        if j == -1:
            yield i + 1
            i += m  
        else:
            i += shift.get(text[i], m)

def load_indonesian_words(filename):
    with open(filename, encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

indonesian_words = load_indonesian_words("kamus_bahasa_indonesia.txt")

def is_indonesian(word):
    return word.lower() in indonesian_words

def italicize_foreign_words_markdown(essay):
    result = ""
    last_idx = 0

    word_pattern = r"\b\w+\b"
    start_idx = 0

    while start_idx < len(essay):
        for match_start in boyer_moore_search(essay[start_idx:], word_pattern):
            word = essay[start_idx + match_start:start_idx + match_start + len(word_pattern)]
            if not is_indonesian(word):
                result += essay[last_idx:start_idx + match_start]
                result += f"*{word}*"
                last_idx = start_idx + match_start + len(word)
        start_idx += 1

    result += essay[last_idx:]
    return result

print("Masukkan esai kamu (akhiri dengan baris kosong):")
lines = []
while True:
    try:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    except EOFError:
        break

essay = "\n".join(lines)

hasil = italicize_foreign_words_markdown(essay)

print("\n=== Hasil Essay dengan Kata Asing Diitalic ===\n")
print(hasil)
