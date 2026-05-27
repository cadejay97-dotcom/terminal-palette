#!/usr/bin/env python3
"""Apply a terminal color theme to Terminal.app + Claude Code."""
import json, plistlib, subprocess, sys, os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
THEMES_FILE = os.path.join(SKILL_DIR, "themes.json")
TERMINAL_PLIST = os.path.expanduser("~/Library/Preferences/com.apple.Terminal.plist")
CC_SETTINGS = os.path.expanduser("~/.claude/settings.json")


def make_nscolor(rgb):
    """Create NSKeyedArchiver plist data for an RGB color."""
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


def apply_terminal_theme(theme):
    """Write theme colors into Terminal.app plist."""
    with open(TERMINAL_PLIST, "rb") as f:
        plist = plistlib.load(f)

    ws = plist.setdefault("Window Settings", {})
    name = theme["name"]
    profile = ws.get(name, {})

    # Set basic colors
    for key, plist_key in COLOR_MAP.items():
        if key in theme.get("colors", {}):
            profile[plist_key] = make_nscolor(theme["colors"][key])

    # Set ANSI colors
    for key, plist_key in ANSI_MAP.items():
        if key in theme.get("ansi", {}):
            profile[plist_key] = make_nscolor(theme["ansi"][key])

    # Set metadata
    profile["name"] = name
    profile["type"] = "Window Settings"
    profile["ProfileCurrentVersion"] = 2.07
    profile.setdefault("FontAntialias", True)

    ws[name] = profile
    plist["Default Window Settings"] = name

    with open(TERMINAL_PLIST, "wb") as f:
        plistlib.dump(plist, f)

    return name


def apply_cc_theme(cc_theme):
    """Set Claude Code theme in settings.json."""
    with open(CC_SETTINGS, "r") as f:
        text = f.read()
    settings = json.loads(text)

    old = settings.get("theme", "")
    settings["theme"] = cc_theme

    with open(CC_SETTINGS, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return old


def apply_to_all_windows(profile_name):
    """Switch all Terminal windows to the profile."""
    script = f'''
tell application "Terminal"
    set targetProfile to settings set "{profile_name}"
    repeat with i from 1 to count of windows
        try
            set current settings of window i to targetProfile
        end try
    end repeat
end tell
'''
    subprocess.run(["osascript", "-e", script], capture_output=True)


def list_themes():
    themes = load_themes()
    current = get_current_theme_name()
    lines = []
    for name, data in themes.items():
        marker = " *" if data["name"] == current else "  "
        t = data.get("type", "?")
        lines.append(f"  {marker} {name:25s} {t:6s}  {data['description']}")
    return "\n".join(lines)


def get_current_theme_name():
    try:
        with open(TERMINAL_PLIST, "rb") as f:
            plist = plistlib.load(f)
        return plist.get("Default Window Settings", "?")
    except:
        return "?"


def get_current_cc_theme():
    try:
        with open(CC_SETTINGS) as f:
            return json.load(f).get("theme", "?")
    except:
        return "?"


def get_current():
    """Show current theme info."""
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
    lines = [
        f"当前配色: {theme_data['name']} ({theme_key})",
        f"CC 主题:   {cc_theme}",
        f"类型:      {theme_data.get('type', '?')}",
        f"描述:      {theme_data.get('description', '')}",
    ]
    if bg:
        hex_bg = "#{:02x}{:02x}{:02x}".format(
            int(bg[0] * 255), int(bg[1] * 255), int(bg[2] * 255)
        )
        lines.append(f"背景色:    {hex_bg}")
    if fg:
        hex_fg = "#{:02x}{:02x}{:02x}".format(
            int(fg[0] * 255), int(fg[1] * 255), int(fg[2] * 255)
        )
        lines.append(f"文字色:    {hex_fg}")
    return "\n".join(lines)


def apply(theme_key):
    themes = load_themes()
    if theme_key not in themes:
        available = ", ".join(themes.keys())
        return f"未知配色: {theme_key}\n可用: {available}"

    theme = themes[theme_key]
    name = apply_terminal_theme(theme)
    old_cc = apply_cc_theme(theme["cc_theme"])
    apply_to_all_windows(name)

    return (
        f"✅ 已切换到: {name}\n"
        f"  Terminal  profile → {name}\n"
        f"  CC 主题          → {theme['cc_theme']} (原: {old_cc})\n"
        f"  已应用到所有窗口"
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["list", "apply", "current", "random"])
    parser.add_argument("name", nargs="?", default=None)
    args = parser.parse_args()

    if args.action == "list":
        print(list_themes())
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
        print(apply(choice))
