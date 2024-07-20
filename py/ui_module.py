from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo                                  
from PyQt5.QtWidgets import QFileDialog, QLabel
from PyQt5.QtGui import *
import pickle
import random

from recognition_module import *

class Ui_MainWindow(object):





    
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