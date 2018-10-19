#-------------------------------------------------
#
# Project created by QtCreator 2018-09-24T19:45:04
#
#-------------------------------------------------

QT       += core gui
QT       += network




greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = JS
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    joystick.cpp

HEADERS  += mainwindow.h \
    joystick.h

FORMS    += mainwindow.ui

LIBS += -LE:/SDL2/SDL2-2.0.8/lib/x86
LIBS += -lSDL2

INCLUDEPATH += E:/SDL2/SDL2-2.0.8/include


