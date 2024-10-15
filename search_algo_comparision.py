import timeit
import pathlib
import random


def boyer_moore(text: str, pattern: str) -> bool:
    """Implementation of the Boyer-Moore algorithm for substring search."""
    if not pattern:
        return True
    if len(pattern) > len(text):
        return False

    # Preprocessing: Create the bad character heuristic
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i

    s = 0  # shift of the pattern
    while s <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return True
        s += max(1, j - bad_char.get(text[s + j], -1))
    return False


def knuth_morris_pratt(text: str, pattern: str) -> bool:
    """Implementation of the Knuth-Morris-Pratt algorithm for substring search."""
    if not pattern:
        return True
    if len(pattern) > len(text):
        return False

    # Preprocessing: Create the longest prefix suffix (LPS) array
    lps = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while (j > 0 and pattern[i] != pattern[j]):
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i, j = 0, 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return True
        else:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1
    return False


def rabin_karp(text: str, pattern: str) -> bool:
    """Implementation of the Rabin-Karp algorithm for substring search."""
    if not pattern:
        return True
    if len(pattern) > len(text):
        return False

    base = 256  # Number of characters in the input alphabet
    prime = 101  # A prime number to avoid overflow
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(len(pattern) - 1):
        h = (h * base) % prime

    for i in range(len(pattern)):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        text_hash = (base * text_hash + ord(text[i])) % prime

    for i in range(len(text) - len(pattern) + 1):
        if pattern_hash == text_hash:
            if text[i:i + len(pattern)] == pattern:
                return True
        if i < len(text) - len(pattern):
            text_hash = (
                base * (text_hash - ord(text[i]) * h)
                + ord(text[i + len(pattern)])) % prime
            text_hash = (text_hash + prime) % prime  # Ensure positive
    return False

# Efficiency Check Function


def measure_efficiency(text: str, pattern: str) -> None:
    """Measure the efficiency of substring search algorithms."""
    print(f"Testing algorithms for text length {
        len(text)} and pattern '{pattern}':")

    bm_time = timeit.timeit(lambda: boyer_moore(text, pattern), number=1000)
    kmp_time = timeit.timeit(
        lambda: knuth_morris_pratt(text, pattern), number=1000)
    rk_time = timeit.timeit(lambda: rabin_karp(text, pattern), number=1000)

    print(f"Boyer-Moore: {bm_time:.5f} seconds")
    print(f"KMP: {kmp_time:.5f} seconds")
    print(f"Rabin-Karp: {rk_time:.5f} seconds")
    print()


def read_file(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        b_data = file.read()
        try:
            return b_data.decode('utf-8')
        except UnicodeDecodeError:
            return b_data.decode('windows-1251')


TEST_DATA_DIR = (pathlib.Path(__file__).parent).joinpath("test_data")

# Define file paths
file_path1 = pathlib.PurePath(TEST_DATA_DIR, "file1.txt")
file_path2 = pathlib.PurePath(TEST_DATA_DIR, "file2.txt")

# Read contents from files
text1 = read_file(file_path1)
text2 = read_file(file_path2)

# substring pattern from text
substr_len = 10
random_ind_text1 = random.randrange(0, len(text1) - substr_len + 1)
random_ind_text2 = random.randrange(0, len(text2) - substr_len + 1)
text1_pattern = text1[random_ind_text1:random_ind_text1 + substr_len]
text2_pattern = text2[random_ind_text2:random_ind_text2 + substr_len]

# Test with a pattern that exists
measure_efficiency(text1, text1_pattern)
measure_efficiency(text2, text2_pattern)

# Test with a pattern that does not exist
measure_efficiency(text1, "nonexistent")
measure_efficiency(text2, "randompattern")

# Test with the same pattern on both texts
pattern = "пошук"  # Example pattern; adjust based on the content of your files
measure_efficiency(text1, pattern)
measure_efficiency(text2, pattern)


# Example text for testing
text1 = "This is a sample text for substring search. This text is for testing the algorithms."
text2 = "Another example text to test substring search algorithms."

# Creating large test strings
large_text = "abcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabcabc" * 100
large_pattern = "abcabc"

# Test with a pattern that exists
measure_efficiency(text1, "substring")
measure_efficiency(text2, "example")

# Test with a pattern that does not exist
measure_efficiency(text1, "nonexistent")
measure_efficiency(text2, "randompattern")

# Test with large strings
measure_efficiency(large_text, large_pattern)

# Test with a larger pattern
measure_efficiency(large_text, "abc")  # Should match many times


"""
Analysis of Algorithms

Python312/python.exe c:/Users/adore/Neoversity/python/Algorithms/goit-algo-hw-05/search_algo_comparision.py
Testing algorithms for text length 12785 and pattern 'тм пошуку,':
Boyer-Moore: 0.68855 seconds
KMP: 2.22999 seconds
Rabin-Karp: 5.06363 seconds

Testing algorithms for text length 17652 and pattern 'сі додаван':
Boyer-Moore: 0.49175 seconds
KMP: 1.28202 seconds
Rabin-Karp: 2.93947 seconds

Testing algorithms for text length 12785 and pattern 'nonexistent':
Boyer-Moore: 0.83908 seconds
KMP: 2.72634 seconds
Rabin-Karp: 6.12155 seconds

Testing algorithms for text length 17652 and pattern 'randompattern':
Boyer-Moore: 0.80543 seconds
KMP: 2.83406 seconds
Rabin-Karp: 8.38046 seconds

Testing algorithms for text length 12785 and pattern 'пошук':
Boyer-Moore: 0.03877 seconds
KMP: 0.06066 seconds
Rabin-Karp: 0.13780 seconds

Testing algorithms for text length 17652 and pattern 'пошук':
Boyer-Moore: 0.86096 seconds
KMP: 1.36082 seconds
Rabin-Karp: 3.24956 seconds

Testing algorithms for text length 84 and pattern 'substring':
Boyer-Moore: 0.00343 seconds
KMP: 0.00586 seconds
Rabin-Karp: 0.01447 seconds

Testing algorithms for text length 57 and pattern 'example':
Boyer-Moore: 0.00231 seconds
KMP: 0.00313 seconds
Rabin-Karp: 0.00545 seconds

Testing algorithms for text length 84 and pattern 'nonexistent':
Boyer-Moore: 0.00537 seconds
KMP: 0.01192 seconds
Rabin-Karp: 0.03017 seconds

Testing algorithms for text length 57 and pattern 'randompattern':
Boyer-Moore: 0.00391 seconds
KMP: 0.00847 seconds
Rabin-Karp: 0.02081 seconds

Testing algorithms for text length 6300 and pattern 'abcabc':
Boyer-Moore: 0.00155 seconds
KMP: 0.00193 seconds
Rabin-Karp: 0.00250 seconds

Testing algorithms for text length 6300 and pattern 'abc':
Boyer-Moore: 0.00094 seconds
KMP: 0.00107 seconds
Rabin-Karp: 0.00158 seconds

Analysis of Substring Search Algorithms:
--------------------------------------------------
1. Boyer-Moore:
   - Best for large alphabets and long patterns.
   - Efficient due to its heuristic approach that skips sections of the text.
2. Knuth-Morris-Pratt:
   - Best when the pattern is small and has repetitive elements.
   - Uses preprocessing (LPS array) to avoid unnecessary comparisons.
3. Rabin-Karp:
   - Efficient for multiple pattern searches with hashing.
   - Can have performance issues with hash collisions but works well with prime numbers.
"""
