import discord, datetime, time, flask, requests, json, threading, os, random, httpx, tls_client, sys
from flask import request
from pathlib import Path
from threading import Thread
from discord_webhook import DiscordWebhook, DiscordEmbed
from boosting import *
from sellpass import SellPass

orders = []

config = json.load(open("config.json", encoding="utf-8"))


def getinviteCode(invite_input): #gets invite CODE
    if "discord.gg" not in invite_input:
        return invite_input
    if "discord.gg" in invite_input:
        invite = invite_input.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_input:
        invite = invite_input.split("https://discord.gg/")[1]
        return invite
    

@app.route("/sellix", methods=["GET", "POST"])
def sellix():
    data = request.json
    if data in orders:    
        pass
    elif data not in orders:
        threading.Thread(target=start_sellix, args=[data, ]).start()
        orders.append(data)
    return '{"status": "received"}', 200


def start_sellix(data):
    try:
        if 'boosts' in data['data']['product_title'].lower():
            nick = ''
            invite_link = ''
            
            for i in data['data']['custom_fields']:
                
                if i == config['field_name_invite']:
                    invite_link = data['data']['custom_fields'][i]
                    
            if nick == "":
                nick = config['server_nick'].capitalize()
                
            
            if data['data']['product_title'].replace(" ", "-").split("-")[0].isdigit():
                amount = int(data['data']['product_title'].replace(" ", "-").split("-")[0])
                
            months = 3 if "3" in data['data']['product_title'].split("[")[1] else 1
            invite = getinviteCode(invite_link)
            
            order_id = data['data']['uniqid']
            customer_email = data['data']['customer_email']
            product_name = data['data']['product_title']
            
            if amount % 2 != 0:
                amount += 1
                
            embed = DiscordEmbed(title = "**New Sellix Order**", description = f"**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months", color = '4598d2')
            embed.set_timestamp()
            webhook = DiscordWebhook(url=config["order_log_webhook"])
            webhook.add_embed(embed)
            webhook.execute()
            print()
            sprint(f"Boosting https://discord.gg/{invite}, {amount} times for {months} months", True)
            start = time.time()
            boosted = thread_boost(invite, amount, months, nick)
            end = time.time()
            time_taken = round(end - start, 2)
            
            if boosted == False:
                with open('success.txt', 'w') as f:
                    for line in variables.success_tokens:
                        f.write(f"{line}\n")
                
                with open('failed.txt', 'w') as g:
                    for line in variables.failed_tokens:
                        g.write(f"{line}\n")
            
            
                embed2 = DiscordEmbed(title = "**Boosts Unsuccessful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 'c80000')
                embed2.set_timestamp()
                webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
                webhook.add_embed(embed2)
                webhook.execute()
                print()
                sprint(f"Failed to Boost https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", False)
                print()
                
                webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
                with open("success.txt", "rb") as f:
                    webhook.add_file(file=f.read(), filename='success.txt')
                with open("failed.txt", "rb") as f:
                    webhook.add_file(file=f.read(), filename='failed.txt')
                webhook.execute()
                
                os.remove("success.txt")
                os.remove("failed.txt")
                
            elif boosted:
                with open('success.txt', 'w') as f:
                    for line in variables.success_tokens:
                        f.write(f"{line}\n")
                
                with open('failed.txt', 'w') as g:
                    for line in variables.failed_tokens:
                        g.write(f"{line}\n")
                        
                embed3 = DiscordEmbed(title = "**Boosts Successful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = '4598d2')
                embed3.set_timestamp()
                webhook = DiscordWebhook(url=config["boost_log_webhook"])
                webhook.add_embed(embed3)
                webhook.execute()
                print()
                sprint(f"Boosted https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", True)
                print()
                
                webhook = DiscordWebhook(url=config["boost_log_webhook"])
                with open("success.txt", "rb") as f:
                    webhook.add_file(file=f.read(), filename='success.txt')
                with open("failed.txt", "rb") as f:
                    webhook.add_file(file=f.read(), filename='failed.txt')
                webhook.execute()
                
                os.remove("success.txt")
                os.remove("failed.txt")
                
        else:
            pass
    
    except Exception as e:
        #sprint(f"{e} | Function: Start_Sellix", False)
        pass
    
    
@app.route("/sellapp", methods=["GET", "POST"])
def sellapp():
    data = request.json
    if data in orders:    
        pass
    elif data not in orders:
        threading.Thread(target=start_sellapp, args=[data, ]).start()
        orders.append(data)
    return 'Our server has received your order.', 200


def start_sellapp(data):
    try:
        nick = ''
        invite_link = ''

        for i in data['additional_information']:
            print(i)
            if i['label'] == config['field_name_invite']:
                invite_link = i['value']
                

        
        if nick == "":
            nick = config['server_nick'].capitalize()
        
            
        elif data['listing']['slug'].split("-")[0].isdigit():
            amount = int(data['listing']['slug'].split("-")[0])
            
        months = 3 if "3" in data['listing']['title'].split("[")[1] else 1
        invite = getinviteCode(invite_link)
        
        order_id = data['invoice']['id']
        customer_email = data['invoice']['payment']['gateway']['data']['customer_email']
        product_name = data['listing']['title']
        
        if amount % 2 != 0:
            amount += 1
            
            
        embed = DiscordEmbed(title = "**New Sell.App Order**", description = f"**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months", color = '4598d2')
        embed.set_timestamp()
        webhook = DiscordWebhook(url=config["order_log_webhook"])
        webhook.add_embed(embed)
        webhook.execute()
        print()
        sprint(f"Boosting https://discord.gg/{invite}, {amount} times for {months} months", True)
        start = time.time()
        boosted = thread_boost(invite, amount, months, nick)
        end = time.time()
        time_taken = round(end - start, 2)
        
        if boosted == False:
            with open('success.txt', 'w') as f:
                for line in variables.success_tokens:
                    f.write(f"{line}\n")
            
            with open('failed.txt', 'w') as g:
                for line in variables.failed_tokens:
                    g.write(f"{line}\n")
        
        
            embed2 = DiscordEmbed(title = "**Boosts Unsuccessful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 'c80000')
            embed2.set_timestamp()
            webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
            webhook.add_embed(embed2)
            webhook.execute()
            print()
            sprint(f"Failed to Boost https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", False)
            print()

            webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
            with open("success.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='success.txt')
            with open("failed.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='failed.txt')
            webhook.execute()
            
            os.remove("success.txt")
            os.remove("failed.txt")
                
        elif boosted:
            with open('success.txt', 'w') as f:
                for line in variables.success_tokens:
                    f.write(f"{line}\n")
            
            with open('failed.txt', 'w') as g:
                for line in variables.failed_tokens:
                    g.write(f"{line}\n")
                    
            embed3 = DiscordEmbed(title = "**Boosts Successful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = '4598d2')
            embed3.set_timestamp()
            webhook = DiscordWebhook(url=config["boost_log_webhook"])
            webhook.add_embed(embed3)
            webhook.execute()
            print()
            sprint(f"Boosted https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", True)
            print()

            webhook = DiscordWebhook(url=config["boost_log_webhook"])
            with open("success.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='success.txt')
            with open("failed.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='failed.txt')
            webhook.execute()
            
            os.remove("success.txt")
            os.remove("failed.txt")
            
    except Exception as e:
        #sprint(f"{e} | Function: Start_Sellapp", False)
        pass
    
    
    
@app.route("/sellpass", methods=["GET", "POST"])
def sellpass():
    received = request.json
    if received in orders:    
        pass
    elif received not in orders:
        threading.Thread(target=start_sellpass, args=[received, ]).start()
        orders.append(received)
    return 'Our server has received your request.', 200


def start_sellpass(received):
    try:
        api_key = config['sellpass_api_key']
        sp = SellPass(
            api_key = api_key
            )

        shop_id = sp.get_public_shop()[0]["shop"]["id"]


        order_id = received['InvoiceId']
        
        nick = ''
        invite_link = ''

        header = {"Authorization": f"Bearer {api_key}"}
        r = httpx.get(f"https://dev.sellpass.io/self/{shop_id}/invoices/{order_id}", headers = header)
        product_name = r.json()['data']['partInvoices'][0]['product']['title']
        
        for i in r.json()['data']['partInvoices'][0]['customFields']:
            
            if i['customField']['name'] == config['field_name_invite']:
                invite_link = i['valueString']
            

        
        customer_email = r.json()['data']['customerInfo']['customerForShop']['customer']['email']
        
        invite = getinviteCode(invite_link)
        months = 3 if "3" in product_name.lower().split("[")[1] else 1
        
                
        if product_name.replace(" ", "-").split("-")[0].isdigit():
            amount = int(product_name.replace(" ", "-").split("-")[0])
            
        if amount % 2 != 0:
            amount += 1
        
        embed = DiscordEmbed(title = "**New SellPass Order**", description = f"**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months", color = '4598d2')
        embed.set_timestamp()
        webhook = DiscordWebhook(url=config["order_log_webhook"])
        webhook.add_embed(embed)
        webhook.execute()
        print()
        sprint(f"Boosting https://discord.gg/{invite}, {amount} times for {months} months", True)
        start = time.time()
        boosted = thread_boost(invite, amount, months, nick)
        end = time.time()
        time_taken = round(end - start, 2)
        
        if boosted == False:
            with open('success.txt', 'w') as f:
                for line in variables.success_tokens:
                    f.write(f"{line}\n")
            
            with open('failed.txt', 'w') as g:
                for line in variables.failed_tokens:
                    g.write(f"{line}\n")
        
        
            embed2 = DiscordEmbed(title = "**Boosts Unsuccessful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 'c80000')
            embed2.set_timestamp()
            webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
            webhook.add_embed(embed2)
            webhook.execute()
            print()
            sprint(f"Failed to Boost https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", False)
            print()
            
            webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
            with open("success.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='success.txt')
            with open("failed.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='failed.txt')
            webhook.execute()
            
            os.remove("success.txt")
            os.remove("failed.txt")
            
        elif boosted:
            with open('success.txt', 'w') as f:
                for line in variables.success_tokens:
                    f.write(f"{line}\n")
            
            with open('failed.txt', 'w') as g:
                for line in variables.failed_tokens:
                    g.write(f"{line}\n")
                    
            embed3 = DiscordEmbed(title = "**Boosts Successful**", description = f"**Boost Type: **Automatic\n**Order ID: **{order_id}\n**Product Name: **{product_name}\n**Customer Email: **{customer_email}\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = '4598d2')
            embed3.set_timestamp()
            webhook = DiscordWebhook(url=config["boost_log_webhook"])
            webhook.add_embed(embed3)
            webhook.execute()
            print()
            sprint(f"Boosted https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", True)
            print()
            
            webhook = DiscordWebhook(url=config["boost_log_webhook"])
            with open("success.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='success.txt')
            with open("failed.txt", "rb") as f:
                webhook.add_file(file=f.read(), filename='failed.txt')
            webhook.execute()
            
            os.remove("success.txt")
            os.remove("failed.txt")
                
    except Exception as e:
        #sprint(f"{e} | Function: Start_Sellpass", False)
        pass



def run():
    app.run(host="0.0.0.0", port="6969")
    
    
def keep_alive():
    t = Thread(target=run)
    t.start()
    
fingerprint_modification()
