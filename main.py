import os
import sys

DB_FILE = "data.db"


class KeyValueStore:
    """
    A simple append-only persistent key-value store.
    Supports SET, GET, and EXIT commands from STDIN.
    """

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.store = []  # List of (key, value) tuples
        self._load_db()

    def _load_db(self) -> None:
        """Rebuild in-memory store from the log file."""
        if not os.path.exists(self.db_file):
            # create empty file if it doesn't exist
            with open(self.db_file, "w") as f:
                pass

        with open(self.db_file, "r") as f:
            for line in f:
                tokens = line.strip().split(" ", 2)
                if len(tokens) == 3 and tokens[0].upper() == "SET":
                    _, key, value = tokens
                    self._update_in_memory(key, value)

    def _update_in_memory(self, key: str, value: str) -> None:
        """Insert a new key or update existing key in memory."""
        for i, (k, _) in enumerate(self.store):
            if k == key:
                self.store[i] = (key, value)
                return
        self.store.append((key, value))

    def set(self, key: str, value: str) -> None:
        """Append a SET command to disk and update memory."""
        with open(self.db_file, "a") as f:
            f.write(f"SET {key} {value}\n")
        self._update_in_memory(key, value)

    def get(self, key: str) -> str | None:
        """Retrieve the latest value for a key, or None if not found."""
        for k, v in reversed(self.store):
            if k == key:
                return v
        return None


def main():
    kv_store = KeyValueStore(DB_FILE)

    for line in sys.stdin:
        cmd = line.strip()
        if not cmd:
            continue

        parts = cmd.split(" ", 2)
        op = parts[0].upper()

        if op == "SET" and len(parts) == 3:
            key, value = parts[1], parts[2]
            kv_store.set(key, value)
        elif op == "GET" and len(parts) == 2:
            key = parts[1]
            value = kv_store.get(key)
            print(value if value is not None else "NULL", flush=True)
        elif op == "EXIT":
            break
        else:
            print(f"Invalid command: {cmd}", flush=True)


if __name__ == "__main__":
    main()
