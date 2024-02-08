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

    @property
    def idx_map(self) -> int:
        """pruned sheet indexes map"""
        return {
            "id": list(self.wash_sale_cols.keys()).index("id"),
            "transaction": list(self.wash_sale_cols.keys()).index("transaction"),
            "date": list(self.wash_sale_cols.keys()).index("date"),
            "price": list(self.wash_sale_cols.keys()).index("price"),
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
                self.idx_map["id"],
                self.idx_map["date"],
            ),
        )

    def get_id_sheets(self, rows: Sheet) -> List[Sheet]:
        """Return a list of Sheet objects for each unique asset id

        :param rows: sheet sorted by ID (and ideally secondarily sorted by date)
        """
        sheets = []
        current_id = ""
        current_sheet = []
        for row in rows:
            if row[self.idx_map["id"]] != current_id:
                # new sheet
                if current_sheet != []:
                    sheets.append(current_sheet)
                current_id = row[self.idx_map["id"]]
                current_sheet = [row]
            else:
                current_sheet.append(row)
        return sheets
