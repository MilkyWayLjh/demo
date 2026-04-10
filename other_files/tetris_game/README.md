# 俄罗斯方块（Python / Pygame）

## 运行

1. 安装依赖：

```bash
python -m pip install -r requirements.txt
```

2. 启动游戏：

```bash
python main.py
```

## 操作

- **左右移动**：← / →
- **软降**：↓
- **硬降**：Space
- **旋转**：↑（顺时针） / Z（逆时针）
- **暂停/继续**：P
- **重新开始**：R
- **退出**：Esc

## 打包成单文件 exe（Windows）

在 `tetris_game/` 目录执行：

```powershell
python -m pip install -r requirements.txt
.\build_exe.ps1
```

产物默认在 `dist\Tetris.exe`，双击即可单独运行（无需 Python 环境）。
