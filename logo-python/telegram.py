import os
import telebot
import requests
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Update

API_KEY = "1966553578:AAFxn1UzRKey8BWMmoGWLdYXXAJIGApZC2Q"
bot = telebot.TeleBot("1966553578:AAFxn1UzRKey8BWMmoGWLdYXXAJIGApZC2Q")
sessionId=""
FirmCode=""
FirmTitle=""



  
options = []
options.append(InlineKeyboardButton(text='New Firm', callback_data='/newfirm'))
options.append(InlineKeyboardButton(text='New Contact', callback_data='2'))
options.append(InlineKeyboardButton(text='New Task', callback_data='3'))
options.append(InlineKeyboardButton(text='New Proposal', callback_data='4'))
options.append(InlineKeyboardButton(text='New Ticket', callback_data='5'))
reply_markup = InlineKeyboardMarkup([options])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "You can choose what you want just put a /")

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# bot.reply_to(message, message.text)

 

@bot.message_handler(commands=['Commands'])
def send_welcome(message):
	# bot.reply_to(message, "Howdy, how are you doing?")
  bot.send_message(message.chat.id, text='What would you like to do?', reply_markup=reply_markup)



@bot.message_handler(commands=['login'])
def login(message):
    global sessionId
    res = requests.post('localhost.tr/LogoCRMRest/api/v1.0/login?authorization=code')
    sessionId = res.json()['SessionId']
    bot.reply_to(message, "login succesful with sessionid :"+sessionId)


#newfirm
@bot.message_handler(commands=['newfirm'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "What is your FirmCode?")
    bot.register_next_step_handler(sent_msg, firm_code_handler) #Next message will call the firm_code_handler function
   
def firm_code_handler(pm):
    global FirmCode
    firm_code = pm.text
    FirmCode=firm_code
    sent_msg = bot.send_message(pm.chat.id, f"Your FirmCode is {firm_code}. What is your FirmTitle?")
    bot.register_next_step_handler(sent_msg,firm_title_handler, firm_code) 

def firm_title_handler(pm, firm_code):
    global FirmTitle
    firm_title = pm.text
    FirmTitle=firm_title
    bot.send_message(pm.chat.id, f"Your name is {firm_code}, and your firm_title is {firm_title}.")
    pload = {
      "FirmCode": FirmCode,   
      "FirmTitle": FirmTitle 
    }
    res = requests.post('localhost.com.tr/LogoCrmRest/api/v1.0/firms', 
    params= {'SessionId' :  sessionId},json = pload)
    bot.send_message(pm.chat.id, "sessionid :"+sessionId+"FirmCode :"+FirmCode + "FirmTitle :"+FirmTitle)
    print(res)


#newcontat
@bot.message_handler(commands=['newcontact'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "What is your Firstname?")
    bot.register_next_step_handler(sent_msg, Firstname_handler) 
   
def  Firstname_handler(pm):
    first_name= pm.text
    sent_msg = bot.send_message(pm.chat.id, f"Your firstname is {first_name}. What is your lastname?")
    bot.register_next_step_handler(sent_msg,lastname_handler, first_name) 

def lastname_handler(pm, first_name):
    last_name = pm.text
    bot.send_message(pm.chat.id, f"Your lastname is {last_name}")
    pload = {
      "FirstName": first_name,   
      "LastName": last_name 
    }
    res = requests.post('localostcom.tr/LogoCRMRest/api/v1.0/contacts?', 
    params= {'SessionId' :  sessionId},json = pload)
    bot.send_message(pm.chat.id, "sessionid :"+sessionId+"FirstName :"+ first_name + "LastName :"+last_name)
    print(res)
    

#newtask
@bot.message_handler(commands=['newtask'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "What is Description for new task?")

def description_handler(pm):
    description  = pm.text
    bot.send_message(pm.chat.id, f"Your description is {description}")
    pload = {
      "Description": description 
    }
    res = requests.post('localost.com.tr/LogoCRMRest/api/v1.0/tasks?', 
    params= {'SessionId' :  sessionId},json = pload)
    bot.send_message(pm.chat.id, "sessionid :"+sessionId+"Description :"+ description)
    print(res)

#newticket   
@bot.message_handler(commands=['newticket'])
def welcome(pm):
    sent_msg = bot.send_message(pm.chat.id, "What is TicketDescription for new ticket?")

def TicketDescription_handler(pm):
    Ticket_Description  = pm.text
    bot.send_message(pm.chat.id, f"Your description is {Ticket_Description}")
    pload = {
      "TicketDescription": Ticket_Description
    }
    res = requests.post('localost.com.tr/LogoCRMRest/api/v1.0/tickets?', 
    params= {'SessionId' :  sessionId},json = pload)
    bot.send_message(pm.chat.id, "sessionid :"+sessionId+" TicketDescription :"+ Ticket_Description)
    print(res)


@bot.message_handler(commands=['newfirmadd'])
def upload_new_firm(message):
    pload = {
      "FirmCode": FirmCode,   
      "FirmTitle": FirmTitle 
    }
    res = requests.post('localost.com.tr/LogoCrmRest/api/v1.0/firms', 
    params= {'SessionId' :  sessionId},json = pload)
    bot.reply_to(message, "sessionid :"+sessionId+"FirmCode :"+FirmCode + "FirmTitle :"+FirmTitle)
    print(res)

bot.polling()     

