import os
import sys

DB_FILE = "data.db"


class KeyValueStore:
    """
    A simple persistent key-value store using an append-only log file.
    Supports SET, GET, and EXIT commands via STDIN.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.index = []  # store (key, value) tuples
        self._load_log()

    def _load_log(self):
        """Rebuild in-memory index by replaying the append-only log."""
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()
            return

        with open(self.db_path, "r") as db:
            for line in db:
                tokens = line.strip().split(" ", 2)
                if len(tokens) == 3 and tokens[0].upper() == "SET":
                    _, key, value = tokens
                    self._insert_or_update(key, value)

    def _insert_or_update(self, key, value):
        """Insert new key or replace the existing key’s value."""
        for i, (k, _) in enumerate(self.index):
            if k == key:
                self.index[i] = (key, value)
                return
        self.index.append((key, value))

    def set(self, key, value):
        """Write a SET command to disk and update memory."""
        with open(self.db_path, "a") as db:
            db.write(f"SET {key} {value}\n")
        self._insert_or_update(key, value)

    def get(self, key):
        """Return latest value for a key, or None if not found."""
        for k, v in reversed(self.index):
            if k == key:
                return v
        return None


def main():
    kv = KeyValueStore(DB_FILE)

    for line in sys.stdin:
        cmd = line.strip()
        if not cmd:
            continue

        parts = cmd.split(" ", 2)
        op = parts[0].upper()

        if op == "SET" and len(parts) == 3:
            kv.set(parts[1], parts[2])
        elif op == "GET" and len(parts) == 2:
            val = kv.get(parts[1])
            print(val if val is not None else "NULL")
        elif op == "EXIT":
            print("Exiting...")
            break
        else:
            print(f"Invalid command: {cmd}")


if __name__ == "__main__":
    main()
