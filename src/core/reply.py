from src.services import redis
from src.utils import capitalize, tokenizer

MAX_WORDS = 300
MAX_MESSAGES = 1
STOP_WORD = "\x00"
SEPARATOR = " "
END_SENTENCE = ".....!!?"


def get_random_reply(chat_id, key):
    member = f"trigrams:{chat_id}:{key}"

    reply = redis.instance().srandmember(member)
    return reply.decode("utf-8") if reply and reply != STOP_WORD else None


def generate_reply(chat_id, message):
    words = tokenizer.extract_words(message)

    pairs = [trigram for trigram in tokenizer.split_to_trigrams(words)]

    messages = [generate_best_message(chat_id, pair) for pair in pairs]

    if not messages:
        return None
    best_message = max(messages, key=len)
    print("> Reply:", best_message)
    return best_message


def generate_best_message(chat_id, pair):
    best_message = ""
    for _ in range(MAX_MESSAGES):
        best_message = generate_sentence(chat_id, pair)
    return best_message


def generate_sentence(chat_id, pair):
    gen_words = []
    key = SEPARATOR.join(pair)

    for _ in range(MAX_WORDS):
        words = key.split(SEPARATOR)
        gen_words.append(words[1])

        next_word = get_random_reply(chat_id, key)

        if next_word is None:
            break

        key = SEPARATOR.join([words[1], next_word])

    last_word = key.split(SEPARATOR)[-1]
    if last_word not in gen_words:
        gen_words.append(last_word)

    gen_words = list(set(w for w in gen_words if w != STOP_WORD))

    sentence = " ".join(gen_words).strip()
    if sentence[-1:] not in END_SENTENCE:
        sentence += tokenizer.random_end_sentence_token()

    return capitalize(sentence)
