#!/usr/bin/env python3
import time
import random
import sys

def main():
    try:
        print("Loading grid topology data...")
        time.sleep(0.8)

        print("Parsing node definitions (256 nodes detected)")
        time.sleep(0.6)

        print("Validating interconnections...")
        time.sleep(0.5)

        if random.random() < 0.15:
            raise Exception("Corrupted topology file: invalid node reference at line 1247")

        print("✓ Grid data loaded successfully")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
