# Math CLI project 

This project provides a CLI interface for basic mathematical operations (`pow`, `fibonacci`, `factorial`) with result persistence in SQLite and a real asynchronous worker that processes tasks from a persistent queue (`task_queue`). It also includes **caching logic**: if a task was already processed in the past, its result is returned directly from the database without recalculating it.

---

## Features

| Functionality                          | Status |
|---------------------------------------|--------|
| CLI with `click`                      | ✅     |
| Operations: `pow`, `fib`, `factorial` | ✅     |
| Result storage in SQLite              | ✅     |
| History listing (`history` command)   | ✅     |
| Asynchronous task submission          | ✅     |
| Background worker (`worker.py`)       | ✅     |
| Persistent queue (`task_queue`)       | ✅     |
| Smart caching (reuse previous results)| ✅     |
| Input validation with `pydantic`      | ✅     |
| Clean MVCS code structure + `flake8`  | ✅     |

---

## Requirements

- Python 3.10 or 3.11
- Cross-platform: Windows / Linux / macOS
- No Docker, Redis, or web framework needed

## Usage
1. Direct execution (synchronous mode)
- python -m math_cli.main pow 2 5
- python -m math_cli.main fib 10
- python -m math_cli.main factorial 6

2. Submit tasks to background worker
- python -m math_cli.main submit-pow 3 4
- python -m math_cli.main submit-fib 8
- python -m math_cli.main submit-factorial 5

3. Start the worker (in a separate terminal)
- python -m math_cli.worker

4. View operation history
- python -m math_cli.main history

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # On Windows
source .venv/bin/activate       # On Linux/macOS

pip install -r requirements.txt
