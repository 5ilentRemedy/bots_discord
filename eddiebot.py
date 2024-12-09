print('EDDIEINDAHOUSE')
import discord
import os
import random
import time
import mysql.connector
from mysql.connector import Error
from discord.ext import tasks, commands
from enum import Enum


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$',intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Dungeons & Dragons'))

####SQL connectpoint
hostc=''
databasec=''
userc=''
passwordc=''
###################
def get_bank_account(ID):
    try:
        connection = mysql.connector.connect(host=hostc,database=databasec,user=userc,password=passwordc)
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
            if cursor.fetchone() is not None:
                cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
                bank_balance = cursor.fetchone()                
                print(bank_balance)
            else:
                cursor.execute("""INSERT INTO tb_user_bank (`id`, `useroid`, `userolvl`, `balanco`) VALUES (NULL, '%s','1','0')""" %ID)
                connection.commit()
                print("No user in DB")
                print("User Added")
                cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
                bank_balance = cursor.fetchone()
    except Error as err:
        print("Connection error to DB ", err)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return bank_balance
###################
def addto_bank_account(ID):
    id_userindb=0
    bank_balancetemp=0

    try:
        connection = mysql.connector.connect(host=hostc,database=databasec,user=userc,password=passwordc)   
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("""SELECT id,balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
            if cursor.fetchone() is not None:
                cursor.execute("""SELECT id,balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
                output = cursor.fetchone()
                connection.commit()
                bank_balancetemp=output[1]+10
                params=(bank_balancetemp,output[0])
                cursor.execute("""UPDATE tb_user_bank SET balanco='%s' WHERE id='%s'""" %params)
                connection.commit()
            else:
                cursor.execute("""INSERT INTO tb_user_bank (`id`, `useroid`, `userolvl`, `balanco`) VALUES (NULL, '%s','1','10')""" %ID)
                print("No user in DB")
                connection.commit()
                print("User Added")
                bank_balancetemp=10
    except Error as err:
        print("Connection error to DB ", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return bank_balancetemp
####################################

@bot.command()    
@commands.cooldown(1,600,commands.BucketType.user)
async def coins(ctx):
    print("gold-add-command")
    await ctx.send("My precious...")
    ID=ctx.author.id
    new_balance=str(addto_bank_account(ID))
    feedbackpayday="Here you go adventurer! You got more shiny coins in your pocket, now you got "+ new_balance+ " golden coins"
    await ctx.reply(feedbackpayday)

@bot.command()
async def ping(ctx):
    print("EasterEgg")
    await ctx.send("You found me. Pong.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    eddie_quotes = ['The Shire, The Shire Is Burning. So Mordor It Is.','This Is Music!','Never Change, Promise Me.','I Mean, Look At Us. We ARE Heroes.','This Is So Stupid. This Is So Stupid. S***! S***! S***!',
    'I Think It’s My Year, Henderson. I Think It’s Finally My Year.','I Didn’t Run Away This Time, Right?'
]
#QUOTE OF EDDIE
    if message.content == '.equote':
        response = random.choice(eddie_quotes)
        await message.channel.send(response)
        #await bot.process_commands(message)
    if message.content == '.ehi':
        if message.author.nick=='None':
            
            usernick=message.author.nick
            ehireply="Hello " + usernick + "! What exciting things awaits us now?"
            await message.channel.send(ehireply)
        else:
            username=message.author.name
            ehireply="Hello " + username + "! What exciting things awaits us now?"
            await message.channel.send(ehireply)  
        #await bot.process_commands(message)
#CALL TRAUMA
    if message.content == '.help':
        response = '<@&1085225669065199817>, user needs medical assitance here!'
        await message.channel.send(response)
        #await bot.process_commands(message)

    if message.content =='.bank':
        ID=message.author.id
        
        output_balance=get_bank_account(ID)
        print(output_balance[0])
        
        balance=str(output_balance[0])
        feedback="You got "+ balance +" golden coins."
        await message.channel.send(feedback)
    elif message.content == 'raise-exception':
        raise discord.DiscordException
    await bot.process_commands(message)

@coins.error        
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Sorry mate, you have to wait for " f"{round(error.retry_after/60,0)} minutes to use that command")
       

bot.run('')