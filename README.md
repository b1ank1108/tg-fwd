# 📨 Telegram Channel Forwarder

[中文说明](README_zh.md)

<div align="center">
  <img src="https://registry.npmmirror.com/@lobehub/icons-static-svg/1.44.0/files/icons/cursor.svg" alt="Cursor" width="32" height="32" />
  <p>Developed with Cursor</p>
</div>

### 🎯 Introduction
Telegram Channel Forwarder is a tool designed to forward messages between Telegram channels/groups when the native forwarding feature is disabled. This is particularly useful when:
- The source channel has disabled message forwarding
- You need to forward messages to multiple channels simultaneously
- You want to filter certain messages using blacklist

### ✨ Features
- Forward messages from multiple source channels to multiple target channels
- Support text, images, videos, documents, and other media types
- Message filtering with blacklist (keywords and full text matching)
- Export channel list for easy configuration
- Offline mode operation while forwarding

### 🚀 Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/tg-fwd.git
cd tg-fwd
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your Telegram API credentials:
- Visit https://my.telegram.org/apps
- Create a new application
- Note down your `api_id` and `api_hash`

### ⚙️ Configuration
1. Export your channel list:
```bash
python main.py --export-channels channels.json
```
This will create a `channels.json` file with detailed channel information.

2. Edit the configuration file:
```yaml
telegram:
  api_id: 123456               # Your API ID
  api_hash: "abcdef1234567890" # Your API Hash
  session_name: "tg_fwd"       # Session file name

blacklist:
  text:                        # Messages containing these texts will be filtered
    - "Forwarding disabled"
    - "AD"
  keywords:                    # Messages matching these keywords will be filtered
    - "test"
    - "spam"

channels:
  listened_groups_id:          # Source channel IDs
    - -1001234567890
    - -1009876543210
  fwd_channels:               # Target channel IDs (in corresponding order)
    - -1002345678901
    - -1002109876543
```

### 🔧 Usage
1. Run the forwarder:
```bash
python main.py -c config.yaml
```

2. Export channel list:
```bash
python main.py --export-channels channels.json
```

### ⚠️ Notes
- The bot needs to be a member of both source and target channels
- For channels, you need to be an administrator
- Messages are forwarded as they are received (real-time)
- Media files are temporarily downloaded before forwarding
- The bot operates in offline mode while forwarding messages

### 📋 Prerequisites
- Python 3.7 or higher
- Valid Telegram API credentials (api_id and api_hash)

### 🔍 Troubleshooting
Check the `tg_fwd.log` file for detailed running information and error logs.

### 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 