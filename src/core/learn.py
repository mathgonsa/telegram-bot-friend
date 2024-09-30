from src.services import redis
from src.utils.tokenizer import extract_words, split_to_trigrams

SEPARATOR = " "


def learn(chat_id: str, message: str):
    print(f"> Learn: message {message}")

    words = extract_words(message)
    print(f"> Learn: words {words}")
    trigrams = split_to_trigrams(words)

    return store(chat_id, trigrams)


def store(chat_id: str, trigrams):
    cursor = redis.instance()

    save_pipe = cursor.pipeline()

    for trigram in trigrams:
        member = SEPARATOR.join(trigram)

        key = f"trigrams:{chat_id}:{member}"
        last_word = trigram[-1]

        save_pipe.sadd(key, last_word)

    save_pipe.execute()
