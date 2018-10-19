#ifndef JOYSTICK_H
#define JOYSTICK_H
/* Documentation
  x axis is numbered as 0,
  y axis is numbered as 1,
  rotation is numbered as 2,
  z axis is numbered as 3

  range is from -32768 to 32767

*/
#include <QDebug>
#include <SDL.h>
#include <SDL_joystick.h>
#include <QTimer>
#include<QObject>
#include <string.h>
using namespace std;
#define DEAD_ZONE 5000
#define GetAxis(JS,AXIS) SDL_JoystickGetAxis(JS,AXIS)
#define SGNFCANT 2000



class Joystick :public QObject
{
    Q_OBJECT
public:
    Joystick();
   private:
    SDL_Joystick *js;
    SDL_Event  event;
    QTimer * timer;
    int prev_x,prev_y,prev_z,prev_r;
    int pwms[5];
    string msg;

signals:
    void do_action(string);
public slots:
    void action();
};

#endif // JOYSTICK_H
