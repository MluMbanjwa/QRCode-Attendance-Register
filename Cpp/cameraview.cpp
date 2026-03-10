#include "cameraview.h"

CameraView::CameraView(QWidget *parent): QVideoWidget()
{
    m_camera=new QCamera(this);
    m_session=new QMediaCaptureSession(this);
    m_imageCapture=new QImageCapture(this);

    m_session->setCamera(m_camera);
    m_session->setVideoOutput(this);
    m_session->setImageCapture(m_imageCapture);

    connect(m_imageCapture, &QImageCapture::imageCaptured, this, [=](int id, const QImage &preview) {
        Q_UNUSED(id);
       // qDebug() << "Image Captured!";
    });

    connect(m_imageCapture, &QImageCapture::imageSaved, this, [=](int id, const QString &filePath) {
        Q_UNUSED(id);
       // qDebug() << "Image saved to:" << filePath;
    });
}
CameraView::~CameraView()
{
}

void CameraView::startCamera()
{
    m_camera->start();
    this->show();
}

void CameraView::stopCamera()
{
    m_camera->stop();
}

void CameraView::captureImage()
{
    if (!m_camera->isActive()) {
        qDebug() << "Camera is not active or ImageCapture is not available!";
        return;
    }

    // Generate a unique filename for the captured image
    QString picturesLocation = QStandardPaths::writableLocation(QStandardPaths::PicturesLocation);
    QDir().mkpath(picturesLocation); // Ensure the directory exists

    QString filePath = picturesLocation + "/image_" + ".png";

    // Connect the imageCaptured signal to a slot where we can handle the captured image
    connect(m_imageCapture, &QImageCapture::imageCaptured, this, &CameraView::handleCapturedImage);

    // Capture the image and save it to the specified file path
    m_imageCapture->captureToFile(filePath);
}

void CameraView::handleCapturedImage(int id, const QImage &image)
{
    // Ensure that the image is valid
    if (image.isNull()) {
        qDebug() << "Failed to capture the image!";
        return;
    }

    // Apply preprocessing (e.g., crop, grayscale, etc.)
    QImage preprocessedImage = preprocessImage(image);

    // Now save the preprocessed image
    QString picturesLocation = QStandardPaths::writableLocation(QStandardPaths::PicturesLocation);
    QDir().mkpath(picturesLocation); // Ensure the directory exists

    QString filePath = picturesLocation + "/image_processed_" + ".png";

    // Save the preprocessed image
    preprocessedImage.save(filePath);
    emit imageCaptured(filePath);

    qDebug() << "Captured and saved image:" << filePath;
}

QImage CameraView::preprocessImage(const QImage &image)
{
    // Example preprocessing: Convert to grayscale
    QImage grayImage = image.convertToFormat(QImage::Format_Grayscale8);

    // Example: Crop the image to focus on a QR code region (for demonstration)
    QRect qrRegion(image.width() / 4, image.height() / 4, image.width() / 2, image.height() / 2);  // Adjust the cropping area as needed
    QImage croppedImage = grayImage.copy(qrRegion);

    // You can add other preprocessing steps here (e.g., contrast enhancement, noise reduction)
    return croppedImage;
}



