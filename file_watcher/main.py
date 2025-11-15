
import argparse
from script import file_watcher


def main():
    parser = argparse.ArgumentParser(description="File Watcher Utility")

    parser.add_argument("--hours", type=float, required=True, help="Total hours to watch")
    parser.add_argument("--interval", type=int, required=True, help="Interval in seconds")
    parser.add_argument("--file", required=True, help="File path to monitor")

    args = parser.parse_args()

    file_watcher(args.file, args.hours, args.interval)


if __name__ == "__main__":
    main()
