#ifndef GSTREAM_H
#define GSTREAM_H
#include <QVBoxLayout>
#include <QObject>
#include <glib.h>
#include <gst/gst.h>
#include <gst/video/videooverlay.h>
#include <QApplication>
#include <QTimer>
#include <QWidget>
#include <QPushButton>
#include <QSpacerItem>

class gstream : public QObject
{
    Q_OBJECT
public:
    gstream(QWidget * parent);
    int action(QWidget * renderingWindow);
    QWidget * getStream();
    QWidget * window;
    void setRenderingWindow(QWidget * window);
private:
    GstElement *pipeline ,*source ,*buffer,*depay,*decompressor,*convert;
    GstElement * sink;
//    GstElement * source
    QVBoxLayout * verLay;
    QPushButton * button;
    GstCaps * caps;
    QSpacerItem vSpacer;

};

#endif // GSTREAM_H
