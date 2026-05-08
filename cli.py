import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--ignite", action="store_true")
parser.add_argument("--sync", action="store_true")

args = parser.parse_args()

if args.ignite:
    print("Ignition sequence active")
from engine.runtime import boot

if __name__ == "__main__":
    boot()
