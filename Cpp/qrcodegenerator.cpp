#include "qrcodegenerator.h"

QString QRCodeGenerator::text() const
{
    return m_text;
}

void QRCodeGenerator::setText(const QString &newText)
{
    m_text = newText;
}

void QRCodeGenerator::saveCode(QString fileName)
{
    m_image->save(fileName);
    qDebug()<<"m_image->save(fileName);"<<fileName;
}

QRCodeGenerator::QRCodeGenerator(QString text)
{
    QZXing file;
    file.setDecoder(QZXing::EncoderFormat_QR_CODE);
    m_image=new QImage(file.encodeData(text,QZXing::EncoderFormat_QR_CODE,QSize(200,200)));
}

QImage *QRCodeGenerator::image() const
{
    return m_image;
}

void QRCodeGenerator::setImage(QImage *newImage)
{
    m_image = newImage;
}


QRCodeGenerator::QRCodeGenerator(QImage img)
{
    // Check if the image is valid
    if (img.isNull()) {
        qDebug() << "Error: Input image is null.";
        return;
    }
    // Convert the image to a format without alpha (no transparency)
    QImage nonAlphaImage = img.convertToFormat(QImage::Format_RGB888);

    // Convert to grayscale for better contrast
    QImage grayImage = nonAlphaImage.convertToFormat(QImage::Format_Grayscale8);

    // Optionally, apply simple thresholding to enhance contrast
    for (int y = 0; y < grayImage.height(); ++y) {
        for (int x = 0; x < grayImage.width(); ++x) {
            QColor pixelColor(grayImage.pixel(x, y));
            int grayValue = pixelColor.red();  // Grayscale image uses the same value for all channels
            grayValue = (grayValue > 128) ? 255 : 0;  // Apply a simple threshold at 128
            grayImage.setPixel(x, y, QColor(grayValue, grayValue, grayValue).rgb());
        }
    }

    // Create QZXing decoder
    QZXing gen;
    gen.setDecoder(QZXing::DecoderFormat_QR_CODE);  // Ensure QR code decoding is enabled
    gen.setTryHarder(true);  // Enable "try harder" mode for decoding difficult images

    // Attempt to decode the thresholded grayscale image
    m_text = gen.decodeImage(grayImage);
}

