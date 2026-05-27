# terminal-palette

macOS Terminal.app + Claude Code 配色方案管理工具，可作为 Claude Code skill 使用。

说感觉就能换主题——"米白色""深色护眼""暖色调"——自动匹配并一键切换终端和 Claude Code 的配色。

## 安装（作为 Claude Code Skill）

```bash
git clone https://github.com/cadejay97-dotcom/terminal-palette ~/.claude/skills/terminal-palette
```

安装后在 Claude Code 中直接说：
> "帮我换个米白色的主题"
> "来个深色护眼的配色"
> "让我选一个"

## 命令行直接使用

```bash
# 列出所有配色（带真实 ANSI 色块预览）
python3 apply.py list

# 交互式选色器
python3 apply.py pick

# 切换到指定配色
python3 apply.py apply warm-beige
python3 apply.py apply nord
python3 apply.py apply dracula

# 其他
python3 apply.py current      # 当前配色详情
python3 apply.py random       # 随机切换
python3 apply.py list --plain # 纯文本列表（无颜色代码）
```

## 配色一览

| # | 名称 | 氛围 | 背景色 | 描述 |
|---|------|------|--------|------|
| 1 | **warm-beige** | 暖·亮 | #FDF6E3 | 暖米黄底 + 深暖灰字 + 琥珀光标 |
| 2 | **dracula** | 冷·暗 | #282336 | 深紫底 + 荧光绿/粉/青/黄 |
| 3 | **nord** | 冷·暗 | #2E3440 | 蓝灰低对比，护眼长读 |
| 4 | **solarized-light** | 暖·亮 | #FDF6E3 | 米黄底 + 蓝灰字，科学配比 |
| 5 | **solarized-dark** | 冷·暗 | #2A363B | 深蓝灰底 + 米黄字 |
| 6 | **gruvbox-dark** | 暖·暗 | #1D1A15 | 暖黑底 + 复古绿/橙 |
| 7 | **gruvbox-light** | 暖·亮 | #F9E9CC | 米白底 + 暖棕字 |
| 8 | **catppuccin-mocha** | 冷·暗 | #1E1C23 | 紫调深底，时尚柔和 |
| 9 | **catppuccin-latte** | 暖·亮 | #F4EFEB | 粉调浅底，温柔明亮 |
| 10 | **monokai** | 冷·暗 | #2A2A2A | 经典高对比，鲜艳醒目 |

## 感觉关键词

| 想要 | 推荐 |
|------|------|
| 米白/米黄/暖白 | warm-beige, solarized-light, gruvbox-light |
| 深色/护眼 | nord, solarized-dark |
| 暖色调 | warm-beige, gruvbox-light, gruvbox-dark |
| 冷色调 | nord, catppuccin-mocha, dracula |
| 鲜艳/高对比 | dracula, monokai |
| 复古 | gruvbox-light, gruvbox-dark |
| 时尚/现代 | catppuccin-latte, catppuccin-mocha |

## 原理

- `plistlib` 直接写入 `~/Library/Preferences/com.apple.Terminal.plist`（NSKeyedArchiver 格式）
- 同步修改 `~/.claude/settings.json` 的 `theme` 字段切换 Claude Code 主题
- AppleScript 推送至所有已打开的终端窗口（即时生效）
- 需要 macOS + Terminal.app + Python 3（系统自带）

## 贡献新主题

在 `themes.json` 中添加一项：

```json
"theme-key": {
  "name": "Display Name",
  "type": "light|dark",
  "cc_theme": "light|dark",
  "description": "一句话描述",
  "colors": {
    "background": [r, g, b],
    "foreground": [r, g, b],
    "cursor":     [r, g, b],
    "selection":  [r, g, b],
    "bold":       [r, g, b]
  },
  "ansi": {
    "black": [r, g, b], "red": [r, g, b], "green": [r, g, b],
    "yellow": [r, g, b], "blue": [r, g, b], "magenta": [r, g, b],
    "cyan": [r, g, b], "white": [r, g, b],
    "bright_black": [r, g, b], "bright_red": [r, g, b], ...
  }
}
```

RGB 值为 0.0–1.0 浮点数。
