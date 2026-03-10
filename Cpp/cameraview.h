#ifndef CAMERAVIEW_H
#define CAMERAVIEW_H

#include <QWidget>
#include <QMediaCaptureSession>
#include <QCamera>
#include <QtMultimedia>
#include <QtMultimediaWidgets/QVideoWidget>
#include <QImageCapture>
#include<QDateTime>
class CameraView: public QVideoWidget
{
    Q_OBJECT
private:
    QCamera *m_camera;
    QMediaCaptureSession *m_session;
    QImageCapture *m_imageCapture;
public:
    explicit CameraView(QWidget *parent = nullptr);
    void handleCapturedImage(int id, const QImage &image);
    QImage preprocessImage(const QImage &image);
    QRect detectQRCodeRegion(const QImage &image);
    ~CameraView();
signals:
    void imageCaptured(const QString &filePath);
public slots:
    void startCamera();
    void stopCamera();
    void captureImage();
};

#endif // CAMERAVIEW_H
