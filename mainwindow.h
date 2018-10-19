#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDebug>
#include <QTimer>
#include <joystick.h>
#include <QTcpSocket>

#undef main

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
        Ui::MainWindow *ui;

        int x,y,z,r;
        Joystick *js;
        QTcpSocket s;
public slots:

      void end();
      void sendmsg(string);
};

#endif // MAINWINDOW_H
