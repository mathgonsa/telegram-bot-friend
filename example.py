from src.core.learn import learn
from src.core.reply import generate_reply

chat_id = "-1001726117958"
message = "Maskara partir pra tomar uma skoooooooooool"

learn(chat_id, message)
print("> Reply:", generate_reply(chat_id, message))
