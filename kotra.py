import curses
import time
import datetime
import string

def draw_logo(stdscr):
    logo = """
██████╗   █████████╗   ██████╗
██╔══██╗  ╚══██╔══╝  ██╔════╝
██████╔╝     ██║     ██║     
██╔══██╗     ██║     ██║     
██████╔╝     ██║     ╚██████╗
╚═════╝      ╚═╝      ╚═════╝

    """
    height, width = stdscr.getmaxyx()
    y_offset = (height - logo.count('\n')) // 2
    x_offset = (width - max(len(line) for line in logo.split('\n'))) // 2
    stdscr.attron(curses.color_pair(1))
    for i, line in enumerate(logo.split('\n'), start=y_offset):
        stdscr.addstr(i, x_offset, line)
    stdscr.attroff(curses.color_pair(1))

def draw_datetime(stdscr):
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    stdscr.addstr(curses.LINES - 2, curses.COLS - len(dt_string) - 2, dt_string)

def display_user_info(stdscr, email, password, balance, status):
    color = 1  # Rouge
    height, width = stdscr.getmaxyx()
    border_win = curses.newwin(7, 40, height // 2 - 3, width // 2 - 20)
    border_win.attron(curses.color_pair(2))  # Couleur bleue
    border_win.box()
    border_win.addstr(1, 2, f"Email: {email}")
    border_win.addstr(2, 2, f"Password: {'*' * len(password)}")
    border_win.addstr(3, 2, f"User: Multiple BTC")
    border_win.addstr(4, 2, f"BTC Balance: {balance:.8f}")
    border_win.addstr(5, 2, status)
    border_win.attroff(curses.color_pair(2))  # Couleur bleue
    border_win.refresh()

def display_history(stdscr, history):
    max_entries = min(20, len(history))
    height, width = stdscr.getmaxyx()
    border_win = curses.newwin(24, width - 4, 1, 2)
    border_win.attron(curses.color_pair(2))  # Couleur bleue
    border_win.box()
    border_win.addstr(0, 2, "BTC MULTIPLY history:")
    for index, entry in enumerate(history[-max_entries:], start=1):
        border_win.addstr(index, 2, f"{index}. {entry}", curses.color_pair(1))  # Rouge
    border_win.attroff(curses.color_pair(2))  # Couleur bleue

    stdscr.refresh()

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)  # Définit la couleur rouge
    curses.init_pair(2, curses.COLOR_BLUE, -1)  # Définit la couleur bleue

    stdscr.clear()
    stdscr.border()
    draw_logo(stdscr)
    stdscr.addstr(10, 2, "TanoraTech", curses.color_pair(1))  # Rouge
    stdscr.addstr(14, 2, "Welcome to my application!", curses.color_pair(1))  # Rouge
    stdscr.refresh()

    stdscr.addstr(16, 2, "Enter your email: ", curses.color_pair(1))  # Rouge
    email = ""
    at_entered = False
    dot_entered = False
    while True:
        draw_datetime(stdscr)
        stdscr.addstr(16, 22, email, curses.color_pair(1))  # Rouge
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        elif key == curses.KEY_BACKSPACE:
            if email.endswith(".com"):
                email = email[:-4]
                dot_entered = False
            elif email.endswith("@"):
                at_entered = False
                email = email[:-1]
            else:
                email = email[:-1]
        elif chr(key) in string.ascii_letters or chr(key) in string.digits:
            email += chr(key)
        elif chr(key) == "@":
            if not at_entered:
                email += chr(key)
                at_entered = True
        elif chr(key) == ".":
            if at_entered and not dot_entered:
                email += chr(key)
                dot_entered = True

    stdscr.addstr(17, 2, "Enter your password: ", curses.color_pair(1))  # Rouge
    password = ""
    while True:
        draw_datetime(stdscr)
        stdscr.addstr(17, 25, "*" * len(password), curses.color_pair(1))  # Rouge
        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        elif key == curses.KEY_BACKSPACE:
            password = password[:-1]
        elif chr(key) in string.ascii_letters or chr(key) in string.digits or chr(key) in string.punctuation:
            password += chr(key)

    user_balance = 0.12345678
    time.sleep(1)

    stdscr.clear()
    stdscr.border()
    draw_logo(stdscr)
    display_user_info(stdscr, email, password, user_balance, "Bot is running")
    stdscr.refresh()
    time.sleep(4)

    history = []
    status = "Bot is running"
    show_winning = False

    while True:
        draw_datetime(stdscr)
        if status == "Bot is running":
            display_user_info(stdscr, email, password, user_balance, status)
            stdscr.refresh()
            time.sleep(4)  # Attendre 4 secondes

            user_balance += 0.00000092  # Créditer le solde
            entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: You won 0.00000092 BTC!"
            history.append(entry)
            display_history(stdscr, history)
            show_winning = True
            status = "Bot is running"

        if show_winning:
            status = "You won 0.00000092 BTC"
            stdscr.addstr(22, 2, status, curses.color_pair(1))
            stdscr.refresh()
            time.sleep(2)
            status = "Bot is running"
            stdscr.addstr(22, 2, status + " "*len("You won 0.00000092 BTC"), curses.color_pair(1))
            stdscr.refresh()
            time.sleep(4)
            show_winning = False

        display_user_info(stdscr, email, password, user_balance, status)
        stdscr.refresh()
        time.sleep(4)  # Attendre 4 secondes

        key = stdscr.getch()
        if key == ord('q'):
            break

curses.wrapper(main)
