# Kv_Store

**CSCE 5350 – Project 1: Simple Key-Value Store**  

A simple persistent key-value store implemented in Python. Supports `SET`, `GET`, and `EXIT` commands via a command-line interface (CLI). This project demonstrates basic database concepts, persistent storage, and integration with the CSCE 5350 Gradebot automated testing system.

---

## Features

- **Append-Only Persistence**: All writes are saved immediately to `data.db` using an append-only log.
- **In-Memory Indexing**: Optimized retrieval of keys using an in-memory index.
- **Command-Line Interface**: Interactive commands:
  - `SET <key> <value>` – store or overwrite a key.
  - `GET <key>` – retrieve the latest value for a key.
  - `EXIT` – exit the program.
- **Data Persistence**: Data remains consistent across program restarts.
- **Gradebot-Ready**: Fully compatible with CSCE 5350 automated grading.

---

## Requirements

- Python 3.7 or higher
- Git (optional, for version control)

---

## Usage

1. **Clone the repository**:
```bash
git clone https://github.com/srinath748/kvstore.git
cd kvstore
```
2. **Run the key-value store**:
   ```bash
   python main.py
   ```
3. **Enter commands in the terminal**:
   ```bash
    SET key1 value1
    GET key1
    EXIT
   ```
    ##Project Structure
    ```bash
    Kv_Store/
        ├─ main.py          # Main program implementing the key-value store
        ├─ data.db          # Append-only database file (created automatically)
        ├─ gradebot.exe     # Gradebot client for automated testing
        ├─ README.md        # Project documentation

   ```
## Testing with Gradebot:
    Run automated tests using Gradebot:
        ```bash
        .\gradebot.exe project-1 --dir "." --run "python main.py"
      ```
    The grader checks:

- Creation of data.db
- SET and GET functionality
- Overwriting existing keys
- Handling nonexistent keys
- Persistence after restart
- Code quality and style

## Gradebot Result
![Gradebot Screenshot](Screenshot (593).png)
![Gradebot Screenshot](Screenshot (594).png)

Score: 94% – fully functional and persistent key-value store

## Improvements
- Added type hints for clarity.
- Optimized GET operation using in-memory index for faster lookups.
- Improved error handling for file operations.
- Compatible with automated Gradebot black-box testing.

## Author

Name: Srinath Reddy

EUID: 21545

Course: CSCE 5350 – Build Your Own Database

## License

This project is for educational purposes in CSCE 5350.