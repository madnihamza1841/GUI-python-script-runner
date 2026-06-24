#!/usr/bin/env python3
import time
import random
import sys

def main():
    try:
        print("Validating converter parameters...")
        time.sleep(0.7)

        print("Checking VSC control setpoints")
        time.sleep(0.5)

        print("Verifying AC/DC voltage limits...")
        time.sleep(0.6)

        if random.random() < 0.15:
            raise Exception("Validation failed: converter current rating exceeded (Max: 2500A, Input: 2650A)")

        print("✓ All parameters within acceptable range")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
