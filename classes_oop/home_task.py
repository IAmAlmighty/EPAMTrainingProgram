from datetime import datetime, timedelta
from random import choice, randint
import json

newsfeed_file = "newsfeed.txt"


def current_date():
    """Returns current date with default format."""
    return datetime.date(datetime.today())  # task asks just for date, not date and time


def reset_newsfeed():
    """Resetting newsfeed file to initial state, erasing all items from it."""
    with open(newsfeed_file, "w") as file:
        file.write("News feed:\n")


def get_geese_facts():
    """Returns list of strings of facts about geese."""
    with open("facts_about_geese.json", "r", encoding="utf-8") as file:
        return json.load(file)


class FeedGenerator:
    """Base class for feed record generation."""
    prefix = "Feed"
    suffix = "*************"
    input_txt = "Feed\n"

    def __init__(self):
        self.text = "Default feed text."

    def __str__(self):
        return self.__class__.__name__

    def generate(self):
        """Implements process of generating feed input and putting it to newsfeed."""
        self.decide_inputs()
        self.add_to_feed()
        print(f"Feed was updated with type: {self}.")

    def decide_inputs(self):
        """Decides how many and what inputs user should input to create feed instance."""
        raise TypeError(f"Wrong class for feed update: {self}")

    def add_to_feed(self):
        """Adds text to newsfeed file with a pattern."""
        with open(newsfeed_file, "a") as file:
            file.write(f"\n{self.prefix} {self.suffix}\n"
                       f"{self.text}"
                       f"\n{self.suffix}\n")


class News(FeedGenerator):
    """Implements adding news to newsfeed.
    Includes: news, city, date of publishing."""
    prefix = "News"

    def decide_inputs(self):
        news_txt = input("Provide news text:\n")
        city_name = input("Provide name of city where it happened:\n")
        news_date = current_date()
        self.text = f"{news_txt}\n" \
                    f"{city_name}, {news_date}"


class Ad(FeedGenerator):
    """Implements adding ads to newsfeed.
    Includes: Advertising, date of ad expiration."""
    prefix = "Private Ad"

    def decide_inputs(self):
        ad_txt = input("Provide advertising text:\n")
        ad_exp_timeout = int(input("Provide advertising expiration timeout in days:\n"))
        exp_date = current_date() + timedelta(days=ad_exp_timeout)
        self.text = f"{ad_txt}\n" \
                    f"Actual until: {exp_date}, {ad_exp_timeout} days left"


class GeeseFacts(FeedGenerator):
    """Implements adding random facts about geese to newsfeed."""
    prefix = "Facts about geese."

    def decide_inputs(self):
        random_geese_fact = choice(get_geese_facts())
        certainty = randint(101, 115)
        self.text = f"{random_geese_fact}\n" \
                    f"Info certainty: {certainty}%"


class FeedFactory:
    """Factory class for deciding what type of content user want to add to the feed."""
    feeds = [News, Ad, GeeseFacts]
    input_txt = f"Please, choose what content type do you want to add by entering given number of feed type:\n" + \
                str([f"{i}: {f.__name__}" for i, f in enumerate(feeds)]) + "\n"

    def __init__(self):
        self.feed = int(input(self.input_txt))
        while self.feed not in range(len(self.feeds)):
            self.feed = int(input(self.input_txt))

        self.feed = self.feeds[self.feed]()

    def generate(self):
        """Redirects newsfeed generation to chosen class."""
        self.feed.generate()


if __name__ == "__main__":
    ff = FeedFactory()
    ff.generate()
