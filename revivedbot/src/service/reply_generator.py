from src.config import config, redis, tokenizer, trigram_repository
from src.utils import capitalize, strings_has_equal_letters


class ReplyGenerator:

    def __init__(self):
        self.redis = redis
        self.tokenizer = tokenizer
        self.trigram_repository = trigram_repository

        self.max_wrds = config.getint("grammar", "max_wrds")
        self.max_msgs = config.getint("grammar", "max_msgs")

        self.stop_word = config["grammar"]["stop_word"]
        self.sep = config["grammar"]["sep"]
        self.endsen = config["grammar"]["endsen"]

    def generate(self, message):

        words = self.tokenizer.extract_words(message)

        pairs = [trigram[:-1] for trigram in self.tokenizer.split_to_trigrams(words)]

        messages = [self.__generate_best_message(chat_id=message.chat_id, pair=pair) for pair in pairs]
        longest_message = max(messages, key=len) if len(messages) else None

        if longest_message and strings_has_equal_letters(longest_message, "".join(words)):
            return None

        return longest_message

    def __generate_best_message(self, chat_id, pair):

        best_message = ""
        for _ in range(self.max_msgs):
            generated = self.__generate_sentence(chat_id=chat_id, pair=pair)
            if len(generated) > len(best_message):
                best_message = generated

        return best_message

    def __generate_sentence(self, chat_id, pair):
        gen_words = []
        key = self.sep.join(pair)

        for _ in range(self.max_wrds):
            words = key.split(self.sep)

            gen_words.append(words[1])

            next_word = self.trigram_repository.get_random_reply(chat_id, key)
            if next_word is None:
                break

            key = self.sep.join(words[1:] + [next_word])

        last_word = key.split(self.sep)[-1]
        if last_word not in gen_words:
            gen_words.append(last_word)

        if len(set(gen_words)) == 1:
            gen_words = list(set(gen_words))

        gen_words = [w for w in gen_words if w != self.stop_word]

        sentence = " ".join(gen_words).strip()
        if sentence[-1:] not in self.endsen:

            sentence += self.tokenizer.random_end_sentence_token()

        sentence = capitalize(sentence)

        return sentence
