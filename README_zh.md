# 📨 Telegram 频道转发工具

[English](README.md)

<div align="center">
  <img src="https://registry.npmmirror.com/@lobehub/icons-static-svg/1.44.0/files/icons/cursor.svg" alt="Cursor" width="32" height="32" />
  <p>使用 Cursor 开发</p>
</div>

### 🎯 简介
Telegram频道转发工具是一个专门用于在禁用原生转发功能时转发消息的工具。它在以下情况特别有用：
- 源频道禁用了消息转发功能
- 需要同时转发消息到多个频道
- 需要使用黑名单过滤某些消息

### ✨ 功能特点
- 支持从多个源频道转发到多个目标频道
- 支持文本、图片、视频、文档等多种媒体类型
- 支持黑名单过滤（关键词和全文匹配）
- 导出频道列表便于配置
- 生成带频道信息的配置模板
- 离线模式运行（转发时显示为离线）

### 🚀 安装方法
1. 克隆仓库：
```bash
git clone https://github.com/yourusername/tg-fwd.git
cd tg-fwd
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 获取Telegram API凭据：
- 访问 https://my.telegram.org/apps
- 创建新应用
- 记下`api_id`和`api_hash`

### ⚙️ 配置说明
1. 导出频道列表：
```bash
python main.py --export-channels channels.json
```
这将创建：
- `channels.json`：详细的频道信息
- `channels_config.yaml`：带频道ID的配置模板

2. 编辑配置文件：
```yaml
telegram:
  api_id: 123456               # 你的API ID
  api_hash: "abcdef1234567890" # 你的API Hash
  session_name: "tg_fwd"       # 会话文件名

blacklist:
  text:                        # 包含这些文本的消息将被过滤
    - "禁止转发"
    - "广告"
  keywords:                    # 匹配这些关键词的消息将被过滤
    - "测试"
    - "spam"

channels:
  listened_groups_id:          # 源频道ID列表
    - -1001234567890
    - -1009876543210
  fwd_channels:               # 目标频道ID列表（与源频道一一对应）
    - -1002345678901
    - -1002109876543
```

### 🔧 使用方法
1. 运行转发器：
```bash
python main.py -c config.yaml
```

2. 导出频道列表：
```bash
python main.py --export-channels channels.json
```

3. 生成配置模板：
```bash
python main.py --generate-template config.yaml
```

### 📋 基本要求
- Python 3.7 或更高版本
- 有效的 Telegram API 密钥（api_id 和 api_hash）

### ⚠️ 重要说明
- 机器人需要是源频道和目标频道的成员
- 对于频道，需要具有管理员权限
- 转发消息时机器人将显示为离线状态
- 消息实时转发（收到后立即转发）
- `listened_groups_id` 和 `fwd_channels` 必须有相同的长度，且一一对应
- 大规模使用可能导致账号被限制，请遵守 Telegram 的使用政策
- 媒体文件会先下载到本地，然后再上传到目标频道，确保有足够的磁盘空间

### 🔍 故障排除
如果遇到问题，请查看 `tg_fwd.log` 日志文件，其中包含详细的运行信息和错误记录。

### 📄 许可证
本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。 