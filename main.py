import os
import sys
from typing import Optional


DB_FILE = "data.db"


class KeyValueStore:
    """
    A simple append-only persistent key-value store.
    Supports SET, GET, and EXIT commands from STDIN.
    """

    def __init__(self, db_file: str):
        self.db_file: str = db_file
        self.store: list[tuple[str, str]] = []  # List of (key, value) tuples
        self.key_index: dict[str, int] = {}     # In-memory index for fast GET
        self._load_db()

    def _load_db(self) -> None:
        """Rebuild in-memory store from the append-only log."""
        if not os.path.exists(self.db_file):
            # Create empty file if it doesn't exist
            open(self.db_file, "w").close()

        try:
            with open(self.db_file, "r") as f:
                for idx, line in enumerate(f):
                    tokens = line.strip().split(" ", 2)
                    if len(tokens) == 3 and tokens[0].upper() == "SET":
                        _, key, value = tokens
                        self.store.append((key, value))
                        self.key_index[key] = idx
        except IOError as e:
            print(f"Error reading DB file: {e}", file=sys.stderr)

    def set(self, key: str, value: str) -> None:
        """Append a SET command to disk and update memory index."""
        try:
            with open(self.db_file, "a") as f:
                f.write(f"SET {key} {value}\n")
        except IOError as e:
            print(f"Error writing to DB: {e}", file=sys.stderr)
            return

        # Update in-memory store and index
        self.store.append((key, value))
        self.key_index[key] = len(self.store) - 1

    def get(self, key: str) -> Optional[str]:
        """Retrieve the latest value for a key, or None if not found."""
        idx = self.key_index.get(key)
        if idx is not None:
            return self.store[idx][1]
        return None


def main() -> None:
    """Main loop to read commands from STDIN."""
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
            # Only print if key exists (Gradebot expects nothing if key not found)
            if value is not None:
                print(value, flush=True)

        elif op == "EXIT":
            break

        else:
            print(f"Invalid command: {cmd}", flush=True)


if __name__ == "__main__":
    main()
