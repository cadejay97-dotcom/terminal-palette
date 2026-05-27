---
name: terminal-palette
version: 1.1.0
description: "终端配色方案管理。说感觉就能换主题——'米白色' '深色护眼' '暖色调'，自动匹配推荐。切换 Terminal.app + Claude Code 主题色。触发词：配色、主题、换颜色、palette、theme"
---

# terminal-palette

管理终端配色。**说感觉就行**，不用记名字。比如：
- "换个米白色的主题" → 匹配 warm-beige / gruvbox-light / solarized-light
- "来个深色护眼的" → 推荐 nord / solarized-dark
- "想要暖色调的" → 推荐 gruvbox-dark / catppuccin-latte
- "换个鲜艳点的" → 推荐 dracula / monokai

## 命令

```
list              列出所有配色
current           当前配色详情
apply <name>      指定切换
random            随机换一个
```

## 配色一览

| 名称 | 氛围 | 背景 | 适合场景 |
|------|------|------|----------|
| **warm-beige** | 暖 · 亮 | 米黄 `#FDF6E3` | 日间/舒适/米白系 |
| **solarized-light** | 暖 · 亮 | 米黄 `#FDF6E3` | 日间/科学配比 |
| **gruvbox-light** | 暖 · 亮 | 米白 `#F9E9CC` | 日间/复古暖调 |
| **catppuccin-latte** | 暖 · 亮 | 粉白 `#F4EFEB` | 日间/温柔明亮 |
| **solarized-dark** | 冷 · 暗 | 蓝灰 `#2A363B` | 夜间/护眼 |
| **nord** | 冷 · 暗 | 蓝灰 `#2E3440` | 夜间/低对比长读 |
| **gruvbox-dark** | 暖 · 暗 | 暖黑 `#1D1A15` | 夜间/复古温暖 |
| **catppuccin-mocha** | 冷 · 暗 | 紫灰 `#1E1C23` | 夜间/时尚柔和 |
| **dracula** | 冷 · 暗 | 深紫 `#282336` | 夜间/鲜艳经典 |
| **monokai** | 冷 · 暗 | 深灰 `#2A2A2A` | 夜间/高对比醒目 |

## 语义标签（帮你理解如何匹配）

**浅色/亮色系**：warm-beige, solarized-light, gruvbox-light, catppuccin-latte
**深色/暗色系**：dracula, nord, solarized-dark, gruvbox-dark, catppuccin-mocha, monokai
**暖色调**：warm-beige, gruvbox-light, gruvbox-dark, solarized-light, catppuccin-latte
**冷色调**：nord, dracula, solarized-dark, catppuccin-mocha, monokai
**米白/米黄/暖白**：warm-beige, solarized-light, gruvbox-light
**低对比/护眼**：nord, solarized-dark
**鲜艳/高对比**：dracula, monokai
**复古**：gruvbox-light, gruvbox-dark
**时尚/现代**：catppuccin-latte, catppuccin-mocha

执行脚本：`python3 terminal-palette/apply.py <action> [name]`

## Install

```bash
# 从项目目录创建 symlink 到 Claude Code 技能目录
ln -sf "$PWD" ~/.claude/skills/terminal-palette
```
