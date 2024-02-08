"""Pylightxl wrapper for spreadsheet reading/writing"""

import os
from datetime import datetime
from operator import itemgetter
from typing import Any, Dict, List

import pylightxl

Row = List[Any]
Sheet = List[Row]


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
        self.columns: Sheet = list(self.sheet.cols)
        self.rows: Sheet = list(self.sheet.rows)

    @property
    def wash_sale_cols(self) -> Dict[str, int]:
        """Get relevant wash sale column numbers"""
        headers = [header.strip() for header in self.sheet.row(1)]
        return {
            "date": headers.index(self.cfg["columns"]["date"]) + 1,
            "transaction": headers.index(self.cfg["columns"]["transaction"]) + 1,
            "id": headers.index(self.cfg["columns"]["id"]) + 1,
            "price": headers.index(self.cfg["columns"]["price"]) + 1,
        }

    def prune_wash_sale_rows(self) -> Sheet:
        """Prune irrelevant columns from data"""
        relevant_cols = [
            self.wash_sale_cols["date"],
            self.wash_sale_cols["transaction"],
            self.wash_sale_cols["id"],
            self.wash_sale_cols["price"],
        ]
        pruned_rows = []
        for row in self.rows:
            pruned_rows.append([row[idx - 1] for idx in relevant_cols])
        return pruned_rows

    def sort_by_id(self, rows: Sheet, date_pattern: str = "%Y/%M/%d") -> Sheet:
        """Sort sheet by id and dates

        ..Note: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

        :param rows: a sheet object to be sorted
        :param date_pattern: datetime from string format following table in note
        """
        for row in rows[1:]:
            row[0] = datetime.strptime(row[0], date_pattern)
        return sorted(
            rows[1:],
            key=itemgetter(
                list(self.wash_sale_cols.keys()).index("id"),
                list(self.wash_sale_cols.keys()).index("date"),
            ),
        )
