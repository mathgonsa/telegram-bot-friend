from src.config import *
from src.services import redis
from src.utils import tokenizer


def generate(message):

    words = tokenizer.extract_words(message)
    print(f"> Reply: words {words}")

    pairs = [trigram[:-1] for trigram in tokenizer.split_to_trigrams(words)]
    print(f"> Reply: pairs {pairs}")

    messages = [generate_best_message(chat_id=message.chat_id, pair=pair) for pair in pairs]
    print(f"> Reply: messages {messages}")

    longest_message = max(messages, key=len) if len(messages) else None
    print(f"> Reply: longest_message {longest_message}")

    return longest_message


def generate_best_message(chat_id, pair):
    best_message = ""
    for _ in range(MAX_MESSAGES):
        generated = generate_sentence(chat_id=chat_id, pair=pair)
        if len(generated) > len(best_message):

            best_message = generated

    print(f"> Reply: best_message {best_message}")
    return best_message


def generate_sentence(chat_id, pair):
    gen_words = []

    sep = "\x02"
    stop_word = "\x00"

    key = sep.join(pair)

    for _ in range(MAX_WORDS):
        words = key.split(sep)

        gen_words.append(words[1])

        next_word = get_random_reply(chat_id, key)
        if next_word is None:
            break

        key = sep.join(words[1:] + [next_word])

    last_word = key.split(sep)[-1]
    if last_word not in gen_words:
        gen_words.append(last_word)

    if len(set(gen_words)) == 1:
        gen_words = list(set(gen_words))

    gen_words = [w for w in gen_words if w != stop_word]

    sentence = " ".join(gen_words).strip()
    if sentence[-1:] not in END_SENTENCE:
        sentence += tokenizer.random_end_sentence_token()

    sentence = tokenizer.capitalize(sentence)
    print(f"> Reply: best_message {sentence}")
    return sentence


def get_random_reply(chat_id, key):
    stop_word = "\x00"
    source_name = "trigrams:{}:{}"

    reply = redis.instance().srandmember(source_name.format(chat_id, key))
    reply = reply.decode("utf-8") if reply is not None else None

    if reply == stop_word:
        return None

    return reply
