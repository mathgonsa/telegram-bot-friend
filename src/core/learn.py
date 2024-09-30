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

    redis_instance = redis.instance()
    counter_pipe = redis_instance.pipeline()
    save_pipe = redis_instance.pipeline()

    for trigram in trigrams:
        member = SEPARATOR.join(trigram)

        key = f"trigrams:{chat_id}:{member}"
        last_word = trigram[-1]

        counter_pipe.exists(key)
        save_pipe.sadd(key, last_word)

    counter_key = f"trigrams:count:{chat_id}"
    new_pairs_count = sum(1 if not exists else 0 for exists in counter_pipe.execute())

    save_pipe.incrby(counter_key, new_pairs_count)
    save_pipe.execute()
