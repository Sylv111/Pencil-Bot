import discord
from requests import Session
from bs4 import BeautifulSoup as bs
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
import pytz
from random import randint

#List of all things that were modified to be published online:
#ROLEID
#USERNAME
#PASSWORD
#BOTKEY


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event #OnReady
async def on_ready():
    print('Bot is ready!')
    await client.change_presence(activity=discord.Game(name="🐢 V1.2 | https://github.com/Askehraz/JeanZayBot"))

@client.event #Autorole
async def on_member_join(member):
    print(f'{member} has joined the server.')
    role = get(member.guild.roles, id=ROLEID)
    await member.add_roles(role)

@client.event #QuoiFeur
async def on_message(message):
    await client.process_commands(message)
    stripped_message = message.content.lower().strip(" .:?!*\)")

    if stripped_message.endswith("quoi"):
        if randint(1,10) == 1:
            await message.channel.send("https://user-images.githubusercontent.com/56942820/137981144-fe0c2d96-400c-45eb-9033-b96d34ed3a20.mp4")
        else:
            await message.channel.send("feur")


#Code for the homework embed

@client.command() #Start the "tasks.loop"
async def start(ctx):
    DevoirFetch.start(ctx)

@tasks.loop(hours=6.0) #Homework fetched than sent in an embed every 3 hours
async def DevoirFetch(ctx):
    with Session() as s:
        LoginSite = s.get("https://cas.ent.auvergnerhonealpes.fr/login?selection=CLERMONT-ATS_parent_eleve&service=https%3A%2F%2Fjean-zay-thiers.ent.auvergnerhonealpes.fr%2Fsg.do%3FPROC%3DIDENTIFICATION_FRONT&submit=Valider")
        LoginSiteContent = bs(LoginSite.content, "html.parser")
        Token = LoginSiteContent.find("input", {"name":"execution"})["value"]
        LoginData = {"username":"USERNAME","password":"PASSWORD", "selection":"CLERMONT-ATS_parent_eleve", "codeFournisseurIdentite":"ATS-CLERM", "execution":Token, "submit":"Valider", "_eventId":"submit", "geolocation":""}
        s.post("https://cas.ent.auvergnerhonealpes.fr/login?selection=CLERMONT-ATS_parent_eleve&service=https%3A%2F%2Fjean-zay-thiers.ent.auvergnerhonealpes.fr%2Fsg.do%3FPROC%3DIDENTIFICATION_FRONT&submit=Valider",LoginData)
        PageOutput = s.get("https://jean-zay-thiers.ent.auvergnerhonealpes.fr/sg.do?PROC=TRAVAIL_A_FAIRE&ACTION=AFFICHER_ELEVES_TAF&filtreAVenir=true").text

        SoupOutput = bs(PageOutput, 'lxml')
        DataOutput = SoupOutput.find_all('div', class_ = 'panel panel--full panel--no-margin')
        FormattedDataOutput = ""
        for element in DataOutput:
            print(element.text)
            FormattedDataOutput = FormattedDataOutput + "\n" + "\n" + "-" + (element.text)
    print("Data fetched")
    TimezoneFrance = pytz.timezone('Europe/Paris')
    DatetimeFrance = datetime.now(TimezoneFrance)
    TimeFranceFormatted = DatetimeFrance.strftime("%H:%M")
    DateTimeFranceFormatted = DatetimeFrance.strftime("%d/%m/%Y")
    print("Fetched on",TimeFranceFormatted)

    embedDevoir = discord.Embed(
    title = '📝 Devoirs',
    description = FormattedDataOutput,
    colour = discord.Colour.gold()
    )
    embedDevoir.set_footer(text="(Physique-Chimie/Allemand non inclu dans la liste)\nDonnées prises automatiquement de ENT Auvergne-Rhône-Alpes")
    embedDevoir.set_author(name='Données mise à jour à ' + TimeFranceFormatted + " le " + DateTimeFranceFormatted, icon_url='https://user-images.githubusercontent.com/56942820/136627456-a9e1b467-5f2d-4248-92b1-e16baabec5e7.png')
    await ctx.send(embed=embedDevoir)


client.run('BOTKEY')
