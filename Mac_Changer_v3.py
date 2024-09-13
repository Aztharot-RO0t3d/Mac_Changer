import curses
import subprocess
import re
import random

def get_arguments():
    return {"interface": None, "new_mac": None, "random": False}

def change_mac(interface, new_mac, stdscr):
    stdscr.addstr(f"[+] Cambiando dirección MAC para {interface} a {new_mac}\n", curses.color_pair(1))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    return mac_address_search_result.group(0) if mac_address_search_result else None

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: f"{x:02x}", mac))

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()

    stdscr.addstr("Cambiador de Dirección MAC\n", curses.A_BOLD | curses.color_pair(1))
    stdscr.refresh()

    stdscr.addstr("\nIntroduce la interfaz: ")
    curses.echo()
    interface = stdscr.getstr().decode('utf-8')

    stdscr.addstr("¿Quieres generar una MAC aleatoria? (s/n): ")
    random_choice = stdscr.getstr().decode('utf-8').lower()
    new_mac = None

    if random_choice == 's':
        new_mac = generate_random_mac()
    else:
        stdscr.addstr("Introduce la nueva dirección MAC: ")
        new_mac = stdscr.getstr().decode('utf-8')

    stdscr.clear()
    stdscr.addstr("Cambiador de Dirección MAC\n", curses.A_BOLD | curses.color_pair(1))
    current_mac = get_current_mac(interface)
    stdscr.addstr(f"MAC actual = {current_mac}\n", curses.color_pair(1) if current_mac else curses.color_pair(2))

    change_mac(interface, new_mac, stdscr)

    current_mac = get_current_mac(interface)
    if current_mac and current_mac.lower() == new_mac.lower():
        stdscr.addstr(f"[+] Dirección MAC cambiada exitosamente a {current_mac}\n", curses.color_pair(1))
    else:
        stdscr.addstr(f"[-] Fallo al intentar cambiar la dirección MAC\n", curses.color_pair(2))

    stdscr.addstr("\nPulsa cualquier tecla para salir...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)