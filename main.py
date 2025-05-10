#Импорт библиотек
import os
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import *

'''Создание интерфейса'''
#Создание виджетов
app = QApplication([])
win = QWidget()
win.resize(300, 400)
win.setWindowTitle("Easy Editor")
btn_dir = QPushButton("Папка")
btn_left = QPushButton("Лево")
btn_right = QPushButton("Право")
btn_mirror = QPushButton("Зеркало")
btn_sharpness = QPushButton("Резкость")
btn_gray = QPushButton("Ч/Б")
btn_blur = QPushButton("Размытыть")
btn_contour = QPushButton("Контур")
btn_detail = QPushButton("Детализировать")
btn_smooth = QPushButton("Сглаживание")
# btn_save = QPushButton("Сохранить")
# btn_reset = QPushButton("Сбросить фильтры")
list_img = QListWidget()
label = QLabel("Здесь могла быть ваша реклама)))")

#Создание лэйаутов
row2 = QHBoxLayout()
row4 = QHBoxLayout()
col1 = QVBoxLayout()
col3 = QVBoxLayout()

#Закрепление виджетов к лэйаутам
col1.addWidget(btn_dir)
col1.addWidget(list_img)
row2.addWidget(btn_left)
row2.addWidget(btn_right)
row2.addWidget(btn_mirror)
row2.addWidget(btn_sharpness)
row2.addWidget(btn_gray)
row2.addWidget(btn_blur)
row2.addWidget(btn_contour)
row2.addWidget(btn_detail)
row2.addWidget(btn_smooth)
# row2.addWidget(btn_save)
# row2.addWidget(btn_reset)
col3.addWidget(label)

#Закрепление лэйаутов
col3.addLayout(row2)
row4.addLayout(col1)
row4.addLayout(col3)
win.setLayout(row4)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        """
        Сохраняет изображение в папку "Modified/" в рабочей директории.
        """
        path = os.path.join(workdir, self.save_dir)  # Формируем путь к папке для сохранённых изображений
        if not os.path.exists(path):  # Если папка не существует, создаём её
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)  # Полный путь к файлу сохранения
        self.image.save(fullname)  # Сохраняем изображение

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        w, h = label.width(), label.height()
        scaled_pixmap = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))
        
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_contour(self):
        self.image = self.image.filter(CONTOUR)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_detail(self):
        self.image = self.image.filter(DETAIL)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

    def do_smooth(self):
        self.image = self.image.filter(SMOOTH)
        self.saveImage()
        self.showImage(os.path.join(workdir, self.save_dir, self.filename))

workimage = ImageProcessor()

def showChosenImage():
    if list_img.currentRow() >= 0:
        filename = list_img.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

# Функция для фильтрации списка файлов по заданным расширениям
def filter(files, extensions):
    result = []  # Создаем пустой список, куда будут добавляться файлы с нужными расширениями
    for filename in files:  # Проходим по каждому файлу из переданного списка
        for ext in extensions:  # Перебираем каждое допустимое расширение
            if filename.endswith(ext):  # Проверяем, заканчивается ли имя файла на текущее расширение
                result.append(filename)  # Если да, добавляем файл в список результатов
    return result  # Возвращаем список файлов, удовлетворяющих условиям фильтра

# Функция для выбора рабочей директории через диалоговое окно
def chooseworkdir():
    global workdir  # Объявляем, что будем использовать глобальную переменную workdir
    workdir = QFileDialog.getExistingDirectory()  # Открываем диалог выбора директории и сохраняем выбранный путь

# Функция для отображения списка имен файлов в виджете QListWidget
def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']  # Определяем список допустимых форматов изображений
    chooseworkdir()  # Вызываем функцию для выбора рабочей директории
    # Получаем список всех файлов в выбранной директории и фильтруем их по допустимым расширениям
    filenames = filter(os.listdir(workdir), extensions)
    list_img.clear()  # Очищаем виджет списка, чтобы удалить предыдущие записи
    for filename in filenames:  # Перебираем каждый файл, удовлетворяющий фильтру
        list_img.addItem(filename)  # Добавляем имя файла в виджет списка для отображения

list_img.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)
btn_gray.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_flip)
btn_sharpness.clicked.connect(workimage.do_sharpen)
btn_blur.clicked.connect(workimage.do_blur)
btn_contour.clicked.connect(workimage.do_contour)
btn_detail.clicked.connect(workimage.do_detail)
btn_smooth.clicked.connect(workimage.do_smooth)

#Показывание окна
win.show()
app.exec()