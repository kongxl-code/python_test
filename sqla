# 使用SQLAlchemy动态查询多个结构相同的表（完整代码示例）

下面是一个完整的Python脚本，展示如何使用SQLAlchemy的`table.c`语法动态查询多个结构相同的表，包括条件查询、排序和分页功能。

## 完整代码

```python
from sqlalchemy import create_engine, MetaData, Table, select, func, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional

class DynamicTableQuery:
    def __init__(self, database_url: str):
        """
        初始化查询器
        :param database_url: 数据库连接URL，如：
            'postgresql://user:password@localhost:5432/mydb'
            'mysql+pymysql://user:password@localhost/mydb'
            'sqlite:///database.db'
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def query_tables(
        self,
        table_names: List[str],
        columns: Optional[List[str]] = None,
        filters: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        distinct: bool = False
    ) -> List[Dict]:
        """
        查询多个结构相同的表
        
        :param table_names: 要查询的表名列表
        :param columns: 要查询的列名列表，None表示所有列
        :param filters: WHERE条件表达式字符串，如 "price > 100 AND category = 'electronics'"
        :param order_by: 排序表达式，如 "created_at DESC"
        :param limit: 返回结果数量限制
        :param distinct: 是否使用UNION去重(True)或UNION ALL不去重(False)
        :return: 字典列表形式的结果
        """
        metadata = MetaData()
        session = self.Session()
        
        try:
            # 动态加载所有表
            tables = []
            for name in table_names:
                try:
                    table = Table(name, metadata, autoload_with=self.engine)
                    tables.append(table)
                except Exception as e:
                    print(f"警告: 表 {name} 加载失败 - {str(e)}")
                    continue
            
            if not tables:
                return []
            
            # 确定要查询的列
            if columns:
                selected_columns = []
                for col in columns:
                    if hasattr(tables[0].c, col):
                        selected_columns.append(getattr(tables[0].c, col))
                    else:
                        print(f"警告: 列 {col} 不存在，已跳过")
                if not selected_columns:
                    selected_columns = [tables[0]]  # 默认选择所有列
            else:
                selected_columns = [tables[0]]  # 选择所有列
            
            # 构建每个表的查询
            queries = []
            for table in tables:
                query = select(*selected_columns).select_from(table)
                
                if filters:
                    query = query.where(text(filters))
                
                queries.append(query)
            
            # 合并查询
            if distinct:
                combined_query = queries[0].union(*queries[1:])
            else:
                combined_query = queries[0].union_all(*queries[1:])
            
            # 添加排序和限制
            if order_by:
                combined_query = combined_query.order_by(text(order_by))
            
            if limit:
                combined_query = combined_query.limit(limit)
            
            # 执行查询
            result = session.execute(combined_query)
            return [dict(row._mapping) for row in result]
        
        finally:
            session.close()
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """获取指定表的所有列名"""
        metadata = MetaData()
        try:
            table = Table(table_name, metadata, autoload_with=self.engine)
            return [c.name for c in table.columns]
        except Exception as e:
            print(f"获取表 {table_name} 列名失败: {str(e)}")
            return []

# 使用示例
if __name__ == "__main__":
    # 1. 初始化查询器 (使用SQLite内存数据库作为示例)
    db_url = "sqlite:///:memory:"
    query = DynamicTableQuery(db_url)
    
    # 2. 创建示例表结构 (实际使用时不需要这部分)
    with query.engine.connect() as conn:
        # 创建两个结构相同的示例表
        conn.execute(text("""
            CREATE TABLE sales_202301 (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                sale_date DATE
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE sales_202302 (
                id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                sale_date DATE
            )
        """))
        
        # 插入示例数据
        conn.execute(text("""
            INSERT INTO sales_202301 VALUES
            (1, 'Laptop', 'Electronics', 999.99, 5, '2023-01-15'),
            (2, 'Smartphone', 'Electronics', 699.99, 10, '2023-01-20'),
            (3, 'Desk Chair', 'Furniture', 149.99, 8, '2023-01-10')
        """))
        
        conn.execute(text("""
            INSERT INTO sales_202302 VALUES
            (4, 'Monitor', 'Electronics', 249.99, 12, '2023-02-05'),
            (5, 'Keyboard', 'Electronics', 49.99, 25, '2023-02-10'),
            (6, 'Coffee Table', 'Furniture', 199.99, 3, '2023-02-15')
        """))
        conn.commit()
    
    # 3. 示例查询
    
    # 示例1: 查询所有列的所有数据
    print("\n示例1: 查询所有数据")
    results = query.query_tables(
        table_names=["sales_202301", "sales_202302"]
    )
    for row in results:
        print(row)
    
    # 示例2: 查询特定列
    print("\n示例2: 只查询产品名称和价格")
    results = query.query_tables(
        table_names=["sales_202301", "sales_202302"],
        columns=["product_name", "price"]
    )
    for row in results:
        print(row)
    
    # 示例3: 带条件查询
    print("\n示例3: 查询电子类产品且价格>100")
    results = query.query_tables(
        table_names=["sales_202301", "sales_202302"],
        columns=["id", "product_name", "price", "category"],
        filters="category = 'Electronics' AND price > 100"
    )
    for row in results:
        print(row)
    
    # 示例4: 排序和限制
    print("\n示例4: 按价格降序排序，只返回3条")
    results = query.query_tables(
        table_names=["sales_202301", "sales_202302"],
        columns=["product_name", "price"],
        order_by="price DESC",
        limit=3
    )
    for row in results:
        print(row)
    
    # 示例5: 获取表结构
    print("\n示例5: 获取表结构")
    columns = query.get_table_columns("sales_202301")
    print("sales_202301表的列:", columns)
```

## 主要功能说明

1. **动态表查询**：
   - 可以传入任意数量的表名列表
   - 自动加载表结构
   - 处理表加载失败的情况

2. **灵活的列选择**：
   - 可以指定要查询的列
   - 自动验证列是否存在
   - 不指定列时查询所有列

3. **条件查询**：
   - 支持完整的SQL WHERE条件表达式
   - 示例：`"price > 100 AND category = 'electronics'"`

4. **结果控制**：
   - 支持排序（ORDER BY）
   - 支持结果数量限制（LIMIT）
   - 可以选择使用UNION去重或UNION ALL不去重

5. **辅助功能**：
   - 获取表的列名列表
   - 自动管理数据库会话

## 实际应用场景

1. **分表数据合并查询**：
   ```python
   # 查询2023年所有月份的数据
   months = [f"sales_2023{str(m).zfill(2)}" for m in range(1, 13)]
   yearly_data = query.query_tables(table_names=months)
   ```

2. **多租户数据查询**：
   ```python
   # 查询多个租户的相同结构表
   tenants = ["tenant1_orders", "tenant2_orders", "tenant3_orders"]
   all_orders = query.query_tables(
       table_names=tenants,
       filters="status = 'completed' AND amount > 1000",
       order_by="created_at DESC"
   )
   ```

3. **日志分析**：
   ```python
   # 分析多个月份的日志数据
   log_tables = [f"app_logs_{month}" for month in ["jan", "feb", "mar"]]
   error_logs = query.query_tables(
       table_names=log_tables,
       filters="level = 'ERROR'",
       columns=["timestamp", "message", "user_id"]
   )
   ```

这个实现提供了高度灵活性，可以适应各种需要合并查询多个结构相同表的场景。
