import sys
import colorama
import re
colorama.init(autoreset=True)



def panic(message,code=1):
    highlight_needies = ["not found","expected","found", r"Holy f\*\*\*\*ng Cow"]
    pattern = re.compile(f"({'|'.join(highlight_needies)})", re.IGNORECASE)
    message = pattern.sub(f"{colorama.Fore.RED}\\1{colorama.Fore.RESET}", message)
    sad_emoticon = "(´•︵•`)"
    indentation = " "* 5
    sys.stderr.write(
        f"\n{indentation}{sad_emoticon}\n\n[{colorama.Fore.RED} Fatal {colorama.Fore.RESET}]"
        f" {message}\n[    Exited with code {code} :-<    ]\n"
    )
    sys.exit(code)
def fmt_c(msg,color="white"):
    color_map = {
        "green":colorama.Fore.GREEN,
        "red":colorama.Fore.RED,
        "blue":colorama.Fore.BLUE,
        "yellow":colorama.Fore.YELLOW,
        "magenta":colorama.Fore.MAGENTA,
        "cyan":colorama.Fore.CYAN,
        "white":colorama.Fore.WHITE
    }
    return f"{color_map.get(color.lower(),color_map["white"])}{msg}{color_map["white"]}"
    