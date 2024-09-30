import random
import re

chain_len = 3
endsen = {".", "!", "?"}

garbage = ",.!?;:"


def split_to_trigrams(words_list):
    if len(words_list) <= chain_len:
        return []

    words = []

    for word in words_list:
        words.append(word)

    return [words[i : i + chain_len + 1] for i in range(len(words) - chain_len)]


def extract_words(message):
    symbols = list(re.sub(r"\s", " ", message))
    return list(filter(None, map(prettify, "".join(symbols).split(" "))))


def prettify(word):
    lowercase_word = word.lower().strip()
    last_symbol = lowercase_word[-1:]
    if last_symbol not in endsen:
        last_symbol = ""

    pretty_word = lowercase_word.strip(garbage)

    if pretty_word != "" and len(pretty_word) > 2:
        return pretty_word + last_symbol
    elif lowercase_word in garbage:
        return None

    return lowercase_word


def random_element(xlist):
    return random.choice(xlist) if len(xlist) > 0 else None


def random_end_sentence_token():
    return random_element(list(endsen))
