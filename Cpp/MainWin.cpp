#include "MainWin.h"
#include <QZXing.h>


QString Widget::log() const
{
    return m_log;
}

void Widget::setLog(const QString &newLog)
{
    m_log = newLog;
}

QString Widget::decode(QImage img)
{
    QRCodeGenerator qrgen(img);
    return qrgen.text();
}

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    m_hLayout=new QHBoxLayout;
    m_btnLayout=new QHBoxLayout;
    m_vlayout=new QVBoxLayout;
    m_camera=new CameraView(this);
    m_nameOfMeeting=new QLineEdit(this);
    m_lblQRCode=new QLabel("\n\n\n\n\n",this);
    m_lblInfo=new QLabel(this);
    m_layout=new QFormLayout(this);
    m_btnclose=new QPushButton("End Session",this);
    m_btnstart=new QPushButton("Start Registration",this);
    m_btnstop=new QPushButton("Stop Registration",this);
    m_time=new QTimeEdit(this);
    m_timer=new QTimer(this);
    m_timer->setInterval(100);
    m_timer->start();
    m_time->setTime(QTime::currentTime());

    m_vlayout->addWidget(m_lblQRCode);
    m_vlayout->addWidget(m_lblInfo);

    m_hLayout->addWidget(m_camera);
    m_hLayout->addLayout(m_vlayout);

    m_btnLayout->addWidget(m_btnclose);
    m_btnLayout->addWidget(m_btnstop);
    m_btnLayout->addWidget(m_btnstart);

    m_layout->addRow("Enter The name of the meeting: ",m_nameOfMeeting);
    m_layout->addRow("Enter time to start the meeting: ",m_time);
    m_layout->addRow(m_hLayout);
    m_layout->addRow(m_btnLayout);

    connect(m_timer,SIGNAL(timeout()),m_camera,SLOT(captureImage()));
    connect(m_camera,SIGNAL(imageCaptured(QString)),this,SLOT(scan(QString)));
    connect(m_btnstart,SIGNAL(clicked(bool)),this,SLOT(startRegistration()));
    connect(m_btnstop,SIGNAL(clicked(bool)),this,SLOT(stopRegistration()));
    connect(m_btnclose,SIGNAL(clicked(bool)),this,SLOT(endMeeting()));
    setLayout(m_layout);
}

Widget::~Widget() {}

void Widget::startRegistration()
{
    m_camera->startCamera();
    m_time->setEnabled(false);
    m_log=m_nameOfMeeting->text()+"\n";
    m_log+="Date: "+QDate::currentDate().toString()+"\n";
    m_log+="Time: "+m_time->time().toString()+"\n";
    m_log+="Registration Started at: "+QTime::currentTime().toString()+"\n";
    m_lblInfo->setText(m_log);

}

void Widget::stopRegistration()
{
    m_camera->stopCamera();
    m_log+="Registration Stopped at: "+QTime::currentTime().toString()+"\n";
    m_lblInfo->setText(m_log);
}

void Widget::endMeeting()
{
    m_log+="Meeting ended at: "+QTime::currentTime().toString()+"\n";
    writeToFile();
    close();
}

void Widget::writeToFile()
{
    QXlsx::Document file;
    QStringList lines=log().split("\n",Qt::SkipEmptyParts);
    for(int i=1;i<lines.size()+1;i++)
    {
        file.write(i,1,lines.at(i-1));
    }
    QString fileName=QFileDialog::getSaveFileName(this,"SAVE AS","./","*.xlsx");
    file.saveAs(fileName);
}

void Widget::createQrCodes(QString fileName)
{
    QXlsx::Document file(fileName,this);
    QRCodeGenerator *generator;
    qDebug()<<file.dimension().rowCount();
    for(int i=1;i<file.dimension().rowCount();i++)
    {
            generator=new QRCodeGenerator(file.read(i,1).toString());
            generator->saveCode("QRCodes_images/"+QString::number(i)+".png");
    }
}

void Widget::scan(QString fileName)
{
    // Load the image
    QImage image(fileName);

    // Check if the image is loaded successfully
    if (image.isNull()) {
        qDebug() << "Failed to load image:" << fileName;
        return;  // Early exit if image loading fails
    }

    // Attempt to decode the QR code using your QRCodeGenerator
    QRCodeGenerator gen(image);

    // Check if the text is decoded successfully
    QString decodedText = gen.text();

    if (decodedText.isEmpty()) {
        qDebug() << "QR code decoding failed!";
    } else {
        qDebug() << "Decoded text:" << decodedText;
    }

    // Set the timer interval and start it
    m_timer->setInterval(1000);
    m_timer->start();
}

