// Arduino RGB plant lamp controlled by serial or transparent Bluetooth UART.
// Commands: R0..R255, G0..G255, B0..B255; separate tokens with commas/spaces.

#include <Arduino.h>
#include <stdlib.h>
#include <string.h>

namespace {
constexpr uint8_t kRedPin = 11;
constexpr uint8_t kGreenPin = 10;
constexpr uint8_t kBluePin = 9;
constexpr size_t kBufferSize = 32;

char inputBuffer[kBufferSize];
size_t inputLength = 0;

void applyToken(char *token) {
  if (token == nullptr || token[0] == '\0') {
    return;
  }

  const char channel = token[0];
  if (channel != 'r' && channel != 'R' && channel != 'g' &&
      channel != 'G' && channel != 'b' && channel != 'B') {
    return;
  }

  const long value = constrain(strtol(token + 1, nullptr, 10), 0L, 255L);
  const uint8_t pwm = static_cast<uint8_t>(value);
  if (channel == 'r' || channel == 'R') {
    analogWrite(kRedPin, pwm);
  } else if (channel == 'g' || channel == 'G') {
    analogWrite(kGreenPin, pwm);
  } else {
    analogWrite(kBluePin, pwm);
  }
}

void applyLine() {
  inputBuffer[inputLength] = '\0';
  char *token = strtok(inputBuffer, ", \\t");
  while (token != nullptr) {
    applyToken(token);
    token = strtok(nullptr, ", \\t");
  }
  inputLength = 0;
}
}  // namespace

void setup() {
  Serial.begin(9600);
  pinMode(kRedPin, OUTPUT);
  pinMode(kGreenPin, OUTPUT);
  pinMode(kBluePin, OUTPUT);
  analogWrite(kRedPin, 0);
  analogWrite(kGreenPin, 0);
  analogWrite(kBluePin, 0);
}

void loop() {
  while (Serial.available() > 0) {
    const char ch = static_cast<char>(Serial.read());
    if (ch == '\n' || ch == '\r') {
      if (inputLength > 0) {
        applyLine();
      }
      continue;
    }
    if (inputLength < kBufferSize - 1) {
      inputBuffer[inputLength++] = ch;
    } else {
      // Drop an overlong frame instead of writing past the buffer.
      inputLength = 0;
    }
  }
}

