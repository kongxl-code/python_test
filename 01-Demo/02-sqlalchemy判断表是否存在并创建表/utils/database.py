from sqlalchemy import create_engine, insert, update
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
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(data.get("user"), data.get("password"), data.get("host"), data.get("port"), data.get("db")), echo=True)
    def check_and_create_table(self, table):
        table.create(self.engine, checkfirst=True)

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