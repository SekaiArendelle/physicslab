# physicslab

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/SekaiArendelle/physicslab/blob/main/LICENSE)
![support-version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)

## 介绍

`physicslab` 是 [物理实验室 AR](https://www.turtlesim.com/) 的 Python API，支持通过代码创建实验、读写 `.plsav` 存档文件、以及与物实社区进行网络交互。

## 安装

```shell
pip install physicslab
```

## 快速开始

```python
from physicslab import (
    crt_circuit_experiment,
    LogicOutput,
    Position,
    generate_a_new_sav_path,
)

with crt_circuit_experiment("example") as expe:
    expe.crt_a_element(LogicOutput(Position(0, 0, 0.1)))

    destination = generate_a_new_sav_path()
    if not destination.parent.exists():
        destination.parent.mkdir(parents=True)
    expe.save_to(destination)
```

更多用法请查看 [快速开始](quick_start.md)。

## 功能支持

- 跨平台支持：Windows 7+、Linux、macOS、Android
- 支持物实所有实验类型：电学、天体物理、电与磁
- 支持物实全部元件
- 大多数物实网络 API 封装

## 链接

- [GitHub](https://github.com/SekaiArendelle/physicslab)
- [Gitee 镜像](https://gitee.com/script2000/physicslab)
