import re

initial_text = """homEwork:

  tHis iz your homeWork, copy these Text to variable.




  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.




  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.




  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


def normalize_text(text):
    """Returns normalized text."""
    split_text = text.lower().split(".")[:-1]
    result = ""
    for sentence in split_text:
        first_letter_i = next(re.finditer(r"[A-Za-z]", sentence)).start()
        result += sentence[:first_letter_i] + sentence[first_letter_i:].capitalize() + "."

    return result
"""Separating text by split it by dot, then applying capitalization on each sentence starts with actual word, not space or newline."""

if __name__ == "__main__":
    normalized_text = normalize_text(initial_text)
    solution = re.sub(r"\siz\s", " is ", normalized_text)
    """Correcting misspelling except one which is example via regular expression."""

    cnt_whitespaces_str = initial_text.count(" ")
    cnt_whitespaces_re = len(re.findall(r"[\s]", initial_text))
    """Not sure what mean 'not only spaces, but all whitespaces'...
    Usually I'll go and clarify it with task creator."""

    last_words = " ".join(re.findall(r"[0-9A-Za-z]+(?=\.)", normalized_text))
    """Creating new sentence from last words after finding them via regex."""
    updated_init_text = f"{initial_text} {last_words.capitalize()}."
    """Adding new sentence of last words to the end of initial sentence.
    Assuming that '87' should be added instead of actual word before it.
    This is also a moment to clarify with task giver normally."""

    print(f"{solution=}")
    print(f"{cnt_whitespaces_str=}")
    print(f"{cnt_whitespaces_re=}")
    print(f"{updated_init_text=}")
