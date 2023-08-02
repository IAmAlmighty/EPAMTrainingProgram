import csv
import re

feed_file_path = "../classes_oop/newsfeed.txt"


class Parser:
    """Implements parsing text with different end-goals."""

    @staticmethod
    def count_words(text):
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

    @staticmethod
    def count_chars(text):
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

        for v in result.values():
            v["percentage"] = round(v["total"] / chars_total * 100, 2)

        return result


class CSVExporter:
    """Implements export data to CSV file."""
    words_file = "words_count.csv"
    chars_file = "chars_count.csv"
    words_headers = ["Word", "Count"]
    chars_headers = ["Char", "Total", "Upper", "Percentage"]

    def export_words(self, words_dict):
        formatted = [{"Word": k, "Count": v} for k, v in words_dict.items()]

        with open(self.words_file, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.words_headers)
            writer.writeheader()
            writer.writerows(formatted)

    def export_chars(self, chars_dict):
        formatted = [{"Char": k, "Total": v["total"], "Upper": v["upper"], "Percentage": v["percentage"]}
                     for k, v in chars_dict.items()]

        with open(self.chars_file, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.chars_headers)
            writer.writeheader()
            writer.writerows(formatted)


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
