"""
配置管理模块
"""

import yaml
import logging
import sys
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_path: str = 'config.yaml'):
        """初始化配置"""
        self.config_path = config_path
        self.config = self._load_config()
        
        # 验证并加载配置
        self.telegram = self.config['telegram']
        self.api_id = self.telegram['api_id']
        self.api_hash = self.telegram['api_hash']
        self.session_name = self.telegram.get('session_name', 'session_file')
        
        self.blacklist = self.config['blacklist']
        self.channels = self.config['channels']
        
        # 设置频道相关属性
        self.listened_groups_id = self.channels['listened_groups_id']
        self.fwd_channels = self.channels['fwd_channels']
        
        # 验证频道配置
        if len(self.listened_groups_id) != len(self.fwd_channels):
            raise ValueError("错误: `listened_groups_id` 和 `fwd_channels` 必须有相同的长度。")

    def _load_config(self) -> Dict[str, Any]:
        """从YAML文件加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as config_file:
                return yaml.safe_load(config_file)
        except FileNotFoundError:
            logger.error(f"配置文件 {self.config_path} 未找到。请确保配置文件存在。")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"解析配置文件时出错: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"加载配置文件时发生未知错误: {e}")
            sys.exit(1) 