"""Pylightxl wrapper for spreadsheet reading/writing"""

import os
from typing import Any, Dict, List

import pylightxl

Sheet = List[List[Any]]


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
        self.columns: List[str] = list(self.sheet.cols)
        self.rows: List[str] = list(self.sheet.rows)

    def prune_rows(self) -> Sheet:
        """Prune irrelevant columns from data"""
        headers = [header.strip() for header in self.sheet.row(1)]
        relevant_cols = [
            headers.index(self.cfg["columns"]["date"]) + 1,
            headers.index(self.cfg["columns"]["transaction"]) + 1,
            headers.index(self.cfg["columns"]["id"]) + 1,
            headers.index(self.cfg["columns"]["price"]) + 1,
        ]
        pruned_rows = []
        for row in self.rows:
            pruned_rows.append([row[idx - 1] for idx in relevant_cols])
        return pruned_rows

    def sort_by_date(self, rows: Sheet) -> Sheet:
        """Sort sheet by date"""
        raise NotImplementedError
