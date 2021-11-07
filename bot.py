import qrcode
import cv2
import requests
import telebot
import os

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN, parse_mode=None)
print("Bot is working!")



# /start or /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi!\n\nSend me any link or text and I will make a QR-code from it.\nOR\nYou can send me any image with QR-code and I will try to scan it.")



# Text
@bot.message_handler(content_types=['text'])
def send_qrcode(message):
    if message.text == "https://www.youtube.com/watch?v=dQw4w9WgXcQ":
        bot.reply_to(message, "Bruh. No.")
    else:
        type(qrcode.make(message.text))
        qrcode.make(message.text).save("qrcode-"+str(message.from_user.id)+"-"+str(message.message_id)+".png")
        bot.send_photo(message.chat.id, photo=open("qrcode-"+str(message.from_user.id)+"-"+str(message.message_id)+".png", "rb"), caption="Value: "+message.text)
        os.remove("qrcode-"+str(message.from_user.id)+"-"+str(message.message_id)+".png")



# Photo
@bot.message_handler(content_types=['photo'])
def read_qrcode(message):
    #Load photo
    global TOKEN
    file_info = bot.get_file(message.photo[-1].file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
    open("qrcode-read-"+str(message.from_user.id)+"-"+str(message.message_id)+".jpg", "wb").write(bot.download_file(file_info.file_path))

    #Decode
    img=cv2.imread("qrcode-read-"+str(message.from_user.id)+"-"+str(message.message_id)+".jpg")
    det=cv2.QRCodeDetector()
    val, pts, st_code=det.detectAndDecode(img)

    #Is empty?
    if val == "":
        bot.reply_to(message, "There is no QR-code here\nOr try to send me a better image")
    elif val == "https://www.youtube.com/watch?v=dQw4w9WgXcQ":
        bot.reply_to(message, "Never gonna give you up :P")
    else:
        bot.reply_to(message, "QR-code contains:\n"+val)

    os.remove("qrcode-read-"+str(message.from_user.id)+"-"+str(message.message_id)+".jpg")




#Wait for next command
bot.polling( none_stop = True)
