from telethon import TelegramClient, events,utils
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.tl.types import PeerChannel
from dotenv import load_dotenv
import os, yaml


# 加载 YAML 配置文件
with open('config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.safe_load(config_file)

# 从配置中提取 API ID 和 API Hash
api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']

# 黑名单和频道配置
blacklist = config['blacklist']
channels = config['channels']


# 初始化 Telegram 客户端
client = TelegramClient('session_file', api_id, api_hash)


async def main():
    # 启动客户端并设置离线状态
    await client.start()
    await client(UpdateStatusRequest(offline=True))

    if len(channels['listened_groups_id']) != len(channels['fwd_channels']):
        print("Error: `listened_groups_id` and `fwd_channels` must have the same length.")
        return

    # 为每个目标频道创建 PeerChannel 对象
    destinations = [PeerChannel(channel_id) for channel_id in channels['fwd_channels']]

    @client.on(events.NewMessage(incoming=True,chats=channels['listened_groups_id']))
    async def message_handler(event):
        # 检查消息来自哪个群组并确定目标频道
        message_text = event.raw_text
        to_id = event.message.to_id
        
        if any(black_word in message_text for black_word in blacklist['text']) or message_text in blacklist['keywords']:
            print("Message is in the blacklist. Not forwarding.")
            return
        
        index = channels['listened_groups_id'].index(getattr(to_id, 'channel_id', None))
        destination = destinations[index]
        
        print(f"-- Incoming message from {event.input_sender} in group {event.message.to_id} --")
        print(f"Forwarding to channel: {destination.channel_id}")
        print(f"Message: {message_text}")

        # 如果消息包含媒体
        if event.media:
            try:
                path = await client.download_media(event.media)
                if utils.is_audio(event.media):
                    await client.send_file(destination, file=path,voice_note=True)
                    await client.send_message(destination, message_text)
                    print("voice uploaded and forwarded successfully.")
                elif utils.is_video(event.media):
                    await client.send_file(destination, file=path, video_note=True)
                    await client.send_message(destination, message_text)
                    print("video uploaded and forwarded successfully.")
                else:
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
