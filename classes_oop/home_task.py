from csv_parsing.home_task import CSVExporter, Parser
from string_object.home_task import normalize_text
from random import choice, randint
from datetime import datetime
import json
import os

newsfeed_file = "newsfeed.txt"
geese_facts_file = "facts_about_geese.json"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
default_news_import_file = os.path.join(PROJECT_ROOT, "news_to_feed.json")

default_date_format = "%Y-%m-%d"


def current_date():
    """Returns current date with default format."""
    return datetime.date(datetime.today())


def reset_newsfeed():
    """Resetting newsfeed file to initial state, erasing all items from it."""
    with open(newsfeed_file, "w", encoding="utf-8") as file:
        file.write("News feed:\n")


def add_text_to_feed_file(text):
    """Adds text to newsfeed file."""
    with open(newsfeed_file, "a", encoding="utf-8") as file:
        file.write(text)


def get_geese_facts():
    """Returns list of strings of facts about geese."""
    with open("facts_about_geese.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_file_data_json(file_path):
    """Returns data from file path in JSON format."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_file_data(file_path):
    """Returns data from file path."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


class FeedGenerator:
    """Base class for feed record generation."""
    prefix = "Feed"
    suffix = "*************"
    fields = {"type", "text"}

    @staticmethod
    def export_feed_words_chars_count():
        """Retrieves newsfeed data: words count, chars count. Exports such data to CSV file."""
        feed_text = get_file_data(newsfeed_file)
        words_dict = Parser.count_words(feed_text)
        chars_dict = Parser.count_chars(feed_text)
        exp = CSVExporter()
        exp.export_words(words_dict)
        exp.export_chars(chars_dict)

    def generate(self):
        """Implements process of generating feed input and putting it to newsfeed."""
        data = self.input_data()
        text = self.form_feed_record(data)

        add_text_to_feed_file(text)

    def input_data(self):
        """Decides how many and what inputs user should input to create feed instance."""
        raise TypeError(f"Wrong class for feed update: {self}")

    def form_feed_record(self, data):
        """Returns proper format for Feed record."""
        return (f"\n{self.prefix} {self.suffix}\n"
                f"{self.inner_text(data)}"
                f"\n{self.suffix}\n")

    def inner_text(self, data):
        for f in self.fields:
            if f not in data:
                raise ValueError(f"Wrong data passed: {data},\nkeys should contain: {self.fields}")
        return "-==-"


class News(FeedGenerator):
    """Implements adding news to newsfeed.
    Includes: news, city, date of publishing."""
    prefix = "News"
    fields = {"type", "text", "city"}

    def input_data(self):
        data = {"text": input("Provide news text:\n"),
                "city": input("Provide name of city where it happened:\n"),
                "date": str(current_date())}
        return data

    def inner_text(self, data):
        return f"{data['text']}\n" \
               f"{data['city']}, {current_date()}"


class Ad(FeedGenerator):
    """Implements adding ads to newsfeed.
    Includes: Advertising text, date of ad expiration."""
    prefix = "Private Ad"
    exp_date_input_text = "Provide advertising expiration date in format <year-month-day> (eg: 2077-07-13):\n"
    fields = {"type", "text", "exp_date"}

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

    def inner_text(self, data):
        super().inner_text(data)
        exp_days_left = (datetime.date(datetime.strptime(data["exp_date"], default_date_format)) -
                         datetime.date(datetime.today())).days

        return f"{data['text']}\n" \
               f"Actual until: {data['exp_date']}, {exp_days_left} days left"


class GeeseFacts(FeedGenerator):
    """Implements adding random facts about geese to newsfeed."""
    prefix = "Facts about geese."

    def input_data(self):
        data = {"text": choice(get_file_data_json(geese_facts_file)),
                "certainty": randint(101, 115)}
        return data

    def inner_text(self, data):
        return f"{data['text']}\n" \
               f"Info certainty: {data['certainty']}%"


class FeedImport:
    """Implements adding entries in bulk to feed from file."""

    @staticmethod
    def input_import_file_path():
        """Returns file path from user input or default file path if input in empty."""
        file_path = input(f"Provide full path to file from which feed should be imported.\n"
                          f"Press <ENTER> to use default file: {default_news_import_file}\n")
        if not file_path:
            file_path = default_news_import_file
        return file_path

    def import_feed(self, classes, normalize=False):
        """
        Imports data from file to feed in bulk. Then deletes that file.
        """
        file_path = self.input_import_file_path()
        file_data = get_file_data_json(file_path)

        text = ""
        for data in file_data:
            obj_type = data["type"]
            if normalize:
                data["text"] = normalize_text(data["text"])

            text += classes[obj_type].form_feed_record(data)

        add_text_to_feed_file(text)
        print(f"Removing file: {file_path}")
        os.remove(file_path)


class FeedFactory:
    """Factory class for deciding what type of content user want to add to the feed."""
    classes = {News.__name__: News(), Ad.__name__: Ad(), GeeseFacts.__name__: GeeseFacts(), FeedImport.__name__: FeedImport()}
    cls_enum = {i: c for i, c in enumerate(classes.keys())}

    input_txt = f"Please, choose what content type do you want to add by entering given number of feed type:\n" + \
                str(cls_enum) + "\n"

    def run(self):
        """Decides whether user want to generate news feed from console by hand or import it from file."""
        index = int(input(self.input_txt))
        while index not in range(len(self.cls_enum)):
            index = int(input(self.input_txt))

        cls_name = self.cls_enum[index]
        if cls_name == FeedImport.__name__:
            self.classes[cls_name].import_feed(self.classes, normalize=True)
        else:
            self.classes[cls_name].generate()

        FeedGenerator.export_feed_words_chars_count()


if __name__ == "__main__":
    """Generate feed entries by input or import in bulk."""
    ff = FeedFactory()
    ff.run()
