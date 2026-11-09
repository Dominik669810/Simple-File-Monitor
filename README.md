# Basic File Integrity Monitor

A small Python program that watches a folder and alerts you when a file is
created, modified or deleted, It detects modifications by comparing
the file's SHA-256 hashes so it notices any change to the file's contents.

## Example

```
Baseline created: 0 files hashed
Checking 'test_folder' every 2 seconds (press Ctrl+C to stop)
10:51:04  [NEW]  test_folder/notes.txt
10:51:06  [MODIFIED]  test_folder/notes.txt  (hash 5891b5b522d5... -> 75ecc33bdd08...)
10:51:08  [NEW]  test_folder/renamed.txt
10:51:08  [DELETED]  test_folder/notes.txt
10:51:14  [DELETED]  test_folder/renamed.txt
```

## How to run

Requires Python 3.

- **VS Code:** open this folder, open `file_monitor.py` and press Run.
- **Terminal:** `python3 file_monitor.py`

It watches a folder called `test_folder`, creating it if it doesn't exist.
Add, edit or delete files in it and the alerts appear within 2 seconds. Press
**Ctrl+C** to stop. To watch a different folder, change `FOLDER` at the top of
the file.

## How it works

1. **Baseline:** it goes through every file in the folder (`os.walk`),
   calculates each file's SHA-256 hash (a fingerprint of its contents) with
   `hashlib`, and stores them in a dictionary: `{file path: hash}`.

2. **Checking:** every 2 seconds it scans the folder again, which produces a
   new dictionary, and compares the two:
   - path in the new scan but not the old one → **NEW**
   - path in both, but the hashes differ → **MODIFIED**
   - path in the old scan but not the new one → **DELETED**

3. The new scan becomes the one to compare against next time.

A renamed file shows up as one **DELETED** (old name) and one **NEW** (new name).
Only the contents matter: opening a file or changing its timestamp doesn't change
its hash, so it doesn't cause an alert.

## Known limitations and future improvements

The things I can improve next to make this Monitor better are:

| Limitation | Improvement |

| Re-reads every file every 2 seconds, which gets slow for big folders | Only re-hash files whose size or modified time changed, or have the operating system report changes (e.g. the `watchdog` library) |

| A file changed and changed back within 2 seconds isn't noticed | Check more often, or use operating-system change notifications |

| Hashes are only kept in memory, so changes made while it isn't running are missed | Save the baseline to a file (`json`) or database (`sqlite3`) |

| Each change becomes the new "normal" after one alert, so an attacker's change is accepted | Keep the original baseline and only update it when a person approves the change |

| If the baseline were saved to disk, an attacker could edit it too | Sign each record with an HMAC (`hmac` module, which uses a secret key) |

| Reads each whole file into memory, which is a problem for very large files | Hash files in small chunks |

| Alerts are only printed to the screen | Write them to a log file (`logging`) or send an email |

| Doesn't notice permission changes | Also compare file permissions (`os.stat`) |

| Shows *that* a file changed, not *who* changed it | Use the operating system's audit logs |
