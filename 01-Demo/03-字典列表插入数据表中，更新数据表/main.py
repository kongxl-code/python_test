import random
import json
from entity.data import generate_unique_dict_list
from tables.dependencies_table import defint_dependencies_table
from database.database import database as db
def main():
    data_list = generate_unique_dict_list(random.randint(1, 10))
    table = defint_dependencies_table("dependencies")
    db.insert_dependencies(table, data_list)
if __name__ == '__main__':
    main()