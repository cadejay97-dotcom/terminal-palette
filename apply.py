#!/usr/bin/env python3
"""Apply a terminal color theme to Terminal.app + Claude Code."""
import json, plistlib, subprocess, sys, os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_FILE = os.path.join(SKILL_DIR, "themes.json")
TERMINAL_PLIST = os.path.expanduser("~/Library/Preferences/com.apple.Terminal.plist")
CC_SETTINGS = os.path.expanduser("~/.claude/settings.json")


def make_nscolor(rgb):
    nsrgb = f"{rgb[0]:.10f} {rgb[1]:.10f} {rgb[2]:.10f}\0".encode()
    obj = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": {"UID": 1}},
        "$objects": [
            "$null",
            {"NSRGB": nsrgb, "NSColorSpace": 1, "$class": {"UID": 2}},
            {"$classes": ["NSColor", "NSObject"], "$classname": "NSColor"},
        ],
    }
    return plistlib.dumps(obj)


COLOR_MAP = {
    "background": "BackgroundColor",
    "foreground": "TextColor",
    "bold": "TextBoldColor",
    "cursor": "CursorColor",
    "selection": "SelectionColor",
}

ANSI_MAP = {
    "black": "ANSIBlackColor",
    "red": "ANSIRedColor",
    "green": "ANSIGreenColor",
    "yellow": "ANSIYellowColor",
    "blue": "ANSIBlueColor",
    "magenta": "ANSIMagentaColor",
    "cyan": "ANSICyanColor",
    "white": "ANSIWhiteColor",
    "bright_black": "ANSIBrightBlackColor",
    "bright_red": "ANSIBrightRedColor",
    "bright_green": "ANSIBrightGreenColor",
    "bright_yellow": "ANSIBrightYellowColor",
    "bright_blue": "ANSIBrightBlueColor",
    "bright_magenta": "ANSIBrightMagentaColor",
    "bright_cyan": "ANSIBrightCyanColor",
    "bright_white": "ANSIBrightWhiteColor",
}


def load_themes():
    with open(THEMES_FILE) as f:
        return json.load(f)


# ── ANSI helpers ─────────────────────────────────────────────────────────────

def _bg(rgb):
    r, g, b = int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    return f"\033[48;2;{r};{g};{b}m"

def _fg(rgb):
    r, g, b = int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    return f"\033[38;2;{r};{g};{b}m"

RESET = "\033[0m"

def swatch(theme_data):
    """Return a colored ANSI swatch string showing bg + accent colors."""
    colors = theme_data.get("colors", {})
    ansi = theme_data.get("ansi", {})
    bg = colors.get("background")
    fg = colors.get("foreground")
    accents = [ansi.get(k) for k in ("red", "green", "yellow", "blue", "magenta", "cyan") if ansi.get(k)]

    parts = []
    if bg:
        parts.append(f"{_bg(bg)}  {RESET}")
    if fg and bg:
        parts.append(f"{_bg(bg)}{_fg(fg)} A {RESET}")
    for acc in accents[:4]:
        if bg:
            parts.append(f"{_bg(bg)}{_fg(acc)}▮{RESET}")
        else:
            parts.append(f"{_fg(acc)}▮{RESET}")
    return "".join(parts)


def hex_color(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))


# ── Core operations ──────────────────────────────────────────────────────────

def _as_rgb(rgb):
    """Convert 0-1 float RGB to AppleScript 0-65535 integer list."""
    return "{%d, %d, %d}" % (int(rgb[0]*65535), int(rgb[1]*65535), int(rgb[2]*65535))


def _terminal_running():
    r = subprocess.run(["pgrep", "-x", "Terminal"], capture_output=True)
    return r.returncode == 0


def apply_terminal_theme(theme):
    """Apply theme via AppleScript (live, no restart needed) + persist to plist."""
    name = theme["name"]
    colors = theme.get("colors", {})

    color_props = {
        "background color": colors.get("background"),
        "normal text color": colors.get("foreground"),
        "bold text color": colors.get("bold") or colors.get("foreground"),
        "cursor color": colors.get("cursor"),
        "selection color": colors.get("selection"),
    }
    set_lines = []
    for prop, rgb in color_props.items():
        if rgb:
            set_lines.append(
                f'            set {prop} of current settings of w to {_as_rgb(rgb)}'
            )
    set_block = "\n".join(set_lines)

    as_ok = False
    win_count = 0
    if _terminal_running():
        count_script = 'tell application "Terminal" to count windows'
        cr = subprocess.run(["osascript", "-e", count_script], capture_output=True, text=True)
        if cr.returncode == 0:
            try:
                win_count = int(cr.stdout.strip())
            except ValueError:
                win_count = 0

        script = f'''
tell application "Terminal"
    repeat with w in windows
        try
{set_block}
        end try
    end repeat
end tell
'''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        as_ok = result.returncode == 0

    _persist_to_plist(theme)
    return name, as_ok, win_count


def _persist_to_plist(theme):
    """Write theme to Terminal.app plist for persistence across restarts."""
    try:
        with open(TERMINAL_PLIST, "rb") as f:
            plist = plistlib.load(f)
        ws = plist.setdefault("Window Settings", {})
        name = theme["name"]
        profile = ws.get(name, {})
        for key, plist_key in COLOR_MAP.items():
            if key in theme.get("colors", {}):
                profile[plist_key] = make_nscolor(theme["colors"][key])
        for key, plist_key in ANSI_MAP.items():
            if key in theme.get("ansi", {}):
                profile[plist_key] = make_nscolor(theme["ansi"][key])
        profile["name"] = name
        profile["type"] = "Window Settings"
        profile["ProfileCurrentVersion"] = 2.07
        profile.setdefault("FontAntialias", True)
        ws[name] = profile
        plist["Default Window Settings"] = name
        with open(TERMINAL_PLIST, "wb") as f:
            plistlib.dump(plist, f)
    except Exception:
        pass


def apply_cc_theme(cc_theme):
    if not os.path.exists(CC_SETTINGS):
        return None
    with open(CC_SETTINGS, "r") as f:
        settings = json.load(f)
    old = settings.get("theme", "")
    settings["theme"] = cc_theme
    with open(CC_SETTINGS, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return old


def apply_to_all_windows(profile_name):
    pass  # now handled inside apply_terminal_theme via AppleScript


def get_current_theme_name():
    try:
        with open(TERMINAL_PLIST, "rb") as f:
            plist = plistlib.load(f)
        return plist.get("Default Window Settings", "?")
    except Exception:
        return "?"


def get_current_cc_theme():
    try:
        with open(CC_SETTINGS) as f:
            return json.load(f).get("theme", "?")
    except Exception:
        return "?"


# ── Output formatters ────────────────────────────────────────────────────────

def list_themes(plain=False):
    """List all themes with ANSI color swatches (or plain text)."""
    if not plain and not sys.stdout.isatty():
        plain = True  # captured by subprocess (e.g. Claude Code) → no ANSI
    themes = load_themes()
    current = get_current_theme_name()
    lines = [""]
    for i, (key, data) in enumerate(themes.items(), 1):
        is_current = data["name"] == current
        marker = "▶" if is_current else " "
        bg_hex = hex_color(data["colors"]["background"]) if data.get("colors", {}).get("background") else ""
        label = f"{i:2}. {marker} {key:<22}"
        tag = f"{data.get('type','?'):<6}  {data.get('description','')}"
        if plain:
            lines.append(f"  {label}  {tag}")
        else:
            sw = swatch(data)
            lines.append(f"  {label} {sw}  {bg_hex}  {tag}")
    lines.append("")
    return "\n".join(lines)


def get_current():
    term_name = get_current_theme_name()
    cc_theme = get_current_cc_theme()

    themes = load_themes()
    theme_data = None
    theme_key = None
    for k, v in themes.items():
        if v["name"] == term_name:
            theme_data = v
            theme_key = k
            break

    if not theme_data:
        return f"Terminal: {term_name} (custom)\nCC: {cc_theme}"

    c = theme_data.get("colors", {})
    bg = c.get("background", [])
    fg = c.get("foreground", [])
    sw = swatch(theme_data)
    lines = [
        f"当前配色: {theme_data['name']} ({theme_key})  {sw}",
        f"CC 主题:  {cc_theme}",
        f"类型:     {theme_data.get('type', '?')}",
        f"描述:     {theme_data.get('description', '')}",
    ]
    if bg:
        lines.append(f"背景色:   {hex_color(bg)}")
    if fg:
        lines.append(f"文字色:   {hex_color(fg)}")
    return "\n".join(lines)


def apply(theme_key):
    themes = load_themes()
    if theme_key not in themes:
        # fuzzy match
        matches = [k for k in themes if theme_key.lower() in k.lower()]
        if len(matches) == 1:
            theme_key = matches[0]
        else:
            return f"未知配色: {theme_key}  可用: {', '.join(themes.keys())}"

    theme = themes[theme_key]
    name, as_ok, win_count = apply_terminal_theme(theme)
    old_cc = apply_cc_theme(theme["cc_theme"])

    sw = swatch(theme) if sys.stdout.isatty() else ""
    if as_ok and win_count > 0:
        term_status = f"已即时应用到 {win_count} 个窗口"
    elif not _terminal_running():
        term_status = "Terminal 未运行，配置已保存，下次打开生效"
    else:
        term_status = "配置已保存"

    cc_line = ""
    if old_cc is None:
        cc_line = "\n   CC 主题          → (settings.json 不存在，已跳过)"
    else:
        cc_line = f"\n   CC 主题          → {theme['cc_theme']}  (原: {old_cc})"

    return (
        f"✅ 已切换到: {name}  {sw}\n"
        f"   Terminal        → {term_status}"
        f"{cc_line}"
    )


def pick():
    """Interactive numbered theme picker (standalone mode)."""
    themes = load_themes()
    keys = list(themes.keys())
    current = get_current_theme_name()

    print(list_themes())
    print("输入编号或主题名 (q 退出): ", end="", flush=True)
    try:
        choice = input().strip()
    except (EOFError, KeyboardInterrupt):
        return

    if choice.lower() in ("q", "quit", ""):
        return

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(keys):
            print(apply(keys[idx]))
        else:
            print(f"编号超出范围 (1-{len(keys)})")
    elif choice in themes:
        print(apply(choice))
    else:
        # fuzzy: check if choice is a substring of any key
        matches = [k for k in keys if choice.lower() in k.lower()]
        if len(matches) == 1:
            print(apply(matches[0]))
        elif len(matches) > 1:
            print(f"模糊匹配到多个: {', '.join(matches)}，请更精确")
        else:
            print(f"未找到: {choice}")


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Terminal + Claude Code theme switcher")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["list", "apply", "current", "random", "pick"],
        default="list",
    )
    parser.add_argument("name", nargs="?", default=None)
    parser.add_argument("--plain", action="store_true", help="No ANSI colors in output")
    args = parser.parse_args()

    if args.action == "list":
        print(list_themes(plain=args.plain))
    elif args.action == "current":
        print(get_current())
    elif args.action == "apply":
        if not args.name:
            print("Usage: apply.py apply <theme_name>")
            sys.exit(1)
        print(apply(args.name))
    elif args.action == "random":
        import random
        themes = load_themes()
        choice = random.choice(list(themes.keys()))
        print(f"随机选择: {choice}")
        print(apply(choice))
    elif args.action == "pick":
        pick()
