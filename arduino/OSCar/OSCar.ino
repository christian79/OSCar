#include <Servo.h>
//#include <DistanceGP2Y0A41SK.h>

int X;
int Y;
byte servoPin1 = 11;  //ESC
byte servoPin2 = 10;  //Steering
long previousMillis = 0;
long interval = 150;
Servo myServo1;
Servo myServo2;
//DistanceGP2Y0A41SK Dist;
int distance;


void setup()
{
  Serial1.begin(115200);
  myServo1.attach(servoPin1);
  myServo2.attach(servoPin2);
  myServo1.write( 90);
  myServo2.write(90);
  //Dist.begin(A0);
}

void loop()
{
  if (Serial1.available() > 0)
  {
    char syncChar = Serial1.read();
    if (syncChar == 'F')
    {
      X = Serial1.parseInt();
      forward();
    }
    if (syncChar == 'B')
    {
      X = Serial1.parseInt();
      backward();
    }
    if (syncChar == 'S')
    {
      Serial1.read();
      myServo1.write(90);
    }
    if (syncChar == 'Y')
    {
      Y = Serial1.parseInt();
      Y = map(Y, 20, 189, 135, 35);
      myServo2.write(Y);
    }
  }
}

void forward()
{
  byte ValX = map(X, 100, 189, 91, 179);
  myServo1.write(ValX);
}

void backward()
{
  byte valX = map(X, 89, 0, 89, 0);
  myServo1.write(valX);
}
    


