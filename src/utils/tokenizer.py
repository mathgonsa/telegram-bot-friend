import random
import re

# Constants
CHAIN_LEN = 3
ENDSEN = {".", "!", "?"}
GARBAGE = ",.!?;:"


def split_to_trigrams(words_list):
    if len(words_list) <= CHAIN_LEN:
        return []

    return [words_list[i : i + CHAIN_LEN + 1] for i in range(len(words_list) - CHAIN_LEN)]


def extract_words(message):
    symbols = re.sub(r"\s", " ", message)
    return list(filter(None, map(prettify, symbols.split(" "))))


def prettify(word):
    lowercase_word = word.lower().strip()
    last_symbol = lowercase_word[-1:] if lowercase_word[-1:] in ENDSEN else ""

    pretty_word = lowercase_word.strip(GARBAGE)

    if len(pretty_word) > 2:
        return pretty_word + last_symbol

    return None if lowercase_word in GARBAGE else lowercase_word


def random_element(xlist):
    return random.choice(xlist) if xlist else None


def random_end_sentence_token():
    return random_element(list(ENDSEN))
