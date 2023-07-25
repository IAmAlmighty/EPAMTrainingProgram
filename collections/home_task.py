from random import randint, sample
import string

# 1. create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

rand_num_of_dicts = []
"""Creating an empty list."""
for _ in range(randint(2, 10)):
    """For range between 2 and 10."""
    sample_size = randint(1, len(string.ascii_letters))
    """Randomizing size for each dict."""
    keys = sample(string.ascii_letters, sample_size)
    """Creating sample of random keys."""
    values = (randint(0, 100) for _ in range(sample_size))
    """Creating sample of random values."""
    rand_num_of_dicts.append(dict(zip(keys, values)))
    """Merge keys and values as dict and appending to a list."""

"""There is no explicit info about how many items every dict should contain.
Normally I'll go and clarify it with task creator and ask to update task description.
Here I assume that there should be from 1 to max number of letters."""

# 2. get previously generated list of dicts and create one common dict:
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
"""
Task is ambiguous: given I should rename key with just dict number which has max value.
But in example seems like I should use pattern: <<<key + '_' + dict number which has max value>>>.
Normally I'll go and clarify and ask to update task with clear description.
Here I assume that example is correct way to do it.
"""
common_dict = {}
"""Will contain end result."""
keys_and_indexes = {}
"""Will contain track of which keys already added and dict number with max value."""
for i, d in enumerate(rand_num_of_dicts):
    """Enumerating dict for parsing purposes."""
    for key, value in d.items():
        """Looking at keys, values in enumerated dict."""
        if key in keys_and_indexes:
            """If we already have such key."""
            keys_and_indexes[key].update({i: value})
            """Update it with new value."""
        else:
            """Or else."""
            keys_and_indexes[key] = {i: value}
            """Add new key with value."""
"""
Note that I'm using another pattern for number of dict, starting from 0, instead of 1 like in example.
This is because of convention of indexing things in python.
"""
for key, value in keys_and_indexes.items():
    """Iterate through intermediate dict items."""
    if len(value.values()) == 1:
        """If there only 1 value for current key."""
        common_dict[key] = list(value.values())[0]
        """We name that just at it is, without any additional suffixes to final dict."""
        continue
        """Jump to next iteration immediately, we not needed other operations in such case."""

    max_i, max_v = 0, 0
    """Default index and value initialization."""
    for k, v in value.items():
        """Iterate through values."""
        if v > max_v:
            """If there are value that > than default 0."""
            max_v = v
            """Mark that value as current maximum."""
            max_i = k
            """Mark that index as holder of current maximum value."""

    common_dict[f"{key}_{max_i}"] = max_v
    """Adding found maximum value to final dict with correct index where we found that value."""

print(f"{rand_num_of_dicts=}")
print(f"{keys_and_indexes=}")
print(f"{common_dict=}")
for k, v in common_dict.items():
    if "_" in k:
        print(f"Renamed key: {k}")
    else:
        print(f"Not renamed key: {k}")
