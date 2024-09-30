from src.services import redis
from src.utils import capitalize, strings_has_equal_letters, tokenizer

# Global variables replacing the class attributes
max_wrds = 300
max_msgs = 500

stop_word = "\x00"
sep = "\x02"
endsen = ".....!!?"


def get_random_reply(chat_id, key):
    reply = redis.instance().srandmember(f"trigrams:{chat_id}:{key}")
    reply = reply.decode("utf-8") if reply is not None else None

    if reply == stop_word:
        return None

    return reply


def reply(chat_id, message):
    """
    Generates response based on the given message.

    :param message: Message object
    :return: response or None
    """
    words = tokenizer.extract_words(message)
    # print(f"> Reply: words {words}")

    pairs = [trigram[:-1] for trigram in tokenizer.split_to_trigrams(words)]
    # print(f"> Reply: pairs {pairs}")

    messages = [generate_best_message(chat_id, pair=pair) for pair in pairs]
    # print(f"> Reply: messages {messages}")

    longest_message = max(messages, key=len) if messages else None
    # print(f"> Reply: longest_message {longest_message}")

    return longest_message


def generate_best_message(chat_id, pair):
    """
    Generates the longest possible message based on word pairs.

    :param chat_id: chat ID
    :param pair: word pair
    :return: best message
    """
    best_message = ""
    for _ in range(max_msgs):
        generated = generate_sentence(chat_id=chat_id, pair=pair)
        best_message = generated  # Take the latest generated message

    # print(f"> Reply: best_message {best_message}")
    return best_message


def generate_sentence(chat_id, pair):
    """
    Generates a sentence based on the word pair.

    :param chat_id: chat ID
    :param pair: word pair
    :return: generated sentence
    """
    gen_words = []
    key = sep.join(pair)

    for _ in range(max_wrds):
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
    if sentence[-1:] not in endsen:
        sentence += tokenizer.random_end_sentence_token()

    sentence = capitalize(sentence)
    # print(f"> Reply: best_message {sentence}")

    return sentence
