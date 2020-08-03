import requests
import os
import re
import json
import urllib
import sys
import telebot
reload(sys)
sys.setdefaultencoding("UTF8")



token = "" #ISI DENGAN BOT TOKEN KAMU
owner_id = "942592519"  #ISI DENGAN USER ID KAMU


















import bs4
heder = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
}

def gsearch(query):
    src = requests.get("https://www.google.com/search?q="+urllib.quote(query)).text
    return re.findall('<a href="/url\?q\=(.*?)\&amp;',src)

class brainlyparse:
    def __init__(self,url):
        self.result = []
        source = requests.get(url, headers = heder).text
        parse = bs4.BeautifulSoup(source,"html.parser")
        self.soal = parse.find("span", class_="sg-text sg-text--large sg-text--bold sg-text--break-words brn-qpage-next-question-box-content__primary").text
        self.mapel,self.sekolah = [i.text for i in parse.findAll("span",itemprop="name",class_="sg-text sg-text--xsmall sg-text--gray-secondary sg-text--link")]
        self.p = [i.text.replace("\n","",1)[::-1].replace("\n","")[::-1] for i in parse.findAll("span",role="link",class_="sg-text sg-text--bold sg-text--small sg-text--gray sg-text--gray sg-text--link")]
        self.ans = [i.text.replace("\n","",1)[::-1].replace("\n","")[::-1] for i in parse.findAll("div",class_="sg-text js-answer-content brn-rich-content")]
        self.answ = [i.findAll("p") for i in parse.findAll("div",class_="sg-text js-answer-content brn-rich-content")]
        self.lk = [i.text for i in parse.findAll("span",class_="js-thanks-button-counter")]
        self.result.append([self.p[0],self.ans[0],self.lk[0]])
        self.result.append([self.p[1],self.ans[1],self.lk[1]]) if len(self.p) == 2 else None



user = []
reply = """
-  Detail Soal
   Pertanyaan : {}
   Mata Pelajaran : {}
   Tingkat Soal : {}
   Original Url : {}

=========================



-  Jawaban 1
{}

Penjawab : {}
Terima Kasih : {}



"""
j2 = """
- Jawaban 2
{}

Penjawab : {}
Terima Kasih : {}

"""
bot = telebot.TeleBot(token)
user = open("user.txt").read().splitlines()
def ln(msg):
   global user
   try:
    for i in msg:
        chat_id = i.chat.id
        if i.content_type == "text":
           text = i.text
           print (text)
           if text == "/start" or str(chat_id) not in user:
              bot.send_message(chat_id,"Selamat datang,semoga bot ini membantumu!")
              user.append(str(chat_id))
              open("user.txt","w").write("\n".join(user))
              user=open("user.txt").read().splitlines()
              print("Total User : {}".format(len(user)))
           elif text == "/search":
              bot.send_message(chat_id,"Penggunaan : /search pertanyaan\n\nContoh : /search sebutkan hal yang menyebabkan inflasi")
           elif text.startswith("/search ") or text.startswith("/search@Brainly_ID_BOT "):
              jawaban = ""
              urlo = gsearch(text.replace("/search ","").replace("/search@Brainly_ID_BOT ","")+" site:brainly.co.id")[0]
              datot = brainlyparse(urlo)
              jbw = datot.result
              jbw2 = datot.answ
              if len(jbw2) != 0:
                 if jbw2[0] != []:
                    fuki = "\n".join([i.text for i in jbw2[0]])
                 else:
                    fuki = jbw[0][1]
              if len(jbw2) == 2:
                 if jbw2[1] != []:
                    fuki2 = "\n".join([i.text for i in jbw2[1]])
                 elif jbw2[1] == []:
                    fuki2 = jbw[1][1]
              if len(jbw) != 0:
                 jawaban += reply.format(datot.soal,datot.mapel,datot.sekolah,urlo,fuki,jbw[0][0],jbw[0][2])
              if len(jbw) == 2:
                  jawaban += j2.format(fuki2,jbw[1][0],jbw[1][2])
              jawaban += "\nMade with luv by JustA Hacker"
              bot.send_message(chat_id,jawaban.replace("\\n","\n"))
              print urlo
           else:
              bot.send_message(chat_id,"Unknown Command,Type /search to search answer from brainly")
   except Exception as e :print e;bot.send_message(chat_id,"Error : {}".format(e))
bot.set_update_listener(ln)
try:
  bot.polling()
  bot.polling(none_stop=True)
  bot.polling(interval=0)
  while True:
    pass
except:pass
