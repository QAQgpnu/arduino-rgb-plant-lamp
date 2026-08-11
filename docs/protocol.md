# Serial command protocol

The sketch accepts a line of one or more comma- or whitespace-separated tokens.

| Token | Meaning |
|---|---|
| `R0` … `R255` | Set red PWM duty |
| `G0` … `G255` | Set green PWM duty |
| `B0` … `B255` | Set blue PWM duty |

Channel letters are case-insensitive. Values outside `0..255` are clamped. Unknown tokens are ignored. A frame ends with `LF` or `CRLF`.

Examples:

```text
R255
G80,B20
r0 g0 b0
```

The protocol intentionally does not include credentials, network addresses, or vendor-specific commands.

