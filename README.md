# Arduino RGB Plant Lamp

[中文](#中文) · [English](#english)

A small, reproducible RGB plant-lamp controller: send readable serial commands,
drive three PWM channels, and preview the behavior with a zero-dependency offline
simulator before connecting hardware.

![Serial commands flow through Arduino firmware and an external driver to an RGB lamp](docs/architecture.svg)

> This public-safe example contains no cloud account, Wi-Fi credential, private
> device protocol, vendor SDK, or copied third-party repository.

## 中文

### 它解决什么问题

很多灯控样例绑定某个 App、云平台或厂商协议，离开指定设备就难以复现。本项目用简单文本命令控制 RGB 三路 PWM，并提供离线仿真和功耗估算，让普通开发者没有硬件也能先理解协议和状态变化。

### 功能

- 串口或透明蓝牙 UART：`R0..255`、`G0..255`、`B0..255`
- 一行多通道控制：`R180,G80,B20`
- `OFF` 一键关闭，`STATUS` 查询当前 PWM 状态
- 输入长度限制、数值钳位、错误 token 忽略
- 零第三方依赖的离线 Demo
- 根据可编辑示例参数估算理论输入功率

### 30 秒离线 Demo

不需要 Arduino、蓝牙模块或云服务：

```bash
python demo/lamp_simulator.py "R180,G80,B20" STATUS OFF
```

示例输出：

```text
> R180,G80,B20
  R=180 G= 80 B= 20 estimated=0.110 W
> STATUS
  R=180 G= 80 B= 20 estimated=0.110 W
> OFF
  R=  0 G=  0 B=  0 estimated=0.000 W
```

估算值来自 [`config/hardware.example.json`](config/hardware.example.json)，不是实测值，也不能证明节能效果。

### 硬件清单

- Arduino Uno 或兼容板
- 共阳/共阴 RGB LED，或低压 RGB 灯带
- 与负载电流匹配的限流电阻或 MOSFET/恒流驱动级
- 稳压低压电源
- 可选：透明串口模式蓝牙模块

高功率灯具不能由 Arduino 引脚直接供电。详细连接见 [`docs/wiring.md`](docs/wiring.md)，电气边界见 [`docs/safety.md`](docs/safety.md)。

### 接线摘要

| 通道 | Arduino Uno 示例引脚 |
|---|---:|
| Red PWM | D11 |
| Green PWM | D10 |
| Blue PWM | D9 |
| Bluetooth TX | Arduino RX |
| Bluetooth RX | Arduino TX（按模块电平要求转换） |

### 固件快速开始

1. 在 Arduino IDE 中打开 [`src/rgb_plant_lamp.ino`](src/rgb_plant_lamp.ino)。
2. 选择实际板卡和串口后上传。
3. 打开 `9600` 波特率串口监视器，行尾选择换行。
4. 发送 [`examples/commands.txt`](examples/commands.txt) 中的命令。

蓝牙模块若处于透明串口模式，手机端发送相同文本即可。完整协议见 [`docs/protocol.md`](docs/protocol.md)。

### 功耗估算逻辑

离线 Demo 使用以下简化关系：

```text
estimated_power = supply_voltage × Σ(channel_max_current × pwm / 255)
```

它只用于比较命令对应的理论占空比和输入功率。真实 LED 驱动效率、恒流方式、温升和电源损耗必须通过硬件测量确认。

### 已验证与未验证

**[已确认] 本仓库验证：** Python 离线 Demo、协议语义、边界值、错误输入、文档结构和敏感信息规则可由自动化测试检查。

**[待确认] 硬件验证：** 当前没有在本轮环境中完成具体 Arduino 板卡编译、实物接线、功率计测量、温升、EMC、防水或植物生长效果测试。

### 项目结构

```text
.
├── README.md
├── CHANGELOG.md
├── config/hardware.example.json
├── demo/lamp_simulator.py
├── docs/
│   ├── architecture.md
│   ├── architecture.svg
│   ├── protocol.md
│   ├── safety.md
│   └── wiring.md
├── examples/commands.txt
├── src/rgb_plant_lamp.ino
├── tests/test_protocol.py
└── .github/workflows/quality.yml
```

### 公开边界

这是从个人实验记录重新整理的通用、可公开示例，不复制原始厂商资料包、团队申报材料、第三方完整仓库、真实联网凭据或私有设备协议，也不声明对原始团队项目的全部贡献。

## English

This repository demonstrates a generic serial/Bluetooth-UART RGB lamp controller
with a small Arduino sketch, an offline simulator, configurable theoretical power
estimation, documentation, and tests. Start with:

```bash
python demo/lamp_simulator.py "R180,G80,B20" STATUS OFF
```

See [architecture](docs/architecture.md), [wiring](docs/wiring.md),
[protocol](docs/protocol.md), and [safety](docs/safety.md). Hardware behavior and
energy savings are not claimed until measured on a specific build.

## Contributing, security, and license

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the
[MIT License](LICENSE). Changes are tracked in [CHANGELOG.md](CHANGELOG.md).
