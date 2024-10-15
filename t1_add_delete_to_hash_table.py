class HashTable:
    def __init__(self, size: int = 10):
        """Initialize a hash table with the given size."""
        self.size = size
        self.table: list[tuple[str, any]] = [None] * size

    def hash_function(self, key: str) -> int:
        """Compute the hash for a given key."""
        return hash(key) % self.size

    def insert(self, key: str, value: any) -> None:
        """Add a key-value pair to the table."""
        index = self.hash_function(key)
        self.table[index] = (key, value)

    def delete(self, key: str) -> bool:
        """Remove a key-value pair from the table by the given key."""
        index = self.hash_function(key)
        if self.table[index] is not None and self.table[index][0] == key:
            self.table[index] = None
            return True
        return False

    def __str__(self) -> str:
        """Return a string representation of the hash table."""
        return str(self.table)

    def __len__(self) -> int:
        """Return a string representation of the hash table."""
        return len(self.table)

# Testing HashTable


def test_hash_table():
    ht = HashTable()
    ht.insert("a", 1)
    ht.insert("b", 2)
    assert ht.delete("a"), "a key was not deleted"
    assert not ht.delete("c"), "c key was deleted"  # Non-existent key
    assert f"{("b", 2)}" in str(ht), f"Hash table {
        str(ht)} not contains the key 'b'"
    assert f"{("a", 1)}" not in str(ht), f"Hash table {
        str(ht)} contains the key 'a'"
    assert len(ht) == 10, "The has table len not equal to 10"


test_hash_table()
print("HashTable passed testing.")
