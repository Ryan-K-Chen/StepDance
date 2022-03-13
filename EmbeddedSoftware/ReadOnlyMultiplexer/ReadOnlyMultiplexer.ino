#define S0   A0
#define S1   A1
#define S2   A2
#define MUX1 12
#define MUX2 13

#define SOUT1 2
#define SOUT2 3
#define SRCLK 4
#define RCLK  5

void setup() {
  // put your setup code here, to run once:
  pinMode(S0, INPUT);
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(MUX1, INPUT);
  pinMode(MUX2, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  static uint8_t state1 = 0, state2 = 0;
  uint8_t i = (digitalRead(S2) << 2) | (digitalRead(S1) << 1) | (digitalRead(S0));
  
  uint8_t mux1 = digitalRead(MUX1);
  uint8_t mux2 = digitalRead(MUX2);
  if (mux1) state1 |=  (1 << i);
  else      state1 &= ~(1 << i);
  if (mux2) state2 |=  (1 << i);
  else      state2 &= ~(1 << i);

  if (i == 7) {
    digitalWrite(SRCLK, LOW);
    for(uint8_t j = 0; j < 8; ++j){
      digitalWrite(SOUT1, state1 & (1 << j));
      digitalWrite(SOUT2, state2 & (1 << j));
      digitalWrite(SRCLK, HIGH);
      digitalWrite(SRCLK, LOW);
    }
    digitalWrite(RCLK, HIGH);
    digitalWrite(RCLK, LOW);
  }
}
