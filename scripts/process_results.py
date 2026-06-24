#!/usr/bin/env python3
import time
import random
import sys

def main():
    try:
        print("Post-processing results...")
        time.sleep(0.5)

        print("Computing RMS voltages across all phases")
        time.sleep(0.7)

        print("Calculating harmonic distortion metrics")
        time.sleep(0.5)

        if random.random() < 0.15:
            raise Exception("Memory error: insufficient heap space for 2048 time steps")

        print("✓ Results processing complete")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
