"""
消息转发模块
"""

import logging
import asyncio
import os
from typing import List, Dict, Any, Optional
from telethon import TelegramClient, events, utils
from telethon.tl.types import Message, Channel
from .config import Config

logger = logging.getLogger(__name__)

class MessageForwarder:
    def __init__(self, client: TelegramClient, config: Config):
        """初始化消息转发器"""
        self.client = client
        self.config = config
        self.blacklist = config.blacklist
        self.listened_groups = config.listened_groups_id
        self.fwd_channels = config.fwd_channels
        self.media_dir = "downloaded_media"
        
        # 创建媒体文件下载目录
        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)

    def _is_blacklisted(self, message: Message) -> bool:
        """检查消息是否在黑名单中"""
        if not message.text:
            return False
            
        # 检查完整文本匹配
        if message.text in self.blacklist['text']:
            logger.info(f"消息被完整文本黑名单过滤: {message.text}")
            return True
            
        # 检查关键词匹配
        for keyword in self.blacklist['keywords']:
            if keyword in message.text:
                logger.info(f"消息被关键词黑名单过滤: {keyword}")
                return True
                
        return False

    async def _forward_message(self, message: Message, target_channel_id: int) -> None:
        """转发单条消息到目标频道"""
        try:
            if message.media:
                # 下载媒体文件
                path = await self.client.download_media(message.media, self.media_dir)
                
                if path:
                    # 根据媒体类型处理
                    if utils.is_audio(message.media):
                        await self.client.send_file(target_channel_id, file=path, voice_note=True)
                        if message.text:
                            await self.client.send_message(target_channel_id, message.text)
                        logger.info("语音消息已转发")
                    elif utils.is_video(message.media):
                        await self.client.send_file(target_channel_id, file=path, video_note=True)
                        if message.text:
                            await self.client.send_message(target_channel_id, message.text)
                        logger.info("视频消息已转发")
                    else:
                        await self.client.send_message(target_channel_id, message.text if message.text else "", file=path)
                        logger.info("媒体消息已转发")
                    
                    # 清理下载的媒体文件
                    try:
                        os.remove(path)
                    except Exception as e:
                        logger.warning(f"清理媒体文件失败: {e}")
            else:
                # 纯文本消息
                await self.client.send_message(target_channel_id, message.text)
                logger.info("文本消息已转发")
                
            logger.info(f"消息已转发到频道 {target_channel_id}")
        except Exception as e:
            logger.error(f"转发消息到频道 {target_channel_id} 时出错: {e}")

    async def start(self) -> None:
        """启动消息转发器"""
        @self.client.on(events.NewMessage(chats=self.listened_groups))
        async def handler(event):
            """处理新消息事件"""
            try:
                # 检查消息是否在黑名单中
                if self._is_blacklisted(event.message):
                    return

                # 转发消息到所有目标频道
                for channel_id in self.fwd_channels:
                    await self._forward_message(event.message, channel_id)

            except Exception as e:
                logger.error(f"处理消息时出错: {e}")

        logger.info("消息转发器已启动")
        logger.info(f"监听群组: {self.listened_groups}")
        logger.info(f"转发目标: {self.fwd_channels}")

        # 保持运行
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("收到终止信号，正在停止...")
        except Exception as e:
            logger.error(f"运行时出错: {e}")
        finally:
            await self.client.disconnect()
            logger.info("已断开连接") 