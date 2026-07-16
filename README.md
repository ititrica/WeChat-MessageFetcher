# WeChat Message Fetcher

抓取微信聊天窗口中你发送的文本消息，自动滚动加载历史记录，实时写入本地文件（用来把自己炼化成聊天skill）。

## 原理

基于 [wxauto4](https://pypi.org/project/wxauto4/) 操作微信 Windows 客户端 UI，模拟 PageUp 向上翻页，逐条提取你发出的文本消息并去重。

## 使用

1. 微信已登录，打开目标聊天窗口（**不要最小化**）
2. 安装依赖

   ```bash
   pip install wxauto4
   ```

3. 双击 `抓取聊天记录.bat`，或运行

   ```bash
   python fetch_msgs.py
   ```

4. 等待自动完成，输出文件：`我和{对方}_我发的消息.txt`

## 文件

| 文件 | 说明 |
|------|------|
| `fetch_msgs.py` | 主脚本 |
| `抓取聊天记录.bat` | 快捷启动（Windows） |
| `.gitignore` | 屏蔽抓取结果和日志文件 |

## 参数

脚本顶部常量可自行调整：

```python
TARGET = 1200      # 抓取目标条数
MAX_STEPS = 600    # 最大滚动步数（防死循环）
```
