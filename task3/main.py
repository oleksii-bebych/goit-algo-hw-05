import re
import sys
from typing import Optional, Dict, List
from collections import Counter

LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})\s+"
    r"(\d{2}:\d{2}:\d{2})\s+"
    r"([A-Z]+)\s+"
    r"(.*)$"
)

VALID_LEVELS = {"INFO", "DEBUG", "ERROR", "WARNING"}
ORDER = ["INFO", "DEBUG", "ERROR", "WARNING"]

def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    m = LINE_RE.match(line.rstrip("\n"))
    if not m:
        return None
    date, time, level, msg = m.groups()
    return {"date": date, "time": time, "log_level": level, "log_message": msg}

def load_logs(file_path: str) -> List[Dict[str, str]]:
    logs: List[Dict[str, str]] = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                if not line.strip():
                    continue
                parsed = parse_log_line(line)
                if parsed is None:
                    # Можна закоментувати, якщо не хочете попередження
                    print(f"Warning: malformed log line {idx}: {line.strip()}", file=sys.stderr)
                    continue
                logs.append(parsed)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return []
    return logs

def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    return Counter(l["log_level"] for l in logs)

def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    return [l for l in logs if l["log_level"] == level]

def print_table(counts: Dict[str, int]) -> None:
    # Формат рівно як у прикладі
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for lvl in ORDER:
        print(f"{lvl:<16} | {counts.get(lvl, 0):<10}")

def main() -> None:
    if len(sys.argv) == 2:
        # only file
        file_path = sys.argv[1]
        logs = load_logs(file_path)
        if not logs:
            return
        counts = count_logs_by_level(logs)
        print_table(counts)

    elif len(sys.argv) == 3:
        # file + level
        file_path, raw_level = sys.argv[1], sys.argv[2]
        logs = load_logs(file_path)
        if not logs:
            return
        counts = count_logs_by_level(logs)
        print_table(counts)

        level = raw_level.upper()
        if level not in VALID_LEVELS:
            print(f"\nUnknown level '{raw_level}'. Use one of: INFO, DEBUG, ERROR, WARNING.", file=sys.stderr)
            return

        print(f"\nДеталі логів для рівня '{level}':")
        for line in filter_logs_by_level(logs, level):
            print(f"{line['date']} {line['time']} - {line['log_message']}")

    else:
        print("Please provide path to log file")
        print(
            """How to use:
            python main.py /path/to/logfile.log
            python main.py /path/to/logfile.log error"""
        )      

if __name__ == "__main__":
    main()
