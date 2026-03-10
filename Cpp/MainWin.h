#ifndef MAINWIN_H
#define MAINWIN_H

#include <QWidget>
#include <QLayout>
#include <QFormLayout>
#include "cameraview.h"
#include <QLabel>
#include <QPushButton>
#include <QDateTime>
#include <QTimeEdit>
#include "xlsxdocument.h"
#include <QLineEdit>
#include <QZXing.h>
#include <QFileDialog>
#include "qrcodegenerator.h"
#include <QTimer>
class Widget : public QWidget
{
    Q_OBJECT
private:
    QTimer *m_timer;
    QHBoxLayout* m_hLayout;
    QVBoxLayout* m_vlayout;
    QHBoxLayout *m_btnLayout;
    CameraView *m_camera;
    QLabel *m_lblQRCode;
    QLabel* m_lblInfo;
    QFormLayout* m_layout;
    QPushButton* m_btnstart,*m_btnstop,*m_btnclose;
    QTimeEdit *m_time;
    QString m_log;
    QLineEdit * m_nameOfMeeting;

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
    QString log() const;
    void setLog(const QString &newLog);
    QString decode(QImage img);
public slots:
    void startRegistration();
    void stopRegistration();
    void endMeeting();
    void writeToFile();
    void createQrCodes(QString fileName);
    void scan(QString fileNAme);
};
#endif // MAINWIN_H
