print('HEREISTAKI')
import discord
import os
import random
import time
import mysql.connector
from mysql.connector import Error
from discord.ext import tasks, commands
from enum import Enum

#intents = discord.Intents.all()
#client = discord.Client(intents=intents)

intents = discord.Intents.default()
intents.message_content = True

#client = discord.Client
#client= commands.Bot(command_prefix='$',intents=intents)

bot = commands.Bot(command_prefix='$',intents=intents)


####SQL connectpoint
hostc=''
databasec=''
userc=''
passwordc=''
###################


@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Streaming(name='Burning Arasaka Tower', url='https://www.youtube.com/watch?v=AN1RJF55NXI'))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='How to cook the best Yakitori'))
def get_bank_account(ID):
    #bank_balance=0
    try:
        ##connection point use
        connection = mysql.connector.connect(host=hostc,database=databasec,user=userc,password=passwordc) 
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)

            if cursor.fetchone() is not None:
                #cursor.fetchone()
                #print(cursor.fetchone())
                cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
                bank_balance = cursor.fetchone()
                #bank_balance == bank_balancet[0]                
                print(bank_balance)
                
            else:
                cursor.execute("""INSERT INTO tb_user_bank (`id`, `useroid`, `userolvl`, `balanco`) VALUES (NULL, '%s','1','0')""" %ID)
                print("No user in DB")
                connection.commit()
                print("User Added")
                cursor.execute("""SELECT balanco FROM tb_user_bank WHERE useroid='%s'""" %ID)
                bank_balance = cursor.fetchone()
                #bank_balance == bank_balancet[0]
    except Error as err:
        print("Connection error to DB ", err)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return bank_balance
    
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
                #print(output[0])
                #print(output[1])
                connection.commit()

                bank_balancetemp=output[1]+10
                params=(bank_balancetemp,output[0])
                #print(params)
                #print(bank_balancet[0])
                cursor.execute("""UPDATE tb_user_bank SET balanco='%s' WHERE id='%s'""" %params)
                connection.commit()
                #print(bank_balance_output)
                #bank_balancetemp=row[1]
            else:
                cursor.execute("""INSERT INTO tb_user_bank (`id`, `useroid`, `userolvl`, `balanco`) VALUES (NULL, '%s','1','150')""" %ID)
                print("No user in DB")
                connection.commit()
                print("User Added")
                
    except Error as err:
        print("Connection error to DB ", err)
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return bank_balancetemp
    
@bot.command()
async def ping(ctx):
    print("EasterEgg")
    await ctx.send("You found me. Pong.")
    
@bot.command()    
@commands.cooldown(1,600,commands.BucketType.user)
#@tree.command(description='Get some shiny coins to your pocket!', guild=discord.Object(680007186377998545))
async def payday(ctx):
    print("gold-add-command")
    await ctx.send("My precious...")
    ID=ctx.author.id
    new_balance=str(addto_bank_account(ID))
    feedbackpayday="Fixer przelał pieniążki za zleconko, nowy stan konta: "+ new_balance
    await ctx.reply(feedbackpayday)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    takemura_quotes = [ 
    'Hanako-san nam pomoże','To najlepsze Yakitori jakie jadłem'
]

    if message.content == '.taki':
        response = random.choice(takemura_quotes)
        await message.channel.send(response)
    if message.content =='.bank':
        ID=message.author.id
        #print(ID)
        
        output_balance=get_bank_account(ID)
        print(output_balance[0])
        
        balance=str(output_balance[0])
        feedback="On your bank account there are "+ balance +" eurodollar(s)."
        await message.channel.send(feedback)
    
    #if message.content =='.payday':
     #   ID=message.author.id
      #  payday(ID,
        
        #@client.command()
        #@commands.cooldown
        #if not assign_cooldown():
            
            #ID=message.author.id
            #new_balance=str(addto_bank_account(ID))
           # feedbackpayday="Fixer przelał pieniążki za zleconko, nowy stan konta: "+ new_balance
          #  await message.channel.send(feedbackpayday)
            
         #   return
            
        #await message.channel.send('You are unable to get more golden coins, please wait adventurer!')
        #print('Cooldown')

        #print(ID)
    elif message.content == 'raise-exception':
        raise discord.DiscordException
    await bot.process_commands(message)        
#### DO NOT EDIT ONMESSAGE BELOW THIS LINE

@payday.error        
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Sorry mate, you have to wait for " f"{round(error.retry_after/60,0)} minutes to use that command")
       




    #ID=message.author.id
    #new_balance=str(addto_bank_account(ID))
    #feedbackpayday="Fixer przelał pieniążki za zleconko, nowy stan konta: "+ new_balance
    #await message.channel.send(feedbackpayday)


    #if isinstance(error, commands.CommandOnCooldown):
        
        #interaction.response.send('You are unable to get more golden coins, please wait adventurer!')
        



bot.run('')