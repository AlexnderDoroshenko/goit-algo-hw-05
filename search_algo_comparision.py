import timeit


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

Testing algorithms for text length 84 and pattern 'substring':
Boyer-Moore: 0.00371 seconds
KMP: 0.00581 seconds
Rabin-Karp: 0.01329 seconds

Testing algorithms for text length 57 and pattern 'example':
Boyer-Moore: 0.00233 seconds
KMP: 0.00297 seconds
Rabin-Karp: 0.00643 seconds

Testing algorithms for text length 84 and pattern 'nonexistent':
Boyer-Moore: 0.00497 seconds
KMP: 0.01530 seconds
Rabin-Karp: 0.03015 seconds

Testing algorithms for text length 57 and pattern 'randompattern':
Boyer-Moore: 0.00274 seconds
KMP: 0.00891 seconds
Rabin-Karp: 0.01956 seconds

Testing algorithms for text length 6300 and pattern 'abcabc':
Boyer-Moore: 0.00147 seconds
KMP: 0.00195 seconds
Rabin-Karp: 0.00255 seconds

Testing algorithms for text length 6300 and pattern 'abc':
Boyer-Moore: 0.00106 seconds
KMP: 0.00109 seconds
Rabin-Karp: 0.00174 seconds

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
