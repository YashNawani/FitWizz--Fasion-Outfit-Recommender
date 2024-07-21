from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo                                  
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import *
import pickle
import random

from recognition_module import *

class Ui_MainWindow(object):



    # Git check
    def capture_photo_with_camera(self):
        import cv2
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                photo_path = 'user_photo.jpg'
                cv2.imwrite(photo_path, frame)
                self.current_photo_path = photo_path
                print("Photo captured.")
                break
        cap.release()
        cv2.destroyAllWindows()
        self.ALL_PREDICT()

    def select_photo_from_system(self):
        photo_path, _ = QFileDialog.getOpenFileName(None, "Select file", "H:/")
        if photo_path:
            self.current_photo_path = photo_path
            print("Photo selected.")
            self.ALL_PREDICT()

    def set_preferred_gender(self, index):
        if index > 0:
            selected_gender = self.GenderComboBox.itemText(index)
            if selected_gender == "Mix":
                self.gender_set_by_user = False
                print("Gender selection cleared due to 'Mix' selection.")
            else:
                self.preferred_gender = selected_gender
                self.gender_set_by_user = True
                print("Preferred gender set to:", self.preferred_gender)
        else:
            self.gender_set_by_user = False
            print("Gender selection cleared.")

    def ALL_PREDICT(self):
        sub, info, res_place_holder = single_classification(self.current_photo_path)
        parsed_info = self.parse_info(info)
        if not hasattr(self, 'parsed_items'):
            self.parsed_items = []
        self.parsed_items.append(parsed_info)
        if sub == "top":
            item = QtWidgets.QListWidgetItem(info)
            self.TOP_LIST.addItem(item)
            self.top.append(res_place_holder)
        elif sub == "bottom":
            item = QtWidgets.QListWidgetItem(info)
            self.BOTTOM_LIST.addItem(item)
            self.bottom.append(res_place_holder)
        elif sub == "foot":
            item = QtWidgets.QListWidgetItem(info)
            self.SHOE_LIST.addItem(item)
            self.shoes.append(res_place_holder)
 
    def TOP_LIST_EDIT(self):
        selected_items = self.TOP_LIST.selectedItems()
        text, okPressed = QtWidgets.QInputDialog.getText(self.AddTopButton, "EDIT", "Please Edit This Top:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
        for i in selected_items:
            self.TOP_LIST.takeItem(self.TOP_LIST.row(i))
        if okPressed and text != '':
            item = QtWidgets.QListWidgetItem(text)
            self.TOP_LIST.addItem(item)
 
    def TOP_LIST_DEL(self):
        selected_items = self.TOP_LIST.selectedItems()
        for i in selected_items:
            self.TOP_LIST.takeItem(self.TOP_LIST.row(i))
        text = selected_items[0].text()
        path = text.split(", ")[-1]
        for i in self.top:
            if i[-1] == path:
                self.top.remove(i)
 
    def BOTTOM_LIST_EDIT(self):
        selected_items = self.BOTTOM_LIST.selectedItems()
        text, okPressed = QtWidgets.QInputDialog.getText(self.AddBottomButton, "EDIT", "Please Edit This Bottom:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
        for i in selected_items:
            self.BOTTOM_LIST.takeItem(self.BOTTOM_LIST.row(i))
        if okPressed and text != '':
            item = QtWidgets.QListWidgetItem(text)
            self.BOTTOM_LIST.addItem(item)
 
    def BOTTOM_LIST_DEL(self):
        selected_items = self.BOTTOM_LIST.selectedItems()
        for i in selected_items:
            self.BOTTOM_LIST.takeItem(self.BOTTOM_LIST.row(i))
        text = selected_items[0].text()
        path = text.split(", ")[-1]
        for i in self.bottom:
            if i[-1] == path:
                self.bottom.remove(i)



    def SHOE_LIST_EDIT(self):
        selected_items = self.SHOE_LIST.selectedItems()
        text, okPressed = QtWidgets.QInputDialog.getText(self.AddShoeButton, "EDIT", "Please Edit This Shoes:", QtWidgets.QLineEdit.Normal, selected_items[0].text())
        for i in selected_items:
            self.SHOE_LIST.takeItem(self.SHOE_LIST.row(i))
        if okPressed and text != '':
            item = QtWidgets.QListWidgetItem(text)
            self.SHOE_LIST.addItem(item)
 
    def SHOE_LIST_DEL(self):
        selected_items = self.SHOE_LIST.selectedItems()
        for i in selected_items:
            self.SHOE_LIST.takeItem(self.SHOE_LIST.row(i))
        text = selected_items[0].text()
        path = text.split(", ")[-1]
        for i in self.shoes:
            if i[-1] == path:
                self.shoes.remove(i)
 
    def Generate(self):
        with open('filenames.pkl', 'rb') as f:
            items = pickle.load(f)
        current_season = toseason
        genders = set()
        styles = set()
        season = set()
        for item in self.parsed_items:
            genders.add(item['gender'])
            styles.add(item['style'])
            season.add(item['season'])
        if not self.season_set_by_user:
            preferred_season = random.choice(list(season))
        else:
            preferred_season = self.preferred_season
        if not self.gender_set_by_user:
            preferred_gender = random.choice(list(genders))
        else:
            preferred_gender = self.preferred_gender
        if not self.style_set_by_user:
            preferred_style = random.choice(list(styles))
        else:
            preferred_style = self.preferred_style
        print("Selected gender:", preferred_gender)
        print("Selected style:", preferred_style)
        print("Selected season:", preferred_season)
 
        def select_item(category, current_season, preferred_gender, preferred_style):
            items_in_category = [
                info for path, info in items.items()
                if info['category'] == category and info['gender'] == preferred_gender and info['style'] == preferred_style and info['season'] == preferred_season
            ]
            if items_in_category:
                return random.choice(items_in_category)['path']
            return None
 
        ad_top = select_item('Topwear', preferred_season, preferred_gender, preferred_style)
        ad_bot = select_item('Bottomwear', preferred_season, preferred_gender, preferred_style)
        ad_sho = select_item('Shoes', preferred_season, preferred_gender, preferred_style)
 
        def adjust_path(path):
            if path is None:
                return 'images/white.jpg'
            elif path.startswith('/Users/roshinisampath/Downloads/Internship Project I/Project/FitWizz Docs/py/images/images/'):
                return path[100:]
            return path
 
        print("Loading image from:", adjust_path(ad_top))
        self.listWidget_1.setPixmap(QtGui.QPixmap(adjust_path(ad_top)).scaled(281, 300))
        self.listWidget_2.setPixmap(QtGui.QPixmap(adjust_path(ad_bot)).scaled(281, 300))
        self.listWidget_3.setPixmap(QtGui.QPixmap(adjust_path(ad_sho)).scaled(281, 300))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TOP_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.TOP_LIST.setGeometry(QtCore.QRect(10, 30, 281, 181))
        self.TOP_LIST.setObjectName("TOP_LIST")
        self.AddTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddTopButton.setGeometry(QtCore.QRect(10, 210, 141, 41))
        self.AddTopButton.setAutoFillBackground(False)
        self.AddTopButton.setCheckable(False)
        self.AddTopButton.setObjectName("AddTopButton")
        self.DeleteTopButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteTopButton.setGeometry(QtCore.QRect(150, 210, 141, 41))
        self.DeleteTopButton.setCheckable(False)
        self.DeleteTopButton.setChecked(False)
        self.DeleteTopButton.setObjectName("DeleteTopButton")
        self.AddBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddBottomButton.setGeometry(QtCore.QRect(300, 210, 141, 41))
        self.AddBottomButton.setObjectName("AddBottomButton")
        self.BOTTOM_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.BOTTOM_LIST.setGeometry(QtCore.QRect(300, 30, 281, 181))
        self.BOTTOM_LIST.setObjectName("BOTTOM_LIST")
        self.DeleteBottomButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteBottomButton.setGeometry(QtCore.QRect(440, 210, 141, 41))
        self.DeleteBottomButton.setObjectName("DeleteBottomButton")
        self.AddShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddShoeButton.setGeometry(QtCore.QRect(590, 210, 141, 41))
        self.AddShoeButton.setObjectName("AddShoeButton")
        self.SHOE_LIST = QtWidgets.QListWidget(self.centralwidget)
        self.SHOE_LIST.setGeometry(QtCore.QRect(590, 30, 281, 181))
        self.SHOE_LIST.setObjectName("SHOE_LIST")
        self.DeleteShoeButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteShoeButton.setGeometry(QtCore.QRect(730, 210, 141, 41))
        self.DeleteShoeButton.setObjectName("DeleteShoeButton")
        self.GenerateButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateButton.setGeometry(QtCore.QRect(440, 270, 431, 81))
        self.GenerateButton.setObjectName("GenerateButton")
        self.HistoryButton = QtWidgets.QPushButton(self.centralwidget)
        self.HistoryButton.setGeometry(QtCore.QRect(10, 270, 431, 81))
        self.HistoryButton.setObjectName("HistoryButton")
        self.TopLabel = QtWidgets.QLabel(self.centralwidget)
        self.TopLabel.setGeometry(QtCore.QRect(140, 10, 60, 16))
        self.TopLabel.setTextFormat(QtCore.Qt.RichText)
        self.TopLabel.setObjectName("TopLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)