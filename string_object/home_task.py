import re

initial_text = """tHis iz your homeWork, copy these Text to variable.




  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.




  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.




  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

split_text = initial_text.split(".")[:-1]
space_stripped_text = [t.strip() for t in split_text]
"""Split text by sentences and strip all whitespaces."""
solution = ""
for sentence in space_stripped_text:
    solution += f"{sentence.capitalize()}. "
solution = solution.rstrip()
"""Capitalizing each sentence."""
solution = re.sub(r"\siz\s", " is ", solution)
"""Correcting misspelling except one which is example via regular expression."""

cnt_whitespaces_str = initial_text.count(" ")
cnt_whitespaces_re = len(re.findall(r"[\s\n]", initial_text))
"""Not sure what mean 'not only spaces, but all whitespaces'...
Usually I'll go and clarify it with task creator."""

last_words = ""
for s in space_stripped_text:
    last_words += f"{s.split(' ')[-1]} "
    """Taking last word in each sentence."""
last_words = last_words.rstrip(" ")
updated_init_text = f"{initial_text} {last_words}."
"""Adding new sentence of last words to the end of initial sentence.
Assuming that '87' should be added instead of actual word before it.
This is also a moment to clarify with task giver normally."""

print(f"{solution=}")
print(f"{cnt_whitespaces_str=}")
print(f"{cnt_whitespaces_re=}")
print(f"{updated_init_text=}")
