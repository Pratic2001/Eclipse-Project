#include <dht.h>
#include <LiquidCrystal.h>

dht DHT;

#define DHT11_PIN 7
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7); 

void setup(){
  pinMode(0, INPUT);
  pinMode(13, OUTPUT);
  lcd.begin(16, 2);
  lcd.print("Temperature: ");
  lcd.setCursor(0,1);
  lcd.print("Humidity: ");
  }
int temp;
int humid;
void loop(){
  int chk = DHT.read11(DHT11_PIN);
  int var = DHT.temperature;
  int var2 = DHT.humidity;
  if(var >= 1 && var <= 90)
    temp = var;
  if(var2 >= 1 && var2 <= 100)
    humid = var2;
  if(digitalRead(0) == 1){
    if(temp > 26)
      digitalWrite(13, HIGH);
    else
      digitalWrite(13, LOW);
    }
  else if(digitalRead(0) == 0)
    digitalWrite(13, LOW);
  lcd.setCursor(13,0);
  lcd.print(temp);
  lcd.setCursor(10, 1);
  lcd.print(humid);
}
