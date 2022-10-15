int state;
int sv1 = 9;
int sv2 = 10;

void setup() {
  pinMode(sv1, OUTPUT);
  pinMode(sv2, OUTPUT);


  digitalWrite(sv1, LOW);
  digitalWrite(sv2, LOW);

  Serial.begin(115200);

  Serial.setTimeout(1);
}

void loop() {
  while (!Serial.available());
  state = Serial.readString().toInt();
  if(state == 0){
    Serial.print('OPEN');
    digitalWrite(sv1, HIGH);
    digitalWrite(sv2, HIGH);

  }
  if(state == 1){
    Serial.print('CLOSED');
    digitalWrite(sv1, LOW);
    digitalWrite(sv2, LOW);
  }
}
