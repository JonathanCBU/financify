"""Bank statement parsing class"""

import re
from pypdf import PdfReader
from financify.library.statement import Statement

class BankStatement(Statement):
    """Bank statement parser"""

    def __init__(self, reader: PdfReader) -> None:
        super().__init__(reader)
