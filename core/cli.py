"""
命令行工具模块
"""

import os
import sys
import logging
import asyncio
import argparse
from typing import Optional
from telethon import TelegramClient

from .config import Config
from .channel_manager import ChannelManager
from .forwarder import MessageForwarder

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Telegram消息转发机器人')
    
    parser.add_argument('-c', '--config', 
                      help='配置文件路径',
                      default='config.yaml')
                      
    parser.add_argument('--export-channels',
                      help='导出频道列表到指定文件',
                      metavar='FILE')
    
    return parser.parse_args()

async def export_channels(client: TelegramClient, output_file: str):
    """导出频道列表"""
    try:
        channel_manager = ChannelManager(client)
        channels = await channel_manager.get_all_channels()
        channel_manager.export_channels_to_file(channels, output_file)
    except Exception as e:
        logger.error(f"导出频道列表失败: {e}")
        sys.exit(1)

async def run_forwarder(client: TelegramClient, config: Config):
    """运行消息转发器"""
    try:
        forwarder = MessageForwarder(client, config)
        await forwarder.start()
    except Exception as e:
        logger.error(f"运行消息转发器失败: {e}")
        sys.exit(1)

async def main_async():
    """异步主函数"""
    args = parse_args()
    
    try:
        # 加载配置
        config = Config(args.config)
        
        # 创建客户端
        client = TelegramClient(
            config.session_name,
            config.api_id,
            config.api_hash
        )
        
        # 启动客户端
        await client.start()
        
        # 处理命令行参数
        if args.export_channels:
            await export_channels(client, args.export_channels)
        else:
            await run_forwarder(client, config)
            
    except KeyboardInterrupt:
        logger.info("收到终止信号，正在停止...")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            await client.disconnect()

def main():
    """主函数"""
    asyncio.run(main_async()) 