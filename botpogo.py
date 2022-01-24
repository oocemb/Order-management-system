import telebot
from pyowm import OWM
#def async():pass
#bot = telebot.TeleBot("5252287449:AAERORAX4jk8UwDy46CXkvHwN8oczASQl34")

owm = OWM('6d00d1d4e704068d70191bad2673e0cc', language="ru")
obs = owm.weather_at_place('Сочи')
w = obs.get_weather()
temp = w.get_temperature('celsius')["temp"]

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            tb.send_message(chatid, "В сочи " + w.get_detailed_status())
            tb.send_message(chatid, "Температура у тебя" + str(temp))
            if temp < 5:
                tb.send_message(chatid, "Морозец ждет твою жопку")
            elif temp < 15:
                tb.send_message(chatid, "Жить можно жди лето")
            elif temp > 15:
                tb.send_message(chatid,"Да что ты знаешь о холоде сопляк")
            tb.send_message(chatid, temp)


tb = telebot.TeleBot('5252287449:AAERORAX4jk8UwDy46CXkvHwN8oczASQl34')
tb.set_update_listener(listener) #register listener
tb.polling()
#Use none_stop flag let polling will not stop when get new message occur error.
tb.polling(none_stop=True)
# Interval setup. Sleep 3 secs between request new message.
tb.polling(interval=3)

while True: # Don't let the main Thread end.
    pass