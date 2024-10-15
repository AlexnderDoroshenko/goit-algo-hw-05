from typing import List, Tuple, Optional


def binary_search(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """Perform binary search on a sorted array.

    Parameters:
    arr: A list of sorted floating-point numbers.
    target: The target value to search for.

    Returns:
    A tuple containing the number of iterations and the "upper bound".
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] == target:
            return (iterations, arr[mid])  # Found exact value
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    upper_bound = arr[left] if left < len(arr) else None
    return (iterations, upper_bound)

# Testing binary search


def test_binary_search():
    arr = [1.0, 2.5, 3.5, 4.3, 5.9]
    assert binary_search(arr, 3.5) == (1, 3.5), f"6.0 search result {
        binary_search(arr, 3.5)} not equal to (1, 3.5)"
    assert binary_search(arr, 4.0) == (2, 4.3), f"4.0 search result {
        binary_search(arr, 4.0)} not equal to (2, 4.3)"
    assert binary_search(arr, 6.0) == (3, None), f"6.0 search result {
        binary_search(arr, 6.0)} not equal to (3, None)"


test_binary_search()
print("Binary search passed testing.")
