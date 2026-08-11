# Arduino RGB Plant Lamp

[English](#english) · [中文](#中文)

一个可复现的 Arduino RGB 植物灯实验：通过串口或透明传输的蓝牙串口模块接收 `R/G/B` 亮度命令，使用 PWM 控制三路 LED。

> 公开版只保留通用控制逻辑和虚构示例，不包含个人隐私、设备账号、密钥、厂商资料包或第三方库源码。

## 中文

### 项目亮点

- 串口与蓝牙透明传输兼容：蓝牙模块只需把数据转发到 Arduino 串口
- `R0` 到 `R255`、`G0` 到 `G255`、`B0` 到 `B255` 控制三路 PWM
- 一行可发送多个命令，例如 `R180,G80,B20`
- 支持换行提交、输入长度限制和越界值钳位
- 不绑定具体蓝牙模块、手机 App 或厂商 SDK

### 硬件连接

| 功能 | Arduino Uno 示例 |
|---|---:|
| 红色 PWM | D11 |
| 绿色 PWM | D10 |
| 蓝色 PWM | D9 |
| 串口/蓝牙 TX | Arduino RX |
| 串口/蓝牙 RX | Arduino TX（按模块电平要求分压） |
| GND | GND |

LED 和电源应根据实际器件增加限流与驱动电路，不要直接让 Arduino 引脚承载超出规格的电流。

### 上传与运行

1. 在 Arduino IDE 中打开 [`src/rgb_plant_lamp.ino`](src/rgb_plant_lamp.ino)。
2. 选择与你的板卡匹配的 Arduino board 和串口。
3. 上传后打开串口监视器，波特率设为 `9600`，行尾选择换行。
4. 发送 [`examples/commands.txt`](examples/commands.txt) 中的命令。

蓝牙模块使用透明串口模式时，手机 App 发送相同文本即可。

### 命令协议

```text
R255\n          # 红色满亮
G80,B20\n     # 同时调整绿色和蓝色
r0,g0,b0\n    # 关闭三路
```

每个 token 由一个通道字母和十进制亮度组成；亮度会被限制在 `0..255`。协议细节见 [`docs/protocol.md`](docs/protocol.md)。

### 项目结构

```text
.
├── src/rgb_plant_lamp.ino
├── examples/commands.txt
├── docs/protocol.md
├── tests/test_protocol.py
├── .github/workflows/quality.yml
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

### 公开边界

这是从个人实验记录整理出的通用示例，不声明对原始团队项目的全部贡献。若使用本仓库，请按自己的硬件、电源和 LED 驱动方案重新验证。

## English

A small Arduino RGB plant-lamp experiment controlled by serial text commands. It also works with a Bluetooth module in transparent UART mode. The public version keeps the protocol and control logic generic and excludes private data, credentials, vendor bundles, and third-party library source.

See the Chinese quick start above and [`docs/protocol.md`](docs/protocol.md).

## License

MIT License. See [`LICENSE`](LICENSE).

