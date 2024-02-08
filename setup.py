from financify.library.excel_manager import Sheet, ExcelReader
import os
import yaml

p = os.path.join(os.environ["HOME"], "repos/financify/financify/dummy_data")
with open(
    "/home/jcook_ub/repos/financify/financify/configs/wash_sale_detector.yml", "r"
) as f:
    cfg = yaml.safe_load(f)

ex = ExcelReader(p, cfg["input"])
cols = ex.prune_wash_sale_rows()
x = ex.sort_by_id(cols)
y = ex.get_id_sheets(x)
