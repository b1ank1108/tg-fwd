"""
频道管理模块
"""

import json
import logging
from typing import List, Dict, Any
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Channel
from .config import Config

logger = logging.getLogger(__name__)

class ChannelManager:
    def __init__(self, client: TelegramClient):
        """初始化频道管理器"""
        self.client = client

    async def get_all_channels(self) -> List[Dict[str, Any]]:
        """获取当前账号所有的频道信息"""
        channels_info = []
        
        try:
            # 获取所有对话
            async for dialog in self.client.iter_dialogs():
                if isinstance(dialog.entity, Channel):
                    channel = dialog.entity
                    
                    # 获取频道信息
                    channel_info = {
                        "id": channel.id,
                        "title": channel.title,
                        "username": channel.username,
                        "participants_count": getattr(channel, 'participants_count', 'unknown'),
                        "is_group": channel.megagroup,
                        "is_broadcast": channel.broadcast,
                        "created_date": getattr(channel, 'date', datetime.now()).isoformat(),
                        "access_hash": str(channel.access_hash),
                    }
                    
                    channels_info.append(channel_info)
                    logger.info(f"找到频道: {channel.title} (ID: {channel.id})")
            
            logger.info(f"共找到 {len(channels_info)} 个频道/群组")
            return channels_info
            
        except Exception as e:
            logger.error(f"获取频道列表时出错: {e}")
            raise

    @staticmethod
    def export_channels_to_file(channels: List[Dict[str, Any]], output_file: str) -> None:
        """将频道信息导出到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(channels, f, ensure_ascii=False, indent=2)
            logger.info(f"频道信息已保存到: {output_file}")
        except Exception as e:
            logger.error(f"导出频道信息到文件时出错: {e}")
            raise 