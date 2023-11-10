from csv_parsing.home_task import CSVExporter, Parser
from string_object.home_task import normalize_text
from random import choice, randint
from datetime import datetime
import sqlite3
import json
import os
import re

geese_facts_file = "facts_about_geese.json"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
default_news_import_file = os.path.join(PROJECT_ROOT, "news_to_feed.txt")

default_date_format = "%Y-%m-%d"


def get_file_data_json(file_path):
    """Returns data from file path in JSON format."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_file_data(file_path):
    """Returns data from file path."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


class DB:
    """Implements DB interactions."""
    db_name = "newsfeed.db"
    tables = {
        "News": {"columns": ["id", "text", "city", "added_at"],
                 "rules": ["INTEGER PRIMARY KEY AUTOINCREMENT", "TEXT NOT NULL", "varchar(64) NOT NULL",
                           "DATETIME DEFAULT current_timestamp"]},
        "Ads": {"columns": ["id", "text", "exp_date", "added_at"],
                "rules": ["INTEGER PRIMARY KEY AUTOINCREMENT", "TEXT NOT NULL", "DATETIME NOT NULL", "DATETIME DEFAULT current_timestamp"]},
        "GeeseFacts": {"columns": ["id", "text", "certainty", "added_at"],
                       "rules": ["INTEGER PRIMARY KEY AUTOINCREMENT", "TEXT NOT NULL", "INT", "DATETIME DEFAULT current_timestamp"]}
    }

    def __init__(self, isolation_level=None):
        with sqlite3.connect(self.db_name, isolation_level=isolation_level) as conn:
            self.cur = conn.cursor()

        for table_name in self.tables.keys():
            if not self.is_table_exists(table_name):
                raise Exception(f"Currently table {table_name} not exists.\n"
                                f"You should use create_table('{table_name}') method to initiate it.\n"
                                f"Or use create_tables() to create all missing tables.")

    def __del__(self):
        self.cur.close()

    def is_table_exists(self, table_name):
        """Returns boolean value if given table_name exists."""
        cmd = f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table_name}'"
        self.cur.execute(cmd)

        return bool(self.cur.fetchall())

    def create_tables(self):
        """Creates all tables with <self.tables> rules."""
        for table_name in self.tables.keys():
            self.create_table(table_name)

    def create_table(self, table_name):
        """Creates given table with <self.tables> rule."""
        columns_descr = ""
        for col, rule in zip(self.tables[table_name]["columns"], self.tables[table_name]["rules"]):
            columns_descr += f"{col} {rule}, "
        columns_descr = columns_descr.rstrip(", ")

        cmd = f"""CREATE TABLE IF NOT EXISTS {table_name} ({columns_descr})"""
        print(f"Creating table cmd: {cmd}")
        self.cur.execute(cmd)

    def recreate_tables(self):
        """Recreate all <self.tables> after dropping them."""
        for table_name in self.tables.keys():
            self.drop_table(table_name)
        self.create_tables()

    def drop_table(self, table_name):
        """Drops given table."""
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    def insert_many(self, data):
        """Insert many values into tables one by one."""
        for d in data:
            table_name = d.pop("type")
            self.insert(table_name, d)

    def insert(self, table_name, data):
        """Insert data into table."""
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        cmd = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        duplicate = self.is_duplicate(table_name, data)
        if not duplicate:
            self.cur.execute(cmd)
        else:
            raise ValueError(f"Given data already present in DB: {data}\nSQL cmd: {cmd}")

    def is_duplicate(self, table_name, data):
        """Returns boolean if data already present in table."""
        values = [f"{k} = '{v}'" for k, v in data.items()]
        values = " AND ".join(values)
        cmd = f"SELECT count(*) FROM {table_name} WHERE {values}"

        self.cur.execute(cmd)
        return bool(self.cur.fetchall()[0][0])

    def select_all_from(self, table_name):
        """Returns all columns from table."""
        cmd = f"SELECT * FROM {table_name}"
        self.cur.execute(cmd)
        return self.cur.fetchall()


class FeedGenerator:
    """Base class for feed record generation."""
    db = DB()

    @staticmethod
    def export_feed_words_chars_count(data):
        """Retrieves newsfeed data: words count, chars count. Exports such data to CSV file."""
        if not type(data) == list:
            data = [data]
        parser = Parser()
        text_data = [d["text"] for d in data]
        words_dict = parser.count_words_bulk(text_data)
        chars_dict = parser.count_chars_bulk(text_data)

        exp = CSVExporter()
        exp.export_words(words_dict)
        exp.export_chars(chars_dict)

    def generate(self, normalize=False):
        """Implements process of generating feed input and putting it to newsfeed."""
        data = self.input_data()
        data.update({"type": type(self).__name__})
        for _ in data:
            if normalize:
                data["text"] = normalize_text(data["text"])

        self.db.insert_many([data])
        self.export_feed_words_chars_count([data])

    def input_data(self):
        """Decides how many and what inputs user should input to add entry to feed DB."""
        raise TypeError(f"Input data process is not implemented in class: {type(self).__name__}")

    @staticmethod
    def parse(data):
        """Returns list with dicts of parsed items."""
        entries_separator_regex = r"\[(.*?)\]"
        entry_row_separator = ";\n"
        key_value_separator = r"(.*):\"(.*)\""
        rows, result = [], []

        for e in re.findall(entries_separator_regex, data, flags=re.DOTALL):
            rows.append([r for r in e.split(entry_row_separator) if r])

        for i, row in enumerate(rows):
            result.append({})
            for r in row:
                k, v = re.findall(key_value_separator, r, flags=re.DOTALL)[0]
                k = re.sub(r"\s", "", k)
                result[i].update({k: v})

        return result


class News(FeedGenerator):
    """Implements adding news to newsfeed.
    Includes: news, city."""

    def input_data(self):
        return {"text": input("Provide news text:\n"),
                "city": input("Provide name of the city where it happened:\n")}


class Ads(FeedGenerator):
    """Implements adding ads to newsfeed.
    Includes: Advertising text, date of ad expiration."""
    exp_date_input_text = "Provide advertising expiration date in format <year-month-day> (eg: 2077-07-13):\n"

    def input_data(self):
        data = {"text": input("Provide advertising text:\n"),
                "exp_date": input(self.exp_date_input_text)}
        self.validate_exp_date(data["exp_date"])

        return data

    @staticmethod
    def validate_exp_date(date):
        """Validate passed date: correctness and it must be in a future."""
        try:
            date = datetime.date(datetime.strptime(date, default_date_format))
        except ValueError:
            raise
        if date <= datetime.date(datetime.today()):
            raise ValueError(f"Date passed must be in future, got: {date}")


class GeeseFacts(FeedGenerator):
    """Implements adding random facts about geese to newsfeed."""

    def input_data(self):
        return {
            "text": choice(get_file_data_json(geese_facts_file)),
            "certainty": randint(101, 115)}


class FeedImport(FeedGenerator):
    """Implements adding entries in bulk to feed from file."""

    @staticmethod
    def input_import_file_path():
        """Returns file path from user input or default file path if input in empty."""
        file_path = input(f"Provide full path to file from which feed should be imported.\n"
                          f"Press <ENTER> to use default file: {default_news_import_file}\n")
        if not file_path:
            file_path = default_news_import_file
        return file_path

    def generate(self, normalize=False):
        """
        Imports data from file to feed DB in bulk. Then deletes imported file.
        """
        file_path = self.input_import_file_path()
        file_data = get_file_data(file_path)
        parsed_data = self.parse(file_data)

        for data in parsed_data:
            if normalize:
                data["text"] = normalize_text(data["text"])

        self.db.insert_many(parsed_data)
        self.export_feed_words_chars_count(parsed_data)
        print(f"Removing file: {file_path}")
        os.remove(file_path)


class FeedFactory:
    """Factory class for deciding what type of content user want to add to the feed."""
    classes = {News.__name__: News, Ads.__name__: Ads, GeeseFacts.__name__: GeeseFacts, FeedImport.__name__: FeedImport}
    cls_enum = {i: c for i, c in enumerate(classes.keys())}

    input_txt = f"Please, choose what content type do you want to add by entering given number of feed type:\n" + \
                str(cls_enum) + "\n"

    def run(self):
        """Decides whether user want to generate news feed from console by hand or import it from file."""
        index = int(input(self.input_txt))
        while index not in range(len(self.cls_enum)):
            index = int(input(self.input_txt))

        cls_name = self.cls_enum[index]
        obj = self.classes[cls_name]()
        obj.generate(normalize=True)


if __name__ == "__main__":
    """Generate feed entries by input or import in bulk."""
    db = DB()
    db.recreate_tables()

    ff = FeedFactory()
    ff.run()

    print(f"{db.select_all_from('News')}")
    print(f"{db.select_all_from('Ads')}")
    print(f"{db.select_all_from('GeeseFacts')}")
