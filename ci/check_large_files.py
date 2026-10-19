import os
import subprocess
import sys

MAX_SIZE = 100 * 1024 * 1024  # 100 MB


def main():
    files = subprocess.check_output(
        ["git", "ls-files", "-z"]
    ).decode().split("\0")

    oversized = []

    for file in filter(None, files):
        if os.path.isfile(file) and os.path.getsize(file) > MAX_SIZE:
            oversized.append(file)

    if oversized:
        print("ERROR: Files larger than 100 MB detected:")
        for file in oversized:
            print(f"  {file}")
        sys.exit(1)

    print("No tracked files larger than 100 MB detected.")


if __name__ == "__main__":
    main()