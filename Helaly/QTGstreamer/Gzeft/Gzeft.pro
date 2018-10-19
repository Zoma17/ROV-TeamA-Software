#-------------------------------------------------
#
# Project created by QtCreator 2018-10-17T06:57:49
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Gzeft
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

CONFIG += c++11

SOURCES += \
        main.cpp

HEADERS +=

FORMS +=

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

unix {
   CONFIG += link_pkgconfig
   PKGCONFIG += gstreamer-1.0
}


INCLUDEPATH += /usr/include/gstreamer-1.0/ \
/usr/include/glib-2.0/ \
/usr/lib/x86_64-linux-gnu/glib-2.0/include/ \
/usr/include/libxml2/

LIBS += -std=gnu++11
LIBS += -lpthread
LIBS += `pkg-config --cflags --libs  gstreamer-1.0`

