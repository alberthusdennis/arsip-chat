import re
import json

def parse_chat(input_file, output_file='chat.json'):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    messages = []
    current = None

    msg_pattern = re.compile(
        r'^(\d{2}/\d{2}/\d{2})\s+(\d{2}\.\d{2})\s+-\s+([^:]+):\s?(.*)$'
    )
    sys_pattern = re.compile(
        r'^(\d{2}/\d{2}/\d{2})\s+(\d{2}\.\d{2})\s+-\s+(.*)$'
    )

    for line in lines:
        line = line.rstrip('\r')

        m = msg_pattern.match(line)
        if m:
            if current: messages.append(current)
            date, time, sender, text = m.groups()
            current = {
                'date': date, 'time': time,
                'sender': sender.strip(),
                'text': text.strip(),
                'type': 'message'
            }
            continue

        s = sys_pattern.match(line)
        if s:
            if current: messages.append(current)
            date, time, text = s.groups()
            current = {
                'date': date, 'time': time,
                'sender': 'system',
                'text': text.strip(),
                'type': 'system'
            }
            continue

        if current:
            current['text'] += '\n' + line

    if current: messages.append(current)

    # Post-processing
    for msg in messages:
        msg['text'] = msg['text'].replace('‚Äé', '').strip()

        if '<Media tidak disertakan>' in msg['text']:
            msg['type'] = 'media'
            msg['text'] = msg['text'].replace('<Media tidak disertakan>', '').strip()

        if '<Pesan ini diedit>' in msg['text']:
            msg['edited'] = True
            msg['text'] = msg['text'].replace('<Pesan ini diedit>', '').strip()

        if msg['text'] in ['Pesan ini dihapus', 'Anda menghapus pesan ini']:
            msg['type'] = 'deleted'
            msg['text'] = ''

        if 'menyematkan pesan' in msg['text']:
            msg['type'] = 'system'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(messages)} pesan berhasil diparsing → {output_file}")

if __name__ == '__main__':
    parse_chat('Chat WhatsApp dengan Yohana.txt')