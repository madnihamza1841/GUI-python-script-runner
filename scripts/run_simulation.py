#!/usr/bin/env python3
import time
import random
import sys

def main():
    try:
        print("Initializing HVDC simulator...")
        time.sleep(0.6)

        print("Running load flow analysis (5 iterations)")
        time.sleep(1.0)

        print("Converged at iteration 3 with mismatch < 1e-6")
        time.sleep(0.4)

        if random.random() < 0.15:
            raise Exception("Simulation diverged: jacobian matrix singular at step 847")

        print("✓ Simulation complete successfully")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
