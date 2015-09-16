# -*- coding: utf-8 -*-
import glob
import os
import sys
import ctypes
from locale import getdefaultlocale
from zipfile import ZipFile
from PIL import Image
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from title_bar import Frame
import res

APP_ID = 'adriandev.imagecompressor.py-pyqt4.v1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.ctrl = False
        self.DIR_IMAGES = ''
        self.images_compressed_list = []
        self.btn_select_folder = QPushButton('Seleccionar carpeta...')
        self.lbl = QLabel()
        self.sld = QSlider(Qt.Horizontal)
        self.compress_chk = QCheckBox(u"Comprimir imágenes en un .zip")
        self.open_dir_chk = QCheckBox(u"Abrir carpeta al terminar")
        self.msg = QLabel('')
        self.image_view = QLabel()
        self.btn_compress = QPushButton('Comprimir...')

        self.set_ui()
        self.connects()

    def connects(self):
        self.connect(self.sld, SIGNAL('valueChanged(int)'), self.update_ui)
        self.connect(self.btn_select_folder, SIGNAL('clicked()'), self.select_dir)
        self.connect(self.btn_compress, SIGNAL('clicked()'), self.compress_img)

    def set_ui(self):
        self.setObjectName('form')
        # self.setFixedSize(250, 150)
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle('Image Compressor')
        self.setStyleSheet(self.set_style_qss())

        self.btn_select_folder.setObjectName('btn_select_folder')
        self.btn_select_folder.setMinimumHeight(30)

        self.lbl.move(75, 35)
        self.lbl.setMinimumWidth(18)
        self.lbl.setObjectName('lbl')

        self.sld.setValue(30)
        self.sld.setMinimumHeight(30)

        self.msg.setMinimumHeight(50)
        self.msg.setVisible(False)
        self.msg.setObjectName('msg')

        self.image_view.setFixedSize(100, 100)
        self.image_view.setVisible(False)
        self.image_view.setObjectName("image_view")

        self.btn_compress.setObjectName('btn_compress')
        self.btn_compress.setMinimumHeight(50)

        self.open_dir_chk.setChecked(True)

        grid = QGridLayout()
        grid.addWidget(self.btn_select_folder, 0, 0, 1, 2)
        grid.addWidget(self.sld, 1, 0)
        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.compress_chk, 2, 0)
        grid.addWidget(self.open_dir_chk, 3, 0)
        grid.addWidget(self.btn_compress, 4, 0, 1, 2)
        grid.addWidget(self.msg, 5, 0)
        grid.addWidget(self.image_view, 5, 1)
        self.setLayout(grid)

        self.update_ui()

    def update_ui(self):
        self.lbl.setText(str(self.sld.value()))
        # self.lbl.move(10 + self.sld.value() * 2.2, 35)

    def select_dir(self):
        self.btn_compress.setText('Comprimir...')
        directory = unicode(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if directory:
            self.btn_select_folder.setText(os.path.basename(directory))
            self.DIR_IMAGES = directory
            self.btn_compress.setVisible(True)
            self.msg.setVisible(False)
            self.ctrl = True

    def compress_img(self):
        self.btn_compress.setVisible(False)
        self.msg.setVisible(True)
        self.image_view.setVisible(True)
        if not self.ctrl:
            self.msg.setText('Seleccione una carpeta!!')
        else:
            dir_images = unicode(self.DIR_IMAGES.replace('/', '\\') + '\\')
            self.btn_select_folder.setText('...')
            cont = 0
            ctrl = False
            images_list = glob.glob(dir_images + '*.jpg') + \
                          glob.glob(dir_images + '*.png') + \
                          glob.glob(dir_images + '*.gif')
            if self.compress_chk.isChecked():
                myzip = ZipFile(dir_images + 'images.zip', 'w')
            for i in range(0, len(images_list)):
                ctrl = True
                self.btn_compress.setVisible(False)
                try:
                    file_name = os.path.basename(images_list[i])
                    self.msg.setText(
                        u'Comprimiendo imágenes...\n%s\n%s/%s' % (file_name, str(i + 1), str(len(images_list) + 1))
                    )
                    split_name = os.path.splitext(file_name)
                    file_name = split_name[0]
                    file_ext = split_name[1]
                    # mostrar la imagen actual q sera comprimida, escalar su contenido
                    self.image_view.setScaledContents(True)
                    self.image_view.setPixmap(QPixmap(dir_images + file_name + file_ext))
                    i = Image.open(images_list[i])
                    new_name = "%scompress_%s_%s%s" % (dir_images, self.sld.value(), file_name, file_ext)
                    i.save(new_name, quality=self.sld.value())
                    try:
                        myzip.write(new_name)
                    except UnboundLocalError:
                        pass
                    # self.images_compressed_list.append(new_name)
                    # permitir q los cambios en los controles ocurran en cada ciclo del for (mostrar la img y cambiar en text del lbl)
                    QApplication.processEvents()
                except ValueError:
                    print ValueError
                    cont += 1
            if not ctrl:
                self.msg.setText("No hay fotos para comprimir en esta\ncarpeta.")
            else:
                if cont > 0:
                    self.msg.setText("%s archivos no se puedieron comprimir." % cont)
                    os.system('start "" "%s"' % dir_images)
                else:
                    self.msg.setText(u"Todos los ficheros fueron comprimidos\ncon éxito.")
                    if self.open_dir_chk.isChecked():
                        os.system('start "" "%s"' % dir_images.encode(getdefaultlocale()[1]))

                    # for name in self.images_compressed_list:
                    #     myzip.write(name)

    @staticmethod
    def set_style_qss():
        return '''
                #form{
                    background-color: white;
                }
                #lbl{
                    color: #4075CC;
                }
                QSlider::handle:horizontal {
                /*background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);*/
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.3,
                            fx:0.5, fy:0.5, stop:0 #231E78, stop:1 #6495ED);

                border: 0px solid #2E6DA4;
                width: 18px;
                margin: -5px 0;
                border-radius: 8px;
                }
                QSlider::handle:horizontal:pressed{
                    background-color: #6495ED;
                }
                QSlider::groove:horizontal {
                    /*border: 1px solid #999999;*/
                    height: 7px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                    margin: 2px 0;
                }
                #btn_select_folder {
                    color: #333;
                    background-color: #FBFBFB;
                    border: 1px solid #C1C1C1;
                }
                #btn_compress{
                    color: white;
                    border: 1px solid #6495ED;
                    background-color: #6495ED;
                    font: 14px;
                    border-radius: 4px;
                }
                #btn_select_folder:hover{
                    background-color: #C1C1C1;
                }
                #btn_compress:hover{
                    background-color: #337AB7;
                }
                #msg{
                    color: #4075CC;
                    font-size: 14px;
                }
                #image_view{
                    border: 1px solid #333;
                }
                QCheckBox {
                    spacing: 10px;
                    color: #333;
                }
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                    border: 1px solid #d4d4d4;
                }
                QCheckBox::indicator:hover{
                    border: 1px solid #333;
                }
                QCheckBox::indicator:checked {
                    image: url(:/check);
                }
            '''


class UI(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.layout_add(Main())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UI()
    app.setWindowIcon(QIcon(":/icon"))
    app.exec_()
