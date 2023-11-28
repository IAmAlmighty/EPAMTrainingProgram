from db_test_framework.automation.config import Config
import pymssql

"""
DISCLAIMER:
Because of my local issues with MS SQL Server installation, DB will not be used in the scope of this homework.
Instead, I'll use Pyspark DFs and open csv file.
"""


class DB:
    name = "AdventureWorks2012"

    def __init__(self):
        self.cfg = Config()
        self.connection = self._connect_pymssql()
        self.cursor = self.connection.cursor()

    def _connect_pymssql(self):
        db_items_config = self.cfg.db_items
        return pymssql.connect(
            server=db_items_config["server"],
            user=db_items_config["user_name"],
            password=db_items_config["user_password"],
            database=self.name,
            port=int(db_items_config["port"])
        )

    @property
    def execute(self):
        return self.cursor.execute

    def fetchall(self):
        """Alias for cursor.fetchall with Row obj conversion into tuple."""
        return [tuple(r) for r in self.cursor.fetchall()]

    def get_table_schema_details(self, schema_name, table_name):
        cmd = f"""SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, COLUMN_DEFAULT, IS_NULLABLE, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}';"""
        self.execute(cmd)
        return self.fetchall()

    def get_aggregations_of_numeric(self, schema_name, table_name):
        cmd = f"""SELECT column_name
                  FROM information_schema.columns
                  WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'
                    AND data_type IN ('int', 'numeric', 'decimal', 'real', 'float');"""
        self.execute(cmd)
        numeric_columns = self.fetchall()
        if not numeric_columns:
            return []

        aggregations = "'{}', SUM({}), AVG({}), MAX({}), MIN({}), COUNT(DISTINCT {})"
        cmd = ""
        for column in numeric_columns:
            select = f"SELECT {aggregations.format(*[column[0] for _ in range(aggregations.count('{}'))])}"
            cmd += f"""{select} FROM {schema_name}.{table_name} UNION """
        cmd = cmd.rstrip("UNION ") + ";"

        self.execute(cmd)
        return self.fetchall()
