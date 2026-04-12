import pinlayout
from led import update_led
from arm import arm_shorted
from flash import *
from hidkbd import Keyboard
from ducky import run_commands

kb = Keyboard()



def program_mode():
    print("PROGRAM MODE")
    print("Send text over USB serial. End with 'EOF' on its own line.")

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            continue

        if line == "EOF":
            break

        lines.append(line)

    text = "\n".join(lines)

    print("Clearing flash...")
    clear_chip()

    print("Writing flash...")
    write_all(text)
    print("Done. Rebooting recommended.")




def payload_mode():
    script = read_all()
    run_commands(script, kb)



def main():
    update_led()

    if arm_shorted():
        payload_mode()
    else:
        # Programming mode
        program_mode()


main()