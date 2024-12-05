from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import PeerChannel
from data import *  
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

# 初始化 Telegram 客户端
client = TelegramClient('session_file', api_id, api_hash)

# 设置监听的群组和对应的目标频道
listened_groups_id = [2249087232, 2033451182,2069614195,2085209250,2008944470,2287822517]  # 源群组ID
fwd_channels = [2334820600, 2260377185,2415244641,2387902791,2299667497,2441480257]  # 目标频道ID

async def main():
    # 启动客户端并设置离线状态
    await client.start()
    await client(UpdateStatusRequest(offline=True))

    if len(listened_groups_id) != len(fwd_channels):
        print("Error: `listened_groups_id` and `fwd_channels` must have the same length.")
        return

    # 为每个目标频道创建 PeerChannel 对象
    destinations = [PeerChannel(channel_id) for channel_id in fwd_channels]

    @client.on(events.NewMessage(incoming=True))
    async def message_handler(event):
        # 检查消息来自哪个群组并确定目标频道
        if event.chat_id in listened_groups_id:
            index = listened_groups_id.index(event.chat_id)
            destination = destinations[index]
            
            message_text = event.raw_text
            print(f"-- Incoming message from {event.input_sender} in group {event.chat_id} --")
            print(f"Forwarding to channel: {destination.channel_id}")
            print(f"Message: {message_text}")

            # 如果消息包含媒体
            if event.media:
                try:
                    # 下载媒体并转发到对应目标频道
                    path = await client.download_media(event.media)
                    await client.send_message(destination, message_text, file=path)
                    print("Media uploaded and forwarded successfully.")
                except Exception as e:
                    print(f"Error while downloading or sending media: {e}")
            else:
                # 仅转发文本消息
                await client.send_message(destination, message_text)

    print('Started, waiting for messages...')
    await client.run_until_disconnected()

# 启动客户端
with client:
    client.loop.run_until_complete(main())
