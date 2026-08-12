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
uint8_t redPwm = 0;
uint8_t greenPwm = 0;
uint8_t bluePwm = 0;

char upperAscii(const char value) {
  return (value >= 'a' && value <= 'z') ? value - ('a' - 'A') : value;
}

bool equalsIgnoreCase(const char *value, const char *expected) {
  while (*value != '\0' && *expected != '\0') {
    if (upperAscii(*value) != upperAscii(*expected)) {
      return false;
    }
    ++value;
    ++expected;
  }
  return *value == '\0' && *expected == '\0';
}

void writeChannel(const char channel, const uint8_t pwm) {
  if (channel == 'r' || channel == 'R') {
    redPwm = pwm;
    analogWrite(kRedPin, redPwm);
  } else if (channel == 'g' || channel == 'G') {
    greenPwm = pwm;
    analogWrite(kGreenPin, greenPwm);
  } else {
    bluePwm = pwm;
    analogWrite(kBluePin, bluePwm);
  }
}

void printStatus() {
  Serial.print("STATE R=");
  Serial.print(redPwm);
  Serial.print(" G=");
  Serial.print(greenPwm);
  Serial.print(" B=");
  Serial.println(bluePwm);
}

void applyToken(char *token) {
  if (token == nullptr || token[0] == '\0') {
    return;
  }

  if (equalsIgnoreCase(token, "OFF")) {
    writeChannel('R', 0);
    writeChannel('G', 0);
    writeChannel('B', 0);
    return;
  }
  if (equalsIgnoreCase(token, "STATUS")) {
    printStatus();
    return;
  }

  const char channel = token[0];
  if (channel != 'r' && channel != 'R' && channel != 'g' &&
      channel != 'G' && channel != 'b' && channel != 'B') {
    return;
  }

  char *end = nullptr;
  const long parsedValue = strtol(token + 1, &end, 10);
  if (end == token + 1 || *end != '\0') {
    return;
  }
  const long value = constrain(parsedValue, 0L, 255L);
  const uint8_t pwm = static_cast<uint8_t>(value);
  writeChannel(channel, pwm);
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
  writeChannel('R', 0);
  writeChannel('G', 0);
  writeChannel('B', 0);
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
