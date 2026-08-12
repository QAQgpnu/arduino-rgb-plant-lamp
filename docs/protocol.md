# Serial command protocol

The sketch accepts a line of one or more comma- or whitespace-separated tokens.

| Token | Meaning |
|---|---|
| `R0` to `R255` | Set red PWM duty |
| `G0` to `G255` | Set green PWM duty |
| `B0` to `B255` | Set blue PWM duty |
| `OFF` | Set all three channels to zero |
| `STATUS` | Print the current PWM state |

Channel letters are case-insensitive. Numeric values outside `0..255` are
clamped. Malformed numeric tokens such as `Rabc` and unknown tokens are ignored.
A frame ends with `LF` or `CRLF`.

Examples:

```text
R255
G80,B20
r0 g0 b0
STATUS
OFF
```

The protocol intentionally does not include credentials, network addresses,
device IDs, or vendor-specific commands.
