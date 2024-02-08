"""Wash Sale Detection CLI"""

import argparse
import os
from sys import platform

import pylightxl
import yaml

from financify.library.exceptions import InvalidOSException


def main() -> None:
    """Wash Sale Detector entry point"""

    # get operating system
    home = ""
    if platform == "win32":
        # Windows
        home = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"])
    elif platform in ["linux", "darwin"]:
        # Linux or iOS
        home = os.environ["HOME"]
    else:
        raise InvalidOSException(
            f"Operating system not supported. OS detected: {platform}"
        )

    args = get_args()
    cfg_path = (
        args.config
        if args.config != ""
        else os.path.join(
            home, "repos/financify/financify/configs/wash_sale_detector.yml"
        )
    )
    with open(cfg_path, "r", encoding="utf-8") as cfg_file:
        cfg = yaml.safe_load(cfg_file)

    input_folder = (
        args.folder
        if args.folder != ""
        else os.path.join(home, "repos/financify/financify/dummy_data/")
    )
    input_file = args.file if args.file != "" else "wash_sale_example.xlsx"
    input_data = pylightxl.readxl(os.path.join(input_folder, input_file)).ws(
        cfg["input"]["sheet_name"]
    )
    for row in input_data.rows:
        print(row)


def get_args() -> argparse.Namespace:
    """Collect command line args"""

    parser = argparse.ArgumentParser(
        description="Command line arguments for wash sale detector"
    )

    parser.add_argument(
        "--folder",
        default="",
        help="Full path folder name containing spreadsheet",
    )
    parser.add_argument("--file", default="", help="Spreadsheet name")
    parser.add_argument(
        "--config", default="", help="Full path to configuration yaml file"
    )

    args = parser.parse_args()
    return args
