---
name: terminal-palette
version: 2.0.0
description: "终端配色方案管理。说感觉就能换主题——'米白色' '深色护眼' '暖色调'，自动匹配推荐。同时切换 Terminal.app profile 和 Claude Code 主题色。触发词：配色、主题、换颜色、palette、theme、terminal colors"
---

# terminal-palette

管理终端配色。**说感觉就行**，不用记名字。

## 用法示例

- "换个米白色的主题" → 匹配 warm-beige / gruvbox-light / solarized-light
- "来个深色护眼的" → 推荐 nord / solarized-dark
- "想要暖色调的" → 推荐 gruvbox-dark / catppuccin-latte
- "换个鲜艳点的" → 推荐 dracula / monokai
- "让我选" → 展示交互选色器

## 交互流程

**只要用户提到换主题/配色，立即展示下面的主题表**（不需要运行任何命令，直接从这里读）：

| # | 名称 | 氛围 | 背景色 | 描述 |
|---|------|------|--------|------|
| 1 | warm-beige | 暖·亮 | #FDF6E3 | 暖米黄底 + 深暖灰字 + 琥珀光标 |
| 2 | dracula | 冷·暗 | #282336 | 深紫底 + 荧光绿/粉/青/黄 |
| 3 | nord | 冷·暗 | #2E3440 | 蓝灰低对比，护眼长读 |
| 4 | solarized-light | 暖·亮 | #FDF6E3 | 米黄底 + 蓝灰字，科学配比 |
| 5 | solarized-dark | 冷·暗 | #2A363B | 深蓝灰底 + 米黄字 |
| 6 | gruvbox-dark | 暖·暗 | #1D1A15 | 暖黑底 + 复古绿/橙 |
| 7 | gruvbox-light | 暖·亮 | #F9E9CC | 米白底 + 暖棕字 |
| 8 | catppuccin-mocha | 冷·暗 | #1E1C23 | 紫调深底，时尚柔和 |
| 9 | catppuccin-latte | 暖·亮 | #F4EFEB | 粉调浅底，温柔明亮 |
| 10 | monokai | 冷·暗 | #2A2A2A | 经典高对比，鲜艳醒目 |

等用户说编号或名称（如 "3"、"nord"、"第5个"），再运行：
```
python3 apply.py apply <name>
```

如果用户直接说了名字（如"换 nord"），跳过展示直接执行。

## 命令

```
python3 apply.py list              # 列出所有（带 ANSI 色块预览）
python3 apply.py current           # 当前配色详情
python3 apply.py apply <name>      # 切换到指定配色
python3 apply.py random            # 随机切换
python3 apply.py pick              # 交互式选色器（终端直接用）
python3 apply.py list --plain      # 纯文本列表（无颜色）
```

## 语义匹配

**米白/米黄/暖白**：warm-beige, solarized-light, gruvbox-light
**深色/暗色**：dracula, nord, solarized-dark, gruvbox-dark, catppuccin-mocha, monokai
**暖色调**：warm-beige, gruvbox-light, gruvbox-dark, catppuccin-latte
**冷色调/护眼**：nord, solarized-dark, catppuccin-mocha
**鲜艳/高对比**：dracula, monokai
**复古**：gruvbox-light, gruvbox-dark
**时尚/现代**：catppuccin-latte, catppuccin-mocha

## 配色一览

| # | 名称 | 氛围 | 背景色 | 描述 |
|---|------|------|--------|------|
| 1 | warm-beige | 暖·亮 | #FDF6E3 | 暖米黄底 + 深暖灰字 + 琥珀光标 |
| 2 | dracula | 冷·暗 | #282336 | 深紫底 + 荧光绿/粉/青/黄 |
| 3 | nord | 冷·暗 | #2E3440 | 蓝灰低对比，护眼长读 |
| 4 | solarized-light | 暖·亮 | #FDF6E3 | 米黄底 + 蓝灰字，科学配比 |
| 5 | solarized-dark | 冷·暗 | #2A363B | 深蓝灰底 + 米黄字 |
| 6 | gruvbox-dark | 暖·暗 | #1D1A15 | 暖黑底 + 复古绿/橙 |
| 7 | gruvbox-light | 暖·亮 | #F9E9CC | 米白底 + 暖棕字 |
| 8 | catppuccin-mocha | 冷·暗 | #1E1C23 | 紫调深底，时尚柔和 |
| 9 | catppuccin-latte | 暖·亮 | #F4EFEB | 粉调浅底，温柔明亮 |
| 10 | monokai | 冷·暗 | #2A2A2A | 经典高对比，鲜艳醒目 |
