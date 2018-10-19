#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QUrl>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{


    ui->setupUi(this);

this->setFixedSize(600,550);
s.connectToHost("111.111.111.111",5000);
//s.connectToHost("127.0.0.1",8082);

       js=new Joystick;

       connect(js,SIGNAL(do_action(string)),this,SLOT(sendmsg(string)));



    }

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::end()
{
    this->close();

}

void MainWindow::sendmsg(string a)
{

    s.write(a.c_str());
   //s.write("hello");
}
