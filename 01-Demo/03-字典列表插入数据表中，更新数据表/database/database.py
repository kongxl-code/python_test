from sqlalchemy import create_engine, insert, update, and_
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self):
        data = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "root",
            "db": "test"
        }
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(data.get("user"), data.get("password"), data.get("host"), data.get("port"), data.get("db")))
    def check_and_create_table(self, table):
        table.create(self.engine, checkfirst=True)

    def insert_dependencies(self, table, data_list):
        self.check_and_create_table(table)
        try:
            with sessionmaker(bind=self.engine)() as session:
                session.begin()
                table.engine = self.engine
                query_responses = session.query(table.c.module, table.c.dependency).distinct().all()
                dependency_in_sql_list = []
                for query_response in query_responses:
                    modules = query_response.module
                    dependencies = query_response.dependency
                    last_dependency = session.query(table).filter(and_(table.c.module == modules, table.c.dependency == dependencies)).order_by(table.c.update_on.desc()).first()
                    if last_dependency and last_dependency.status:
                        dependency_in_sql_list.append({
                            "module": modules,
                            "dependency": dependencies,
                            "status": True
                        })
                false_data_list = [{ 
                    "module": item.get("module"),
                    "dependency": item.get("dependency"),
                    "status": False
                 } for item in dependency_in_sql_list if item not in data_list]
                for fasle_data in false_data_list:
                    item = insert(table).values(fasle_data)
                    session.execute(item)

                for data in data_list:
                    filter_condition = and_(table.c.module == data.get("module"), table.c.dependency == data.get("dependency"))
                    query_response = session.query(table).filter(filter_condition).order_by(table.c.update_on.desc()).first()
                    if query_response is None:
                        item = insert(table).values(data)
                        session.execute(item)
                    elif query_response.status != data.get("status"):
                        item = insert(table).values(data)
                        session.execute(item)
                session.commit()
        except Exception as e:
            print(e)

    def update_or_insert(self, table, filter_condition, data):
        self.check_and_create_table(table)
        try:
            with sessionmaker(bind=self.engine)() as session:
                session.begin()
                table.engine = self.engine
                count = session.query(table).filter(filter_condition).count()
                if count == 0:
                    item = insert(table).values(data)
                    session.execute(item)
                else:
                    item = update(table).where(filter_condition).values(*data)
                    session.execute(item)
                session.commit()
        except Exception as e:
            print(e)
            

database = Database()