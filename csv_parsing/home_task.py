import csv
import os
import re

feed_file_path = "../classes_oop/newsfeed.txt"


class Parser:
    """Implements parsing text with different end-goals."""

    def count_words(self, text):
        """Counts every single word in given text. Cast lowercase on a text.
        Returns dict with 'word': count."""
        pattern = r"[a-zA-Z]+"
        result = {}

        for w in re.findall(pattern, text.lower()):
            if w in result:
                result[w] += 1
            else:
                result[w] = 1

        return result

    def count_chars(self, text):
        """Counts every single character in given text.
        Differentiates between lower and upper cases, provides difference on total/upper and percentage against overall count of chars in text.
        Returns dict with 'char is lowercase': {'total': count, 'upper': count, 'percentage': total/sum of totals}."""
        pattern = r"[A-Za-z]"
        result = {}
        chars_total = 0

        for c in re.findall(pattern, text):
            chars_total += 1
            c_lower = c.lower()
            if c_lower not in result:
                result[c_lower] = {"total": 1, "upper": int(c.isupper())}
            else:
                result[c_lower]["total"] += 1
                result[c_lower]["upper"] += int(c.isupper())

        self.calc_chars_percentage(result)

        return result

    def count_words_bulk(self, text_data):
        """Counts words in given data in bulk mode."""
        result = {}

        for td in text_data:
            words_cnt = self.count_words(td)
            for k, v in words_cnt.items():
                if k in result:
                    result[k] += v
                else:
                    result[k] = v

        return result

    def count_chars_bulk(self, text_data):
        """Counts chars in given data in bulk mode."""
        result = {}

        for td in text_data:
            chars_cnt = self.count_chars(td)
            for k, v in chars_cnt.items():
                if k in result:
                    result[k]["total"] += v["total"]
                    result[k]["upper"] += v["upper"]
                else:
                    result[k] = v

        # chars_total = 0
        # for v in result.values():
        #     chars_total += v["total"]
        # for v in result.values():
        #     v["percentage"] = round(v["total"] / chars_total * 100, 2)
        self.calc_chars_percentage(result)

        return result

    def calc_chars_percentage(self, chars_dict):
        """Calculate chars percentage in given dict, adding that info to dict itself."""
        chars_total = 0
        for value in chars_dict.values():
            chars_total += value["total"]
        for value in chars_dict.values():
            value["percentage"] = round(value["total"] / chars_total * 100, 2)


class CSVExporter:
    """Implements export data to CSV file."""
    words_file = "words_count.csv"
    chars_file = "chars_count.csv"
    words_headers = ["Word", "Count"]
    chars_headers = ["Char", "Total", "Upper", "Percentage"]

    def export_words(self, words_dict, update_existing=True):
        """Exports given dict with words. Can update values in existing file."""
        if update_existing and os.path.isfile(self.words_file):
            existing_wd = self.get_words_dict()
            for key, value in existing_wd.items():
                if key not in words_dict:
                    words_dict.update({key: value})
                else:
                    words_dict[key] += int(value)

        formatted = [{"Word": k, "Count": v} for k, v in words_dict.items()]

        with open(self.words_file, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.words_headers)
            writer.writeheader()
            writer.writerows(formatted)

    def export_chars(self, chars_dict, update_existing=True):
        """Exports given dict with chars. Can update values in existing file."""
        if update_existing and os.path.isfile(self.chars_file):
            existing_cd = self.get_chars_dict()
            for key, value in existing_cd.items():
                if key not in chars_dict:
                    chars_dict.update({key: value})
                else:
                    chars_dict[key]["total"] += int(value["total"])
                    chars_dict[key]["upper"] += int(value["upper"])
        Parser().calc_chars_percentage(chars_dict)
        formatted = [{"Char": k, "Total": v["total"], "Upper": v["upper"], "Percentage": v["percentage"]}
                     for k, v in chars_dict.items()]

        with open(self.chars_file, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.chars_headers)
            writer.writeheader()
            writer.writerows(formatted)

    def get_words_dict(self):
        """Returns dict with words from existing CSV file."""
        result = {}
        with open(self.words_file, "r", newline='') as file:
            reader = csv.DictReader(file, fieldnames=self.words_headers)
            next(reader, None)  # skip headers
            for item in reader:
                result[item["Word"]] = int(item["Count"])

        return result

    def get_chars_dict(self):
        """Returns dict with chars from existing CSV file."""
        result = {}
        with open(self.chars_file, "r", newline='') as file:
            reader = csv.DictReader(file, fieldnames=self.chars_headers)
            next(reader, None)  # skip headers
            for item in reader:
                result[item["Char"]] = {"total": int(item["Total"]), "upper": int(item["Upper"])}

        return result


if __name__ == "__main__":
    with open(feed_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    words_cnt = Parser.count_words(file_content)
    print(f"{words_cnt=}")
    chars_cnt = Parser.count_chars(file_content)
    print(f"{chars_cnt=}")

    exp = CSVExporter()
    exp.export_words(words_cnt)
    exp.export_chars(chars_cnt)
