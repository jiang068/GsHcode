
from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event

codec_sv = SV('涩涩密文转换器')

# 密码表
codebook = ['齁', '哦', '噢', '喔', '咕', '咿', '嗯', '啊', '～', '哈', '！', '唔', '哼', '❤', '呃', '呼']
#             0    1    2    3    4    5    6    7   FF5E   9   10   11   12   13   14   15
#                               ↑ 这里明确是全角 U+FF5E

codebook_map = {ch: idx for idx, ch in enumerate(codebook)}

def encode_text(text: str) -> str:
    encoded = ''
    for b in text.encode('utf-8'):
        high = (b >> 4) & 0x0F
        low = b & 0x0F
        encoded += codebook[high] + codebook[low]
    return encoded

def decode_text(code: str) -> str:
    code = ''.join(ch for ch in code if ch in codebook_map)  # 去除非法字符
    if len(code) % 2 != 0:
        return '密文长度错误'
    try:
        byte_list = []
        for i in range(0, len(code), 2):
            high = codebook_map.get(code[i])
            low = codebook_map.get(code[i + 1])
            if high is None or low is None:
                return '密文含非法字符'
            byte_list.append((high << 4) | low)
        return bytes(byte_list).decode('utf-8')
    except Exception:
        return '解码失败'

@codec_sv.on_command(('h编码',), block=True)
async def handle_encode(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send('用法：h编码 原文内容')
        return
    await bot.send(encode_text(ev.text))

@codec_sv.on_command(('h解码',), block=True)
async def handle_decode(bot: Bot, ev: Event):
    if not ev.text:
        await bot.send('用法：h解码 密文内容')
        return
    await bot.send(decode_text(ev.text))

@codec_sv.on_command(('h帮助',), block=True)
async def handle_help(bot: Bot, ev: Event):
    await bot.send(
        '📖 涩涩密文转换器使用说明：\n\n'
        '👉 编码原文为涩涩密文：\n'
        'h编码 我喜欢你\n\n'
        '👉 解码涩涩密文：\n'
        'h解码 ❤呼咕咿❤呼唔齁哈唔哈咕噢呼齁啊～\n\n'
        '✨ 原理：使用 UTF-8 每字节两字符编码。'
    )