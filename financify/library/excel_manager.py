"""Pylightxl wrapper for spreadsheet reading/writing"""

import os
from datetime import datetime
from operator import attrgetter
from typing import Any, Dict, List

import pylightxl

from financify.library.exceptions import NoPropException

Row = List[Any]
Sheet = List[Row]


class AssetEvent:
    """Property indexible event for Assets"""

    def __init__(self, **kwargs: str) -> None:
        """Parse key word args"""
        self.__dict__.update(
            (key, kwargs[key])
            for key in ("date", "id", "type", "value")
            if key in kwargs
        )

    def timestamp(self, date_pattern: str = "%Y/%M/%d") -> datetime:
        """Return date as a datetime

        :param date_pattern: optional regex pattern
        """
        if hasattr(self, "date"):
            return datetime.strptime(self.date, date_pattern)
        raise NoPropException("Asset Event does not have a date property")

    def update(self, **kwargs: str) -> None:
        """Update props with extra data"""
        self.__dict__.update(kwargs)


class ExcelReader:
    """Read excel file and process data"""

    def __init__(self, read_loc: str, cfg: Dict[str, Any]) -> None:
        """Get database and sheet objects

        :param read_loc: path to excel file
        :param cfg: input file config information
        """
        self.cfg = cfg
        self.database = pylightxl.readxl(os.path.join(read_loc, self.cfg["file_name"]))
        self.sheet = self.database.ws(self.cfg["sheets"][0])
        self.rows: List[AssetEvent] = []
        self.headers = [header.strip() for header in self.sheet.row(1)]
        self.row_props = list(self.cfg["columns"].keys())
        flagged_cols: Dict[str, int] = {}
        for col, header in self.cfg["columns"].items():
            flagged_cols[col] = self.headers.index(header) + 1
        for row in list(self.sheet.rows)[1:]:
            asset_evt = dict(
                map(
                    lambda key, val: (key, val),
                    flagged_cols.keys(),
                    [row[idx - 1] for idx in flagged_cols.values()],
                )
            )
            self.rows.append(AssetEvent(**asset_evt))

    def sort_by(self, props: List[str]) -> None:
        """Sort rows list by props in place

        :param props: List of properties to sort rows by
        """
        self.rows.sort(key=attrgetter(*props))

    def flag_losses(self) -> None:
        """Update loss sale rows"""
