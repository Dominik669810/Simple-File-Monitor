"""
Basic File Integrity Monitor 

Every few seconds it hashes every file in a folder and compares the hashes
with the previous check, to find files that were created, modified or deleted.
"""

import hashlib
import os
import time

FOLDER = "test_folder"  # the folder to watch 
CHECK_EVERY = 2         # seconds to wait between checks


def hash_file(path):
    """Return the SHA-256 hash of a file's contents."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def scan(folder):
    """Hash every file in the folder. Returns a dictionary of {path: hash}."""
    hashes = {}
    for root, dirs, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                hashes[path] = hash_file(path)
            except OSError:
                pass  # the file was deleted or locked while we were scanning
    return hashes


def alert(kind, path, detail=""):
    """Print a timestamped alert, e.g. 14:02:31  [MODIFIED]  test_folder/notes.txt"""
    print(f"{time.strftime('%H:%M:%S')}  [{kind}]  {path}  {detail}")


def compare(old, new):
    """Compare two scans and print an alert for every difference."""
    for path in new:
        if path not in old:
            alert("NEW", path)
        elif new[path] != old[path]:
            alert("MODIFIED", path, f"(hash {old[path][:12]}... -> {new[path][:12]}...)")

    for path in old:
        if path not in new:
            alert("DELETED", path)


def main():
    if not os.path.isdir(FOLDER):
        os.makedirs(FOLDER)
        print(f"Created the folder '{FOLDER}'")

    previous = scan(FOLDER)
    print(f"Baseline created: {len(previous)} files hashed")
    print(f"Checking '{FOLDER}' every {CHECK_EVERY} seconds (press Ctrl+C to stop)")

    try:
        while True:
            time.sleep(CHECK_EVERY)
            current = scan(FOLDER)
            compare(previous, current)
            previous = current  # the next check compares against this one
    except KeyboardInterrupt:  # Ctrl+C
        print("Stopped")


if __name__ == "__main__":
    main()
