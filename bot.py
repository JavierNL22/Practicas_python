import telebot
TOKEN = "1700941902:AAH2geWU0e5SXHqw2I86ZiLLQ0DK5uJLCNI"
bot = telebot.TeleBot(TOKEN)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Para python-333459f9156b.json', scope)
client=gspread.authorize(creds)
sheet = client.open("TELEGRAM").sheet1

@bot.message_handler(commands=['ayuda','help'])
def send_welcome(message):
    texto = f'''
    Comando /start para comenzar la partida, indicar posición /info para ver tabla con posiciones, tras cada turno se envia una actualizacion del tablero y pasa el turno al siguiente jugador, /end si la partida ha terminado para limpiar el tablero.
    '''
    bot.reply_to(message, texto)

activador = False

@bot.message_handler(commands=['start'])
def mensaje_comienzo(message):
    global activador
    activador = True
    texto = '''
    Empieza la partida, comienza X
    '''
    bot.reply_to(message, texto)

lista = ["X","O","X","O","X","O","X","O","X"]
contador = 0
tablero = ["A1","A2","A3","B1","B2","B3","C1","C2","C3"]

@bot.message_handler(commands=['end'])
def limpiar_tablero(message):
    global contador
    global tablero
    global activador
    bot.reply_to(message, "La partida ha terminado")
    for i in tablero:
            sheet.update_acell(i, "_")
    contador = 0
    activador = False

@bot.message_handler(commands=['info'])
def mensaje_posiciones(message):
    texto = '''
    A1 B1 C1
A2 B2 C2
A3 B3 C3
    '''
    bot.reply_to(message, texto)

@bot.message_handler(func= lambda message: True, content_types=['text'])
def partida(message):
    global tablero
    global contador
    global activador
    if activador == True:
    	if contador == 9:
    		bot.reply_to(message, "La partida ha terminado")
    		for i in tablero:
    			sheet.update_acell(i, "_")
    		contador = 0
    		activador = False
    	else:
    		ficha = lista[contador]
    		sheet.update_acell(message.text, ficha)
    		A1 = sheet.acell('A1').value
    		A2 = sheet.acell('A2').value
    		A3 = sheet.acell('A3').value
    		B1 = sheet.acell('B1').value
    		B2 = sheet.acell('B2').value
    		B3 = sheet.acell('B3').value
    		C1 = sheet.acell('C1').value
    		C2 = sheet.acell('C2').value
    		C3 = sheet.acell('C3').value
    		texto =f'''
    		{A1} {B1} {C1}
{A2} {B2} {C2}
{A3} {B3} {C3}
    		'''
    		contador = contador + 1
    		if sheet.acell('E3').value == "O":
    			for i in tablero:
    				sheet.update_acell(i, "_")
    			contador = 0
    			activador = False
    			bot.reply_to(message, "La parida ha termiando,ganador O")
    		elif sheet.acell('E3').value == "X":
    			for i in tablero:
    				sheet.update_acell(i, "_")
    			contador = 0
    			activador = False
    			bot.reply_to(message, "La partida ha terminado, ganador X")
    		bot.reply_to(message, texto)

bot.polling()
