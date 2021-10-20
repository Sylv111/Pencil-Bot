import discord
from requests import Session
from bs4 import BeautifulSoup as bs
from datetime import datetime
from discord.ext import commands, tasks
from discord.utils import get
import pytz
from random import randint
import itertools

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
    await client.change_presence(activity=discord.Game(name="🐢 V1.3 | https://github.com/Askehraz/JeanZayBot"))

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
        RandomVideoFeur = randint(1,10)
        if RandomVideoFeur == 1:
            await message.channel.send("http://askehraz.fr/upload/TheoFeur.mp4")
        elif RandomVideoFeur == 2:
            await message.channel.send("http://askehraz.fr/upload/MinecraftFeur.mp4")
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
        DataOutputDate = SoupOutput.find_all('p', class_ = 'p-like slug slug--xs text--slate')

        DataOutputPrint = list(itertools.chain.from_iterable(zip(DataOutputDate,DataOutput)))

        FormattedDataOutput = ""
        NbOfElement = 0
        for element in DataOutputPrint:
            print(element.text)
            if (NbOfElement % 2) == 0:
                FormattedDataOutput = FormattedDataOutput + "\n" + "\n" + (element.text.capitalize())
                NbOfElement = NbOfElement + 1
            else:
                FormattedDataOutput = FormattedDataOutput + "\n" + "-" + (element.text)
                NbOfElement = NbOfElement + 1

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