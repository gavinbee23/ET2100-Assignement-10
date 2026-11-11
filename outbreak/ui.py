from colorama import Fore, Style, just_fix_windows_console


def title(text):
    print(Fore.CYAN + text + Style.RESET_ALL)


def warning(text):
    print(Fore.YELLOW + text + Style.RESET_ALL)


def menu(prompt, choices):
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices:
            return answer
        warning("Choose " + ", ".join(choices) + ".")


def intro():
    just_fix_windows_console()
    title(r"""
   =====================================
           D E A D   C I T Y
              O U T B R E A K
   =====================================
""")
    print("Bellwether, 02:13. Rain has flooded the lower streets.")
    print("You follow a distress signal into the Ninth Ward station.")
    print("The radio repeats a message recorded in your own neighborhood:")
    print('"If the sirens go quiet, get above the water."\n')
