"""抓取当前微信聊天窗口中我发送的文本消息——实时写文件"""
import wxauto4, time, win32com.client, os, re

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDERS = {'图片', '文件', '[动画表情]', '[链接]', '[小程序]', '[不支持的消息，可在手机上查看]'}
TARGET = 1200
MAX_STEPS = 600


def sanitize_filename(name):
    """将聊天对象名转为安全的文件名"""
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    return name if name else '当前聊天'


def get_output_path(chat_name):
    safe = sanitize_filename(chat_name)
    return os.path.join(OUTPUT_DIR, f'我和{safe}的聊天_我发的消息.txt')


def write_output(msgs, chat_name):
    path = get_output_path(chat_name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'与{chat_name}的聊天中 我 发送的文本消息（按时间从旧到新）\n')
        f.write(f'共 {len(msgs)} 条\n')
        f.write('=' * 50 + '\n\n')
        for i, txt in enumerate(msgs, 1):
            f.write(f'{i}. {txt}\n\n')


def main():
    print('连接微信...', flush=True)
    wechat = wxauto4.WeChat(ads=False)

    # 获取当前聊天对象名字
    chat_name = '当前聊天'
    try:
        cb = wechat.ChatBox
        who = cb.who if hasattr(cb, 'who') else None
        if who:
            chat_name = who
    except Exception:
        pass

    print(f'检测到当前聊天: {chat_name}', flush=True)
    time.sleep(0.5)

    wechat.Show()
    time.sleep(0.3)

    msgbox = wechat.ChatBox.msgbox
    try:
        msgbox.Click(waitTime=0.5)
    except Exception:
        pass
    time.sleep(0.5)

    shell = win32com.client.Dispatch('WScript.Shell')

    all_msgs = []
    seen = set()
    no_new = 0

    # 先取一次初始消息
    try:
        msgs = wechat.GetAllMessage()
        for m in msgs:
            if 'Self' in type(m).__name__:
                c = (m.content.strip() if hasattr(m, 'content') else '').strip()
                if not c or c in PLACEHOLDERS:
                    continue
                if c not in seen:
                    seen.add(c)
                    all_msgs.append(c)
    except Exception as e:
        print(f'初始取消息失败: {e}', flush=True)

    print(f'初始: {len(all_msgs)} 条', flush=True)

    for step in range(1, MAX_STEPS + 1):
        try:
            shell.SendKeys('{PGUP}')
        except Exception:
            pass
        time.sleep(0.12)

        try:
            msgs = wechat.GetAllMessage()
        except Exception as e:
            print(f'[!] step {step} 取消息失败: {e}', flush=True)
            time.sleep(1)
            continue

        added = 0
        for m in msgs:
            if 'Self' not in type(m).__name__:
                continue
            c = (m.content.strip() if hasattr(m, 'content') else '').strip()
            if not c or c in PLACEHOLDERS:
                continue
            if c not in seen:
                seen.add(c)
                all_msgs.append(c)
                added += 1

        if added > 0:
            no_new = 0
            if len(all_msgs) % 10 < added:
                write_output(all_msgs, chat_name)
        else:
            no_new += 1
            if no_new >= 8:
                print(f'→ 已翻到顶，共 {len(all_msgs)} 条', flush=True)
                break

        print(f'step {step:4d} | 新增 {added:3d} | 累计 {len(all_msgs):4d} 条', flush=True)

        if len(all_msgs) >= TARGET:
            print(f'→ 已达到 {TARGET} 条目标', flush=True)
            break

    all_msgs.reverse()
    write_output(all_msgs, chat_name)
    output_path = get_output_path(chat_name)
    print(f'✅ 完成！共 {len(all_msgs)} 条 → {output_path}', flush=True)


if __name__ == '__main__':
    main()
