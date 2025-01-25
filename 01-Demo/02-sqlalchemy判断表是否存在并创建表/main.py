from utils.database import database as db
from tables.pipeline_detail_table import defint_pipeline_detail_table
from tables.pipeline_info_table import defint_pipeline_info_table
from sqlalchemy import and_


def main():
    data = {"run_number": 1, "pipeline_run_id": "1", "start_time": 2, "end_time": 1},
    # print(*data)
    table = defint_pipeline_detail_table("pipeline_detail")
    filter_condition = and_(table.c.run_number == 1)
    db.update_or_insert(table, filter_condition, data)
    table = defint_pipeline_info_table("pipeline_info")
    filter_condition = and_(table.c.run_number == 1)
    db.update_or_insert(table, filter_condition, data)
    pass


if __name__ == "__main__":
    main()
