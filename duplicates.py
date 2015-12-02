#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
import list_duplicates
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import shutil
 
class myWin(QWidget):
  
  def __init__(self, parent=None):
    super(myWin, self).__init__()
    self.w = QWidget()
 
    self.buildWindow()
  
  def setResults(self,r):
    self.results = r
  
  def resizeEvent(self, event):
    print("Resized")
    self.view()

  def keyPressEvent(self, event):
    if type(event) == QKeyEvent:
      print(event.key())

      if event.text() == 'n':
        self.viewNext()
      if event.text() == 'p':
        self.viewPrev()
      event.accept()
    else:
      print("Another key")
      event.ignore()
  
  def move_to_dup_folder(self,file):
    dupname = "duplicates_script/"
    if ".." in file:
      print("Error: Cannot use relative paths: " + file)
      return

    if ":" in file:
      print("Error: Cannot use relative paths: " + file)
      return
      
    if not os.path.exists(dupname):
      os.mkdir(dupname)

    if os.path.exists(dupname + file):
      print("File " + file + " is already is already in duplicates. Will not move it.")
    else:
      if not os.path.exists(os.path.dirname(dupname + file)):
        os.mkdir(os.path.dirname(dupname + file))
	
      shutil.move(file, dupname + file)
 
    self.viewNext()
  
  def remove1(self):
    print("Remove " + str(self.i))    
    print("Remove " + str(self.results[self.i]))    
    print("Remove " + str(self.results[self.i][0]))
    self.move_to_dup_folder(str(self.results[self.i][0]))

  def remove2(self):
    print("Remove " + str(self.i))    
    print("Remove " + str(self.results[self.i]))    
    print("Remove " + str(self.results[self.i][1]))
    self.move_to_dup_folder(str(self.results[self.i][0]))
    
  def buildBindings(self):
    self.btn1.clicked.connect(self.remove1)
    self.btn2.clicked.connect(self.remove2)
    self.btnPrev.clicked.connect(self.viewPrev)
    self.btnNext.clicked.connect(self.viewNext)

  def buildChildren(self):
    self.img1 = QLabel("img1")
    self.img2 = QLabel("img2")
    
    self.label1 = QLabel("label1")
    self.label2 = QLabel("label2")
    self.btn1 = QPushButton("Remove")
    self.btn2 = QPushButton("Remove")
    
    self.btnPrev = QPushButton("Prev")
    self.btnNext = QPushButton("Next")

    self.label1.setSizePolicy(QSizePolicy(QSizePolicy.Ignored,QSizePolicy.Fixed))
    self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Ignored,QSizePolicy.Fixed))

  def buildWindow(self): 
    # Set window size. 
    self.resize(320, 240)

    self.results = []
    self.i = -1
  
    self.buildChildren()
    self.buildBindings()
  
    grid = QGridLayout()
      
    #hbox.addStretch(1)
    grid.addWidget(self.img1,0,0)
    grid.addWidget(self.img2,0,1)
    
    grid.addWidget(self.label1,1,0)
    grid.addWidget(self.label2,1,1)
            
    grid.addWidget(self.btn1,2,0)
    grid.addWidget(self.btn2,2,1)
    
    grid.addWidget(self.btnPrev,3,0)
    grid.addWidget(self.btnNext,3,1)
    
    self.setLayout(grid)
   
  def view(self):
    myPixmap1 = QPixmap((str(self.results[self.i][0])))
    myPixmap2 = QPixmap((str(self.results[self.i][1])))

    if myPixmap1.isNull() or myPixmap2.isNull():
      return False
    
    print("Viewing " + str(self.i))
    self.label1.setText(str(self.results[self.i][0]))
    self.label2.setText(str(self.results[self.i][1]))

    myScaledPixmap = myPixmap1.scaled(self.img1.size(), Qt.KeepAspectRatio)
    self.img1.setPixmap(myScaledPixmap)

    myScaledPixmap = myPixmap2.scaled(self.img2.size(), Qt.KeepAspectRatio)
    self.img2.setPixmap(myScaledPixmap)
    self.show()
    return True

  def viewPrev(self):
    # Show window
    i_old = self.i 
    self.i = self.i - 1
    print("Viewing")
    while self.i > -1:
      if self.view():
        print(self.i)
        return;
      else:
        self.i=self.i-1

    self.i = i_old
    print(self.i)  
  
  def viewNext(self):
    # Show window
    i_old = self.i 
    self.i = self.i + 1
    print("Viewing")
    while self.i < len(results):
      if self.view():
        print(self.i)
        return;
      else:
        self.i=self.i+1

    self.i = i_old
    print(self.i)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  if len(sys.argv) > 1:
    
    duplicates = list_duplicates.getDuplicates(sys.argv[1:])
    print(duplicates)
    results = list(filter(lambda x: len(x) > 1, duplicates.values()))
    mainW = myWin()
    mainW.setResults(results)
    mainW.viewNext()
  else:
      print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')
  sys.exit(app.exec_())


