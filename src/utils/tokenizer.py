import random
import re

from src.config import *


def split_to_trigrams(words_list):
    if len(words_list) <= CHAIN_LEN:
        yield from ()

    words = [STOP_WORD]

    for word in words_list:
        words.append(word)
        if word[-1] in ENDSEN:
            words.append(STOP_WORD)
    if words[-1] != STOP_WORD:
        words.append(STOP_WORD)

    for i in range(len(words) - CHAIN_LEN):
        j = i + CHAIN_LEN + 1
        yield words[i:j]


def extract_words(message):
    symbols = list(re.sub(r"\s", " ", remove_garbage_entities(message)))
    return list(filter(None, map(prettify, symbols.split(" "))))


def prettify(word):
    lowercase_word = word.lower().strip()
    last_symbol = lowercase_word[-1:]
    if last_symbol not in ENDSEN:
        last_symbol = ""
    pretty_word = lowercase_word.strip(GARBAGE)

    if pretty_word != "" and len(pretty_word) > 2:
        return pretty_word + last_symbol
    elif lowercase_word in GARBAGE:
        return None

    return lowercase_word


def random_element(xlist):
    return random.choice(xlist) if xlist else None


def random_end_sentence_token():
    return random_element(list(ENDSEN))


def remove_garbage_entities(message):
    encoding = "utf-16-le"
    utf16bytes = message.text.encode(encoding)
    result = bytearray()
    cur_pos = 0

    for e in message.entities:
        start_pos = e.offset * 2
        end_pos = (e.offset + e.length) * 2

        result += utf16bytes[cur_pos:start_pos]
        if e.type not in GARBAGE_ENTITIES:
            result += utf16bytes[start_pos:end_pos]

        cur_pos = end_pos

    result += utf16bytes[cur_pos:]

    return result.decode(encoding)


def capitalize(string):
    return string[:1].upper() + string[1:]
