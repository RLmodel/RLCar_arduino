
#define UP 7
#define DOWN 8

String data;

void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(UP, OUTPUT);
  pinMode(DOWN, OUTPUT);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  
  //data = Serial.read();
  //String cmd = data;

  
  //digitalWrite(UP, HIGH);
  printf("up");
  Serial.println("hello");
  delay(1000);

  
  //digitalWrite(DOWN, HIGH);
  printf("down");
    
  delay(1000);
  
  printf("stop");
    

  
  delay(1000);
  
  //digitalWrite(UP, HIGH);
  //digitalWrite(DOWN, HIGH);
   
  //delay(1000);


}