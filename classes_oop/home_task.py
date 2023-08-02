from random import choice, randint
from datetime import datetime
import json

newsfeed_file = "newsfeed.txt"
geese_facts_file = "facts_about_geese.json"

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


def get_file_data_json(file_path):
    """Returns data from file path in JSON format."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


class FeedGenerator:
    """Base class for feed record generation."""
    prefix = "Feed"
    suffix = "*************"

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
        return "-==-"


class News(FeedGenerator):
    """Implements adding news to newsfeed.
    Includes: news, city, date of publishing."""
    prefix = "News"

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


class FeedFactory:
    """Factory class for deciding what type of content user want to add to the feed."""
    classes = {News.__name__: News(), Ad.__name__: Ad(), GeeseFacts.__name__: GeeseFacts(), }
    cls_enum = {i: c for i, c in enumerate(classes.keys())}

    input_txt = f"Please, choose what content type do you want to add by entering given number of feed type:\n" + \
                str(cls_enum) + "\n"

    def run(self):
        """Decides what type of content user want to generate."""
        index = int(input(self.input_txt))
        while index not in range(len(self.cls_enum)):
            index = int(input(self.input_txt))

        cls_name = self.cls_enum[index]
        self.classes[cls_name].generate()


if __name__ == "__main__":
    """Generate feed entries by input."""
    ff = FeedFactory()
    ff.run()
