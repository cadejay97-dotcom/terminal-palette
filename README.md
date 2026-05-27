# terminal-palette

macOS Terminal.app + Claude Code 配色方案管理工具。

说感觉就能换主题——"米白色""深色护眼""暖色调"，自动匹配推荐并一键切换 Terminal.app profile 和 Claude Code 主题。

## 快速开始

```bash
# 安装到 Claude Code
ln -sf "$PWD" ~/.claude/skills/terminal-palette

# 手动切换配色
python3 apply.py list          # 列出所有配色
python3 apply.py current       # 当前配色详情
python3 apply.py warm-beige    # 切换到指定配色
python3 apply.py random        # 随机切换
```

在 Claude Code 中直接说感觉即可自动匹配。

## 配色

| 名称 | 氛围 | 背景 |
|------|------|------|
| warm-beige | 暖 · 亮 | 米黄 #FDF6E3 |
| solarized-light | 暖 · 亮 | 米黄 #FDF6E3 |
| gruvbox-light | 暖 · 亮 | 米白 #F9E9CC |
| catppuccin-latte | 暖 · 亮 | 粉白 #F4EFEB |
| solarized-dark | 冷 · 暗 | 蓝灰 #2A363B |
| nord | 冷 · 暗 | 蓝灰 #2E3440 |
| gruvbox-dark | 暖 · 暗 | 暖黑 #1D1A15 |
| catppuccin-mocha | 冷 · 暗 | 紫灰 #1E1C23 |
| dracula | 冷 · 暗 | 深紫 #282336 |
| monokai | 冷 · 暗 | 深灰 #2A2A2A |

## 原理

- 通过 Python `plistlib` 直接写入 `com.apple.Terminal.plist` 的 NSKeyedArchiver 格式颜色数据
- 同时修改 `~/.claude/settings.json` 的 `theme` 字段同步 Claude Code 主题
- AppleScript 推送至所有已打开终端窗口
