from src.services import redis
from src.utils.tokenizer import extract_words, split_to_trigrams


def learn(chat_id: str, message: str):
    print(f"> Learn: message {message}")
    words = extract_words(message)
    print(f"> Learn: words {words}")
    trigrams = split_to_trigrams(words)

    return store(chat_id, trigrams)


def store(chat_id, trigrams):

    counter_pipe = redis.instance().pipeline()
    save_pipe = redis.instance().pipeline()

    for trigram in trigrams:
        key = f"trigrams:{chat_id}:{trigram[:-1]}"
        last_word = trigram[-1]

        counter_pipe.exists(key)
        save_pipe.sadd(key, last_word)

    counter_key = f"trigrams:count:{chat_id}"

    new_pairs_count = sum(map(lambda x: 1 if x == 0 else 0, counter_pipe.execute()))

    save_pipe.incrby(counter_key, new_pairs_count)
    save_pipe.execute()
