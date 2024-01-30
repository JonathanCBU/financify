import argparse
import os
from sys import platform as sys_platform

import pylightxl


def get_args() -> argparse.Namespace:
    """Collect command line args"""

    parser = argparse.ArgumentParser(
        description="Command line arguments for wash sale detector"
    )

    parser.add_argument("--folder", type=str, default="")
