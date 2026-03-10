#ifndef QRCODEGENERATOR_H
#define QRCODEGENERATOR_H
#include <QZXing.h>
#include <QString>
#include <QImage>
#include <QFile>
class QRCodeGenerator
{
private:
    QImage *m_image;
    QString m_text;
public:
    QRCodeGenerator(QImage img);
    QRCodeGenerator(QString text);

    QImage *image() const;
    void setImage(QImage *newImage);
    QString text() const;
    void setText(const QString &newText);
    void saveCode(QString fileName);
};

#endif // QRCODEGENERATOR_H
