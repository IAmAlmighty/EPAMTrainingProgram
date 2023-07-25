from random import randint, sample
import string
import re

"""
Ideally it is good to separate functions by different modules via their logical functionality.
"""


def gen_rand_num_of_dicts_w_items():
    """
    Returns list of dicts. Each dict may have random count of keys from 1 to maximum chars in English alphabet x2.
    Meaning that upper and lower cases are different possible keys.
    Every value in those dicts will have random int value from 0 to 100 including both.

    Example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
    """

    result = []
    for _ in range(randint(2, 10)):
        sample_size = randint(1, len(string.ascii_letters))
        keys = sample(string.ascii_letters, sample_size)
        values = (randint(0, 100) for _ in range(sample_size))
        result.append(dict(zip(keys, values)))

    return result


def merge_dicts_keys_and_vals(list_of_dicts):
    """
    Merges dicts within a list into one final dict.
    If dicts have same key, it will take max value, and rename key with dict number with max value.
    If key is only in one dict - it will save as is.

    Input example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
    Output example: {'a_0': 5, 'b': 7, 'c': 35, 'g_1': 42}
    """

    result = {}
    keys_and_indexes = {}
    for i, d in enumerate(list_of_dicts):
        for key, value in d.items():
            if key in keys_and_indexes:
                keys_and_indexes[key].update({i: value})
            else:
                keys_and_indexes[key] = {i: value}

    for key, value in keys_and_indexes.items():
        if len(value.values()) == 1:
            result[key] = list(value.values())[0]
            continue

        max_i, max_v = 0, 0
        for k, v in value.items():
            if v > max_v:
                max_v = v
                max_i = k

        result[f"{key}_{max_i}"] = max_v

    return result


dicts = gen_rand_num_of_dicts_w_items()
merged_dicts = merge_dicts_keys_and_vals(dicts)

print(f"{merged_dicts=}")

initial_text = """tHis iz your homeWork, copy these Text to variable.




  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.




  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.




  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


def separate_text_by_sentences(text):
    """
    Returns list of separate sentences of a given text.
    Sentences separated by <.>.
    """
    split_text = text.split(".")
    split_text = split_text if len(split_text[-1]) > 0 else split_text[:-1]
    return [t.strip() for t in split_text]


def normalize_letters_cases(text):
    """
    Returns text with every first word in sentences capitalized. Everything else is lowercase.
    """
    result = ""
    sentences = separate_text_by_sentences(text)

    for s in sentences:
        result += f"{s.capitalize()}. "
    return result.rstrip()


def get_last_words(sentences):
    """
    Takes every last word from list of sentences. Numbers counts as a words.
    Returns it as string where words separated by space.
    """
    result = ""
    for s in sentences:
        result += f"{s.split(' ')[-1]} "
    return result.rstrip(" ")
    """Ideally, I'd like to know how to split each word in sentences better than it is in this version.
    Because there are such cases when people forgot to add space after ',' etc.
    I think that perfect way must use regular expressions to handle corner cases."""


solution = normalize_letters_cases(initial_text)
solution = re.sub(r"\siz\s", " is ", solution)
"""This operation is not repeatable enough to capture it in separate function in my opinion.
Also it is 1-line operation."""

last_words = get_last_words(separate_text_by_sentences(initial_text))
updated_init_text = f"{initial_text} {last_words}."

cnt_whitespaces_str = initial_text.count(" ")
cnt_whitespaces_re = len(re.findall(r"[\s\n]", initial_text))
"""This operation is not repeatable enough to capture it in separate function in my opinion.
Also it is 1-line operation."""

print(f"{solution=}")
print(f"{updated_init_text=}")
