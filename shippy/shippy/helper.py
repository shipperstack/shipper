from rich import print


def input_yn(question, default=True):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default:
        prompt = " [Y/n] "
    else:
        prompt = " [y/N] "

    while True:
        print(question + prompt, end="")
        choice = input().lower()
        if default is not None and choice == "":
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def print_error(msg, newline, exit_after):
    print(f"[red]\u274c ERROR: {msg}", end="\n" if newline else "")

    if exit_after:
        exit(1)


def print_warning(msg, newline=True):
    print(f"[yellow]\u26a0 Warning: {msg}", end="\n" if newline else "")


def print_success(msg, newline=True):
    print(f"[green]\u2713 {msg}", end="\n" if newline else "")
