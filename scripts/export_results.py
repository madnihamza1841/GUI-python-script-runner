#!/usr/bin/env python3
import time
import random
import sys

def main():
    try:
        print("Exporting simulation results...")
        time.sleep(0.6)

        print("Writing HDF5 output file (1.2 GB)")
        time.sleep(0.8)

        print("Generating summary statistics and metadata")
        time.sleep(0.4)

        if random.random() < 0.15:
            raise Exception("Disk write failed: no space available in /tmp")

        print("✓ Results exported successfully")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
