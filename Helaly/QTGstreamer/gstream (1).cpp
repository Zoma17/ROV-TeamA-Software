#include "gstream.h"

gstream::gstream(QWidget *parent)
{
    verLay=new QVBoxLayout ();
    window=parent;
    window->setLayout(verLay);
    vSpacer=new QSpacerItem(1,1,(QSizePolicy::Policy = QSizePolicy:: Expanding),(QSizePolicy::Policy = QSizePolicy:: Expanding));
//    button=new QPushButton("USELESSSSS",parent);
//    verLay->addWidget(button);
//    window=new QWidget();
    action(parent);
}


int gstream::action(QWidget * renderingWindow)
{

    if (!g_thread_supported ())
      g_thread_init (NULL);

    gst_init (0, 0);
    int x=0;
    char * y= NULL;
    QApplication app(x, &y);
    app.connect(&app, SIGNAL(lastWindowClosed()), &app, SLOT(quit ()));

    // prepare the pipeline

    pipeline = gst_pipeline_new ("xvoverlay");
//    pipeline = gst_parse_launch ("udpsrc port=5022 ! application/x-rtp,encoding-name=H264 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! ximagesink name=sink", NULL);
//    pipeline = gst_parse_launch ("udpsrc port=5000 ! application/x-rtp,encoding-name=H264 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! ximagesink name=sink", NULL);
//    pipeline = gst_parse_launch ("v4l2src device='/dev/video0' ! video/x-raw,width=320,height=240 ! videoconvert ! x264enc tune=zerolatency ! rtph264pay ! udpsink host='bta3 el computer' port=5022"
//                                 ,NULL);
    // prepare the ui
//    window->resize(800 , 600);
//    window->show();
    source= gst_element_factory_make("udpsrc","source");
    buffer=gst_element_factory_make("rtpjitterbuffer","buffer");
    depay=gst_element_factory_make("rtph264depay","depay");
    decompressor=gst_element_factory_make("avdec_h264","deco");
    convert=gst_element_factory_make("videoconvert","converter");
    sink=gst_element_factory_make("ximagesink","sink");


    if (!pipeline || !source || !sink || !depay || !buffer || !convert || !decompressor) {
       g_printerr ("Not all elements could be created.\n");
       return -1;
     }
    caps= gst_caps_new_simple("application/x-rtp","media", G_TYPE_STRING, "video","encoding-name", G_TYPE_STRING,"H264",NULL);
    g_object_set(source,"port",5022,nullptr);
    g_object_set(source,"caps",caps, nullptr);
    gst_caps_unref(caps);


    gst_bin_add_many (GST_BIN (pipeline), source/*, filter*/,buffer,depay,decompressor,convert , sink, NULL);
      if (gst_element_link_many (buffer,depay,decompressor,convert , sink) != TRUE) {
          g_printerr ("Elements could not be linked.\n");
          gst_object_unref (pipeline);
          gst_object_unref (decompressor);
          gst_object_unref (depay);
          gst_object_unref (buffer);
//          gst_object_unref (caps);
          gst_object_unref (sink);
          gst_object_unref (filter);
          gst_object_unref (convert);
          gst_object_unref (source);

          return -1;
      }
      else if (!gst_element_link(source,buffer)){
          g_printerr("Error at linking source and buffer");
          gst_object_unref (pipeline);
          gst_object_unref (decompressor);
          gst_object_unref (depay);
          gst_object_unref (buffer);
//          gst_object_unref (caps);
          gst_object_unref (sink);
          gst_object_unref (filter);
          gst_object_unref (convert);
          gst_object_unref (source);
          return -1;
      }
    WId xwinid = window->winId();
//    sink=gst_bin_get_by_name(GST_BIN(pipeline),"sink");
    gst_video_overlay_set_window_handle (GST_VIDEO_OVERLAY (sink), xwinid);

    /**********************************************************************************************/
//    renderingWindow->resize(800 , 600);
//    renderingWindow->show();
//    WId xwinid = renderingWindow->winId();
//    sink=gst_bin_get_by_name(GST_BIN(pipeline),"sink");
//    gst_video_overlay_set_window_handle (GST_VIDEO_OVERLAY (sink), xwinid);

    /**********************************************************************************************/
    // run the pipeline

    GstStateChangeReturn sret = gst_element_set_state (pipeline,
        GST_STATE_PLAYING);
    if (sret == GST_STATE_CHANGE_FAILURE) {
      gst_element_set_state (pipeline, GST_STATE_NULL);
      gst_object_unref (pipeline);
      gst_object_unref (decompressor);
      gst_object_unref (depay);
      gst_object_unref (buffer);
      gst_object_unref (sink);
      gst_object_unref (filter);
      gst_object_unref (convert);
      gst_object_unref (source);
      // Exit application
      QTimer::singleShot(0, QApplication::activeWindow(), SLOT(quit()));
    }

    int ret = app.exec();

    window->hide();
    gst_element_set_state (pipeline, GST_STATE_NULL);
    gst_object_unref (pipeline);
    gst_object_unref (decompressor);
    gst_object_unref (depay);
    gst_object_unref (buffer);
    gst_object_unref (sink);
    gst_object_unref (filter);
    gst_object_unref (convert);
    gst_object_unref (source);
    return ret;

}

QWidget *gstream::getStream()
{
    return window;
}

void gstream::setRenderingWindow(QWidget *window)
{

}
