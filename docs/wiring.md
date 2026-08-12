# Wiring

## Logic-level example

| Signal | Arduino Uno | Connect to |
|---|---:|---|
| Red PWM | D11 | Red driver input |
| Green PWM | D10 | Green driver input |
| Blue PWM | D9 | Blue driver input |
| UART RX | D0 / RX | Bluetooth TX |
| UART TX | D1 / TX | Bluetooth RX through level shifting if required |
| Ground | GND | Common logic/driver ground |

```text
USB serial or Bluetooth UART
            │
            ▼
      Arduino Uno
       D11 D10 D9
        │   │   │
        ▼   ▼   ▼
    external LED driver  ──>  RGB LED / low-voltage strip
```

Do not connect a high-power lamp or strip directly to an Arduino pin. Use a
driver matched to the lamp voltage/current, current limiting, a suitable power
supply, and a common reference ground. See [safety.md](safety.md).
