from financify.library.excel_manager import Sheet, ExcelReader
import os
import yaml

p = os.path.join(os.environ["HOME"], "repos/financify/financify/dummy_data")
with open(
    "/home/jcook_ub/repos/financify/financify/configs/wash_sale_detector.yml", "r"
) as f:
    cfg = yaml.safe_load(f)

ex = ExcelReader(p, cfg["input"])
