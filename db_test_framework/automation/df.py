from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from db_test_framework.automation.config import Config
from pyspark.sql import SparkSession


class DataFrameFactory:
    default_data_file = Config().df_items["file_path"]
    schema = StructType([
        StructField("ID", StringType(), True),
        StructField("Name", StringType(), True),
        StructField("Gender", StringType(), True),
        StructField("Age", IntegerType(), True),
        StructField("Height", IntegerType(), True),
        StructField("Weight", IntegerType(), True),
        StructField("Country", StringType(), True),
        StructField("CountryCode", StringType(), True),
        StructField("Year", StringType(), True),
        StructField("YearInt", IntegerType(), True),
        StructField("Season", StringType(), True),
        StructField("City", StringType(), True),
        StructField("Sport", StringType(), True),
        StructField("Event", StringType(), True),
        StructField("Medal", StringType(), True)
    ])

    def __init__(self):
        self.spark = SparkSession.builder.appName("DB's mock").getOrCreate()
        self.numeric_columns = ['Age', 'Height', 'Weight']

    def get_df(self):
        return self.spark.read.csv(self.default_data_file, header=True, schema=self.schema, quote='"', escape='"')


if __name__ == "__main__":
    pass
