import time


MODIFIERS = {
    "CONTROL": 0x01,
    "CTRL": 0x01,
    "SHIFT": 0x02,
    "ALT": 0x04,
    "WINDOWS": 0x08,
    "GUI": 0x08,
}


KEYS = {
    "ENTER": "\n",
    "RETURN": "\n",
    "TAB": "\t",
    "SPACE": " ",
}


def run_commands(text, kb):

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        cmd = parts[0].upper()


        if cmd == "DELAY":
            delay_ms = int(parts[1])
            time.sleep_ms(delay_ms)
            continue


        if cmd == "TEXT":
            phrase = raw_line[len("TEXT "):]
            kb.send(phrase)
            continue


        if cmd in KEYS:
            kb.send(KEYS[cmd])
            continue


        if cmd in MODIFIERS:
            mod = MODIFIERS[cmd]
            if len(parts) < 2:
                continue

            key = parts[1]

            if len(key) == 1:
                kb.press(mod, key)
            elif key.upper() in KEYS:
                kb.press(mod, KEYS[key.upper()])
            else:

                kb.press(mod, key)
            continue


        kb.send(raw_line)