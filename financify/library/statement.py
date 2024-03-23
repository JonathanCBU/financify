"""Parent class for financial statement readers"""

from typing import List
import re
from collections import deque
from pypdf import PdfReader, PageObject


class Statement:
    """Statement parser base"""

    def __init__(self, reader: PdfReader, id_num: int) -> None:
        self.reader = reader
        self.id = id_num

    @property
    def front_page(self) -> PageObject:
        """Get front page of statement object"""
        return self.reader.pages[0]

    def dollar_value_lines(self, page: PageObject) -> deque:
        """Find all lines on a page that contain dollar signs

        :param page: Page object from statement pdf
        """
        lines = deque([])
        for line in page.extract_text().split("\n"):
            if "$" in line:
                lines.append(line)
        return lines
