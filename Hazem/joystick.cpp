#include "joystick.h"
/*
X,Y,Z,R are the axes of the joystick for simplicity
*/
#define X SDL_JoystickGetAxis(js,0)
#define Y (-SDL_JoystickGetAxis(js,1))
#define Z SDL_JoystickGetAxis(js,3)
#define R SDL_JoystickGetAxis(js,2)

#define Axis_Range 32767
#define R_Range 32767
// =============================================
#define Brake_Force 140
#define Neutral 290
#define Forward_Force 440
// front right motor -> 1
// front left motor -> 2
// back right motor -> 3
// back left motor -> 4
// ==============================================
int convert_to_PWM(int x , int Range)
{
   double percentage = abs((double)x/Range);
   if (x > 0)
       return Neutral + percentage * (Forward_Force - Neutral);
   else if (x < 0)
       return Neutral - percentage * (Neutral - Brake_Force);
   else
       return Neutral;
}

Joystick::Joystick()
{
   timer =new QTimer;
   timer->start();
   timer->setInterval(50);

   SDL_Init(SDL_INIT_JOYSTICK);
   SDL_Init(SDL_INIT_EVERYTHING);

    if (SDL_INIT_JOYSTICK<0)
        qDebug()<<"failed to init";
    SDL_JoystickEventState(SDL_ENABLE);
    js= SDL_JoystickOpen(0);

    if (SDL_JoystickGetAttached(js)){
        qDebug() <<"attached";
    qDebug() <<"Num of buttons is : "<<SDL_JoystickNumButtons(js);
    qDebug()<<"Num of hats is : " <<SDL_JoystickNumHats(js);
    qDebug() <<"num of axes is :" <<SDL_JoystickNumAxes(js);
    qDebug() <<"num of balls is :" <<SDL_JoystickNumBalls(js); }


connect(timer,SIGNAL(timeout()),this,SLOT(action()));

}

void Joystick::action()
{


while (SDL_PollEvent(&event)){
switch (event.type){
case SDL_JOYAXISMOTION:
if (abs(X-prev_x) >SGNFCANT || abs(Y-prev_y) >SGNFCANT ||abs(Z-prev_z) >(SGNFCANT) || abs(R-prev_r) >(SGNFCANT*2)){
   prev_x=X,prev_y=Y,prev_z=Z,prev_r=R;

   // Z Direction
// ==============================================================
   if (abs(Z)>DEAD_ZONE)
   {
       pwms[0]=convert_to_PWM(Z,Axis_Range);
   }
   else if (abs(Z) < DEAD_ZONE)
   {
       pwms[0]=convert_to_PWM(0,Axis_Range);
   }
// ==============================================================
 // Diagonal

   // Dead Zone *2 for more flexablity in forward and backward
   if (abs(X)>(DEAD_ZONE*2) && abs(Y)>(DEAD_ZONE*2))
   {
    if (X>0)
    {
      if(Y>0)
      {
          // Forward Right
          pwms[2] = convert_to_PWM(X,Axis_Range);
          pwms[3] = convert_to_PWM(Y,Axis_Range);
          pwms[1]=pwms[4]=convert_to_PWM(0,Axis_Range);
      }
      else if (Y<0)
      {
          // Backword Right
          pwms[1] = convert_to_PWM(Y,Axis_Range);
          pwms[4] = convert_to_PWM(-X,Axis_Range);
          pwms[2]=pwms[3]=convert_to_PWM(0,Axis_Range);
          // -X because the function reverse the motor direction according to sign of x
      }
     }
   else if(Y>0)
   {     // Forward Left
        pwms[1] = convert_to_PWM(-X,Axis_Range);
        pwms[4] = convert_to_PWM(Y,Axis_Range);
        pwms[2]=pwms[3]=convert_to_PWM(0,Axis_Range);
   }
   else
   {
        // Backword Left
        pwms[2] = convert_to_PWM(Y,Axis_Range);
        pwms[3] = convert_to_PWM(X,Axis_Range);
        pwms[1]=pwms[4]=convert_to_PWM(0,Axis_Range);
   }

   }
// ==============================================================
else if (abs(X) >DEAD_ZONE && abs(Y) < DEAD_ZONE*2)
{
 // Right & Left
 
       pwms[2] = pwms[3] =convert_to_PWM (X,Axis_Range);
       pwms[1] = pwms[4] =convert_to_PWM(-X,Axis_Range);
   
}
// ==============================================================
else if (abs(Y) >DEAD_ZONE && abs(X) < DEAD_ZONE*2)
{
   // Forward & Back
   for (int i =1 ;i<5 ;i++)
   {
       pwms[i] = convert_to_PWM(Y,Axis_Range);
   }

   if ( abs(R)>(DEAD_ZONE * 2) && Y > DEAD_ZONE)
   {
      // turn off the motor that in the direction of rotation
      if (R>0)
      {
             pwms[1] = convert_to_PWM(0,Axis_Range);
             pwms[2] = convert_to_PWM(R,R_Range);
      }
      else if (R<0)
      {
             pwms[2] = convert_to_PWM(0,Axis_Range);
             pwms[1] = convert_to_PWM(-R,R_Range);
      }
   }
   else if (abs(R)>(DEAD_ZONE * 2) && Y < -DEAD_ZONE)
   {
       // turn off the motor that in the direction of rotation
       if (R>0)
       {
          pwms[4] = convert_to_PWM(0,Axis_Range);
          pwms[3] = convert_to_PWM(-R,R_Range);
       }
       else if (R<0)
       {
          pwms[3] = convert_to_PWM(0,Axis_Range);
          pwms[4] = convert_to_PWM(R,R_Range);
       }
   }
}
// ==============================================================
else if (abs(R)>(DEAD_ZONE))
{
   pwms[1] = pwms[3] = convert_to_PWM(-R,R_Range);
   pwms[2] = pwms[4] = convert_to_PWM(R,R_Range);
}
// ==============================================================
else
{
       for (int i =1 ;i<5 ;i++)
       {
           pwms[i] = convert_to_PWM(0,Axis_Range);
       }
}
// ==============================================================
   msg=to_string(pwms[0]);
   for(int i=1;i<5;i++)
       msg+=" "+to_string(pwms[i]);

   qDebug()<<msg.c_str();
   emit do_action(msg);

} break;


case SDL_JOYDEVICEADDED:
   qDebug()<< "joystick plugged";
   js= SDL_JoystickOpen(0);
   break;
// =============================================================
case SDL_JOYBUTTONDOWN:
     qDebug()<<"button down"<<event.jbutton.button;
     if (event.jbutton.button==3){
       msg="d";emit do_action(msg);}
     else if (event.jbutton.button==2){
       msg="u";emit do_action(msg);}
   // #### FOR Mecanical Mession ###
     else if (event.jbutton.button==10)
     {
         pwms[1] =convert_to_PWM(-50,100);
         pwms[2] =convert_to_PWM(50,100);
         pwms[3] =convert_to_PWM(100,100);
         pwms[4] =convert_to_PWM(-100,100);

         msg=to_string(pwms[0]);
         for(int i=1;i<5;i++)
             msg+=" "+to_string(pwms[i]);
         qDebug()<<msg.c_str();
         emit do_action(msg);
     }
      break;
// =============================================================
default: break;
}
}
}


