# GroupMaid

基于 [pyrogram](https://github.com/pyrogram/pyrogram) 和 Pillow 的 Telegram 群组实用 Bot。

[//]: # (本项目包含 Binary v2.034 的 [Noto Emoji]&#40;https://github.com/googlefonts/noto-emoji&#41; 。)

## 特性

~~饼画好了，什么时候圆不知道~~（

讨论群相关：

- [x] 解除频道消息置顶
- [x] 移除加入群的成员
  -  解封时间为 1min，误触加入稍等待即可正常使用频道评论

通用：

- [x] 删除并封禁以频道身份发出的消息
  - 不会封禁关联频道和匿名管理员

TODO：

- [ ] 删除并封禁以频道身份发出的消息 - 频道白名单
- [ ] 入群验证问题
- [ ] Support other languages (e.g. English)

## 使用

- *(Optional, but strongly recommended)* 创建 `venv` 并激活
- `pip install -r requirements.txt`
- 复制一份 `bot.ini.sample` 并重命名为 `bot.ini`，填入 [Telegram API ID & Hash](https://my.telegram.org) 和管理员用户 ID
- 在 [@BotFather](https://t.me/BotFather) 处创建 Bot，获取 API Token
- `python -m bot` 并使用 API Token 登录
- 在与 Bot 的聊天中配置 Bot

注：如果你不知道如何获取用户 ID 和频道 / 群聊 ID，Google for how-to

## LICENSE

[GPLv3](./LICENSE)