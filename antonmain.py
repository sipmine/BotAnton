import discord
from discord.ext import commands
from config import settings
from bs4 import BeautifulSoup
import requests
import random
import time
#Разрешения
intents = discord.Intents.default()
intents.members = True
from time import perf_counter
from lxml import html
ROLE = 'id'

bot = commands.Bot(command_prefix=settings['prefix'])
bot.remove_command('help')
# Выводит сообщение что бот подключён и работает
Clear_Mute = ['Сюда id ролей у которых будет доступ']
Ban_kick_outher = ['Сюда id ролей у которых будет доступ']

@bot.event
async def on_ready():  # console join and status bot
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('*help'))

# Выдаёт роль автоматом при заходе
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=ROLE)
    await member.add_roles(role)



# Функции бота
@bot.command()
async def help(ctx):
    embed = discord.Embed(title='HELP', color=0xfab319)
    embed.add_field(name='Измерить бибу', value='*bibametr', inline=False)
    embed.add_field(name='Просмотр статистики R6S', value='*stats + nick', inline=False)
    embed.add_field(name='Модераторские команды для администрирования', value="*ban @nik\n*kick @nick\n*clear (кол-во сообщений)", inline=False)
    embed.set_thumbnail(url='https://cdn3.savepice.ru/uploads/2020/10/2/e9938631b115e80241e46497caf4f5ff-full.png')
    await ctx.send(embed=embed)
#закрыть лобби

# тестовая команда для проверки бота
@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.channel.send(f'Hello, {author.mention}!')

# Команада чистит чат *clear (Число сообщений)
@bot.command()
async def clear(ctx, amount=20):  # admin command clear chat
    if discord.utils.get(ctx.author.roles, id=Clear_Mute) is None or discord.utils.get(ctx.author.roles,
                                                                                             id=776142091922833488) is None:
        await ctx.channel.purge(limit=amount)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if discord.utils.get(ctx.author.roles, id=Ban_kick_outher) is None or discord.utils.get(ctx.author.roles,
                                                                                       id=776142091922833488) is None:
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        await ctx.channel.send(f'Бан')


# Команда позваляет кикать участников *kick (@Ник)
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):  # admin command kick player
    if discord.utils.get(ctx.author.roles, id=Ban_kick_outher) is None or discord.utils.get(ctx.author.roles,
                                                                                       id=776142091922833488) is None:
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)

# Шуточная команда
@bot.command()
async def bibametr(ctx):  # bibametr rofl command
    biba = random.randint(1, 50)
    if biba > 31:
        await ctx.channel.send(f'```{biba} Ебать у тебя Монстр!```')
    elif 30 < biba < 31:
        await ctx.channel.send(f'```{biba} ебать у тебя гигант!```')
    elif 20 < biba < 30:
        await ctx.channel.send(f'```{biba} сойдёт```')
    elif 20 > biba >= 10:
        await ctx.channel.send(f'```{biba} ну такое```')
    elif biba < 10:
        await ctx.channel.send(f'```{biba} собалезную```')


# Игра пинг понг
@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'pong')
    guilds = bot.guilds
    print(guilds[0])

#Rainbow six siege function

URL = None
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
RANK_ROLE = {
    'unranked': 783007655437271061,
    'COPPER V': 783004133741166602,
    'COPPER IV': 783004133741166602,
    'COPPER III': 783004133741166602,
    'COPPER II': 783004133741166602,
    'COPPER I': 783004133741166602,
    'BRONZE V': 783004192251838505,
    'BRONZE IV': 783004192251838505,
    'BRONZE III': 783004192251838505,
    'BRONZE II': 783004192251838505,
    'BRONZE I': 783004192251838505,
    'SILVER V': 783004251965489172,
    'SILVER IV': 783004251965489172,
    'SILVER III': 783004251965489172,
    'SILVER II': 783004251965489172,
    'SILVER I': 783004251965489172,
    'GOLD III': 783002165261631508,
    'GOLD II': 783002165261631508,
    'GOLD I': 783002165261631508,
    'PLATINUM III': 778502500453580840,
    'PLATINUM II': 778502500453580840,
    'PLATINUM I': 778502500453580840,
    'DIAMOND': 778502219208589352,
    'CHAMPION': 783006747027046410
}#ваши id
RANK_IMG = {
    'unranked': 'https://i.imgur.com/sB11BIz.png',
    'COPPER V': 'https://i.imgur.com/B8NCTyX.png',
    'COPPER IV': 'https://i.imgur.com/ehILQ3i.jpg',
    'COPPER III': 'https://i.imgur.com/6CxJoMn.jpg',
    'COPPER II': 'https://i.imgur.com/eI11lah.jpg',
    'COPPER I': 'https://i.imgur.com/eI11lah.jpg',
    'BRONZE V': 'https://i.imgur.com/TIWCRyO.png',
    'BRONZE IV': 'https://i.imgur.com/42AC7RD.jpg',
    'BRONZE III': 'https://i.imgur.com/QD5LYD7.jpg',
    'BRONZE II': 'https://i.imgur.com/9AORiNm.jpg',
    'BRONZE I': 'https://i.imgur.com/hmPhPBj.jpg',
    'SILVER V': 'https://i.imgur.com/PY2p17k.png',
    'SILVER IV': 'https://i.imgur.com/D36ZfuR.jpg',
    'SILVER III': 'https://i.imgur.com/m8GToyF.jpg',
    'SILVER II': 'https://i.imgur.com/EswGcx1.jpg',
    'SILVER I': 'https://i.imgur.com/KmFpkNc.jpg',
    'GOLD III': 'https://i.imgur.com/B0s1o1h.jpg',
    'GOLD II': 'https://i.imgur.com/ELbGMc7.jpg',
    'GOLD I': 'https://i.imgur.com/ffDmiPk.jpg',
    'PLATINUM III': 'https://i.imgur.com/tmcWQ6I.png',
    'PLATINUM II': 'https://i.imgur.com/CYMO3Er.png',
    'PLATINUM I': 'https://i.imgur.com/qDYwmah.png',
    'DIAMOND': 'https://i.imgur.com/37tSxXm.png',
    'CHAMPION': 'https://i.imgur.com/VlnwLGk.png'
}#картинки с рангами

@bot.command()
async def stats(ctx, nick):
    start = perf_counter()
    global URL
    website = 'https://r6.tracker.network/profile/pc/'
    URL = website + nick

    def get_html(url):
        global HEADERS
        r = requests.get(url, headers=HEADERS)
        tree = html.fromstring(r.content)
        return r, tree

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='trn-text--dimmed')
        img = soup.find('div', class_='trn-profile-header__avatar').find('img')
        wins_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[5]/div[2]')
        losses_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[6]/div[2]')
        kills_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[6]/div[2]')
        HS_chance_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[1]/div[2]')
        KD_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[2]/div[2]')
        KD = KD_xpath[0].text.strip('\n')
        HS_chance = HS_chance_xpath[0].text.strip('\n')
        kills = kills_xpath[0].text.strip('\n')
        losses = losses_xpath[0].text.strip('\n')
        wins = wins_xpath[0].text.strip('\n')

        ranks = []
        for item in items:
            title = item.get_text(strip=True)
            ranks.append({
                'title': title,
            })

        MMR = ranks[1]['title']
        TRANK = ranks[0]['title']
        #print(MMR, '\n', TRANK, '\n', img['src'], '\n', RANK_IMG[TRANK], '\n', wins, '\n', losses, '\n', kills)

        return MMR, TRANK, img['src'], RANK_IMG[TRANK], wins, losses, HS_chance, KD, kills

    def parse():
        global URL
        html = get_html(URL)[0]
        if html.status_code == 200:
            print('Connect to website')
            mmr_rank = get_content(html.text)
            return mmr_rank
        else:
            print('Error')
    try:
        mmr_rank = parse()
        if mmr_rank[0] in mmr_rank:
            guilds = bot.guilds
            NG = guilds[1]
            print(NG)
            emb = discord.Embed(color=0xfab319)
            emb.set_author(name=nick, icon_url=mmr_rank[2])
            emb.add_field(name='```RANK```', value=f'```{mmr_rank[1]}```')
            emb.add_field(name='```MMR```', value=f'```{mmr_rank[0]}```', inline=False)
            emb.add_field(name='WINS', value=mmr_rank[4], inline=False)
            emb.add_field(name='LOSSES', value=mmr_rank[5], inline=False)
            emb.add_field(name='HEADSHOOTS CHANCE', value=mmr_rank[6], inline=False)
            emb.add_field(name='KILL/DEATH', value=mmr_rank[7], inline=False)
            emb.add_field(name='RANKED KILLS', value=mmr_rank[8], inline=False)
            emb.set_thumbnail(url = mmr_rank[3])
            await ctx.send(embed=emb)
            end = perf_counter()
            print(end - start)
    except Exception as e:
        print(e)


#Система регестрации
messegeid = []
player_rank = []

@bot.command()
async def reg(ctx, nick):
    global URL
    website = 'https://r6.tracker.network/profile/pc/'
    URL = website + nick

    def get_html(url):
        global HEADERS
        r = requests.get(url, headers=HEADERS)
        tree = html.fromstring(r.content)
        return r, tree

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='trn-text--dimmed')
        img = soup.find('div', class_='trn-profile-header__avatar').find('img')
        wins_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[5]/div[2]')
        losses_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[6]/div[2]')
        kills_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[6]/div[2]')
        HS_chance_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[1]/div[2]')
        KD_xpath = get_html(URL)[1].xpath('//*[@id="profile"]/div[3]/div[1]/div[2]/div[2]/div/div[2]/div[2]')
        KD = KD_xpath[0].text.strip('\n')
        HS_chance = HS_chance_xpath[0].text.strip('\n')
        kills = kills_xpath[0].text.strip('\n')
        losses = losses_xpath[0].text.strip('\n')
        wins = wins_xpath[0].text.strip('\n')

        ranks = []
        for item in items:
            title = item.get_text(strip=True)
            ranks.append({
                'title': title,
            })

        MMR = ranks[2]['title']
        TRANK = ranks[0]['title']
        return MMR, TRANK, img['src'], RANK_IMG[TRANK], wins, losses, HS_chance, KD, kills

    def parse():
        global URL
        html = get_html(URL)[0]
        if html.status_code == 200:
            print('Connect to website')
            mmr_rank = get_content(html.text)
            return mmr_rank
        else:
            print('Error')
    await ctx.send(f'Отправлю запрос')
    try:
        mmr_rank = parse()
        if mmr_rank[0] in mmr_rank:
            emb = discord.Embed(color=0xfab319)
            emb.set_author(name=nick, icon_url=mmr_rank[2])
            emb.add_field(name='```RANK```', value=f'```{mmr_rank[1]}```')
            emb.add_field(name='```MMR```', value=f'```{mmr_rank[0]}```', inline=False)
            emb.add_field(name='WINS', value=mmr_rank[4], inline=False)
            emb.add_field(name='LOSSES', value=mmr_rank[5], inline=False)
            emb.add_field(name='HEADSHOOTS CHANCE', value=mmr_rank[6], inline=False)
            emb.add_field(name='KILL/DEATH', value=mmr_rank[7], inline=False)
            emb.add_field(name='RANKED KILLS', value=mmr_rank[8], inline=False)
            emb.set_thumbnail(url = mmr_rank[3])
            mess = await ctx.channel.send(embed=emb)
            await mess.add_reaction('✅')
            @bot.event
            async def on_raw_reaction_add(payload):
                message_id = payload.message_id
                if message_id == message_id:
                    guild_id = payload.guild_id
                    guild = discord.utils.find(lambda g: g.id == guild_id,
                                               bot.guilds)

                    if payload.emoji.name == "✅":  # смайл
                        role = discord.utils.get(guild.roles, id=RANK_ROLE[mmr_rank[1]])
                        #member = guild.get_member(int(payload.user_id))
                        member = payload.member #кто ставил эмоцию
                        if member:
                            if "боты" in [role.name.lower() for role in member.roles]: #Проверка кто поставил эмоцию
                                pass
                            else:
                                await member.add_roles(role)

                        else:
                            print('no found user')
                    else:
                        print("no found role")

    except Exception as e:
        print(e)


#За регестрированые user'ы в разработке
@bot.event
async def on_guild_role_update(before, after, member):
    global URL
    website = 'https://r6.tracker.network/profile/pc/'
    URL = website + member

    def get_html(url):
        global HEADERS
        r = requests.get(url, headers=HEADERS)
        tree = html.fromstring(r.content)
        return r, tree

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='trn-text--dimmed')


        ranks = []
        for item in items:
            title = item.get_text(strip=True)
            ranks.append({
                'title': title,
            })

        MMR = ranks[2]['title']
        TRANK = ranks[0]['title']
        return MMR, TRANK

    def parse():
        global URL
        html = get_html(URL)[0]
        if html.status_code == 200:
            print('Connect to website')
            mmr_rank = get_content(html.text)
            return mmr_rank
        else:
            print('Error')
    pass# тут должно быть если ранг сейчас и
    if after != None:
        pass




bot.run(settings['token'])
