import logging
import re
from pathlib import Path
from typing import Optional, Callable, List

from httpx import AsyncClient
from khl import Bot, Message, MessageTypes

with open('cookie', 'r') as f:
    cookie = f.readline()

emojis = {
    '128516': '20201001',
    '128512': '20201001',
    '128578': '20201001',
    '128579': '20201001',
    '128515': '20201001',
    '128513': '20201001',
    '128522': '20201001',
    '128519': '20201001',
    '128518': '20201001',
    '128514': '20201001',
    '129315': '20201001',
    '128517': '20201001',
    '128521': '20201001',
    '128535': '20201001',
    '128537': '20201001',
    '128538': '20201001',
    '128536': '20201001',
    '128525': '20201001',
    '129392': '20201001',
    '129321': '20201001',
    '128539': '20201001',
    '128541': '20201001',
    '128523': '20201001',
    '128540': '20201001',
    '129322': '20201001',
    '129297': '20201001',
    '129394': '20201001',
    '129303': '20201001',
    '129323': '20201001',
    '129325': '20201001',
    '129762': '20211115',
    '129763': '20211115',
    '129296': '20201001',
    '128566': '20201001',
    '129300': '20201001',
    '129320': '20201001',
    '128528': '20201001',
    '128529': '20201001',
    '128566-8205-127787-65039': '20210218',
    '128527': '20201001',
    '128524': '20201001',
    '128556': '20201001',
    '128580': '20201001',
    '128530': '20201001',
    '128558-8205-128168': '20210218',
    '128542': '20201001',
    '128532': '20201001',
    '129317': '20201001',
    '129393': '20201001',
    '128554': '20201001',
    '128564': '20201001',
    '129316': '20201001',
    '128567': '20201001',
    '129298': '20201001',
    '129301': '20201001',
    '129314': '20201001',
    '129326': '20201001',
    '129319': '20201001',
    '129397': '20201001',
    '129398': '20201001',
    '128565': '20201001',
    '129396': '20201001',
    '129760': '20211115',
    '129327': '20201001',
    '129312': '20201001',
    '129395': '20201001',
    '129400': '20201001',
    '129488': '20201001',
    '128526': '20201001',
    '128533': '20201001',
    '129764': '20211115',
    '128543': '20201001',
    '128577': '20201001',
    '128558': '20201001',
    '128559': '20201001',
    '128562': '20201001',
    '128551': '20201001',
    '128550': '20201001',
    '128552': '20201001',
    '128560': '20201001',
    '128561': '20201001',
    '128563': '20201001',
    '129761': '20211115',
    '129765': '20211115',
    '129401': '20211115',
    '129402': '20201001',
    '129299': '20201001',
    '128546': '20201001',
    '128557': '20201001',
    '128549': '20201001',
    '128531': '20201001',
    '128555': '20201001',
    '128553': '20201001',
    '128547': '20201001',
    '128534': '20201001',
    '128544': '20201001',
    '128545': '20201001',
    '129324': '20201001',
    '128548': '20201001',
    '128520': '20201001',
    '128127': '20201001',
    '128169': '20201001',
    '128128': '20201001',
    '128125': '20201001',
    '128123': '20201001',
    '129302': '20201001',
    '129313': '20201001',
    '127875': '20201001',
    '127801': '20201001',
    '127804': '20201001',
    '127799': '20201001',
    '127800': '20210218',
    '128144': '20201001',
    '127797': '20201001',
    '127794': '20201001',
    '129717': '20211115',
    '127821': '20201001',
    '129361': '20201001',
    '127798-65039': '20201001',
    '127820': '20211115',
    '127827': '20210831',
    '127819': '20210521',
    '127818': '20211115',
    '127874': '20201001',
    '129473': '20201001',
    '129472': '20201001',
    '127789': '20201001',
    '127838': '20210831',
    '9749': '20201001',
    '127869-65039': '20201001',
    '129440': '20201001',
    '9924': '20201001',
    '127882': '20201001',
    '127880': '20201001',
    '128142': '20201001',
    '128139': '20201001',
    '128148': '20201001',
    '128140': '20201001',
    '128152': '20201001',
    '128159': '20201001',
    '128149': '20201001',
    '128158': '20201001',
    '128147': '20201001',
    '128151': '20201001',
    '10084-65039-8205-129657': '20210218',
    '10084-65039': '20201001',
    '129505': '20201001',
    '128155': '20201001',
    '128154': '20201001',
    '128153': '20201001',
    '128156': '20201001',
    '129294': '20201001',
    '129293': '20201001',
    '128420': '20201001',
    '128150': '20201001',
    '128157': '20201001',
    '127873': '20211115',
    '127895-65039': '20201001',
    '127942': '20211115',
    '129351': '20220203',
    '129352': '20220203',
    '129353': '20220203',
    '127941': '20220203',
    '128240': '20201001',
    '127911': '20210521',
    '128175': '20201001',
    '128064': '20201001',
    '127751': '20210831',
    '128371-65039': '20201001',
    '129668': '20210521',
    '128302': '20201001',
    '128293': '20201001',
    '128081': '20201001',
    '128049': '20201001',
    '129409': '20201001',
    '128047': '20220110',
    '128053': '20201001',
    '128584': '20201001',
    '128055': '20201001',
    '129412': '20210831',
    '129420': '20201001',
    '128016': '20210831',
    '129433': '20201001',
    '128038': '20210831',
    '129417': '20210831',
    '128039': '20211115',
    '129415': '20201001',
    '128029': '20201001',
    '128375-65039': '20201001',
    '128034': '20201001',
    '128025': '20201001',
    '128060': '20201001',
    '128059': '20210831',
    '128040': '20201001',
    '129445': '20201001',
    '128048': '20201001',
    '128045': '20201001',
    '129428': '20201001',
    '128054': '20211115',
    '128041': '20211115',
    '129437': '20211115',
    '128012': '20210218',
    '129410': '20210218',
    '128031': '20210831',
    '127757': '20201001',
    '127774': '20201001',
    '127775': '20201001',
    '11088': '20201001',
    '127772': '20201001',
    '127771': '20201001',
    '128171': '20201001',
    '127752': '20201001',
    '9729-65039': '20201001',
}

emoji_to_codes: Callable[[str], List[int]] = lambda c: list(map(lambda x: ord(x), c))
codes_to_unicode: Callable[[List[int]], str] = lambda codes: "-".join(list(map(lambda code: f"u{code:x}", codes)))

logging.basicConfig(level='DEBUG')

bot = Bot(cookie)


async def mix_emoji(emoji_1: str, emoji_2: str) -> Optional[bytes]:
    codes_1 = emoji_to_codes(emoji_1)
    try:
        path = emojis["-".join([str(i) for i in codes_1])]
    except KeyError:
        return

    unicode_1 = codes_to_unicode(codes_1)
    unicode_2 = codes_to_unicode(emoji_to_codes(emoji_2))

    url = f"https://www.gstatic.com/android/keyboard/emojikitchen/{path}/{unicode_1}/{unicode_1}_{unicode_2}.png"
    try:
        async with AsyncClient() as client:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
    except Exception:
        return
    else:
        return resp.content


async def emoji(msg: Message):
    match = re.match(r'^([\u200d-\U0001fab5]+)\+([\u200d-\U0001fab5]+)$', msg.content.replace(' ', ''))
    print(match)
    if match:
        emoji_1, emoji_2 = match.group(1), match.group(2)
        for i in ((emoji_1, emoji_2), (emoji_2, emoji_1)):
            ret = await mix_emoji(*i)

            if ret:
                path = Path() / 'mixed.png'
                path.write_bytes(ret)
                url = await bot.client.create_asset(path.__str__())
                await msg.ctx.channel.send(url, type=MessageTypes.IMG)
                return

        await msg.ctx.channel.send('不支持的Emoji')


bot.client.register(MessageTypes.TEXT, emoji)
bot.client.register(MessageTypes.KMD, emoji)

bot.run()
