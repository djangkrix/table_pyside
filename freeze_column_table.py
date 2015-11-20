from PySide.QtGui import *
from PySide.QtCore import *
import random
import sys

class FreezeTableWidget(QTableView):
    def __init__(self, model, parent=None):
        super(FreezeTableWidget, self).__init__(parent)
        self.setModel(model)
        self.frozenTableView = QTableView(self)
        self.init()
        self.connect(self.horizontalHeader(),SIGNAL('sectionResized(int,int,int)'), self.updateSectionWidth)
        self.connect(self.verticalHeader(),SIGNAL('sectionResized(int,int,int)'), self.updateSectionHeight)
        self.connect(self.frozenTableView.verticalScrollBar(), SIGNAL('valueChanged(int)'),
               self.verticalScrollBar(), SLOT('setValue(int)'))
        self.connect(self.verticalScrollBar(), SIGNAL('valueChanged(int)'),
               self.frozenTableView.verticalScrollBar(), SLOT('setValue(int)'))
    def init(self):
        self.frozenTableView.setModel(self.model())
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setResizeMode(QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.setStyleSheet("QTableView { border: none;"
                                      "background-color: #9B9B9B;"
                                      "selection-background-color: #999}")
        self.frozenTableView.setSelectionModel(self.selectionModel())
        for col in range(1,self.model().columnCount()):
             self.frozenTableView.setColumnHidden(col, True)
        self.frozenTableView.setColumnWidth(0, self.columnWidth(0))
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerPixel)

    def updateSectionWidth(self,logicalIndex,i,newSize):
        if logicalIndex==0:
             self.frozenTableView.setColumnWidth(0,newSize)
             self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, i, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self,event):
        super(QTableView, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        if (cursorAction == self.MoveLeft and current.column()>0
                and  self.visualRect(current).topLeft().x() < self.frozenTableView.columnWidth(0) ):
            newValue = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() - self.frozenTableView.columnWidth(0)
            self.horizontalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        if (index.column()>0):
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
          self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
            self.frameWidth(),
            self.columnWidth(0),
            self.viewport().height()+self.horizontalHeader().height())

class MyWidget(QWidget):
    
    def __init__(self, parent=None):
        
        super(MyWidget, self).__init__(parent)
        model = QStandardItemModel()
        header = [u'Name', u'Math', u'Physics', u'Biology', u'Chemistry',u'Basa Jawa',u'Bahasa Indonesia',u'English',u'Sosiology',u'Geography',u'History']
        student_name = ['Adi','Budi','Cici','Didi','Eka','Faris','Geni','Hanif','Ismail','Junaedi']
        model.setHorizontalHeaderLabels(header)
        for row_index,name in enumerate(student_name): # Perulangan sebanyak jumlah baris tabel
            for column_index in range (len(header)): # Perulangan sebanyak jumlah kolom tabel
                if column_index == 0:
                    newItem = QStandardItem(name)
                else:
                    newItem = QStandardItem('%d ' % (random.randint(5,10)))
                model.setItem(row_index,column_index, newItem)
        tableView = FreezeTableWidget(model)
        layout = QVBoxLayout(self) # Menambahkan layout pada MyWidget
        layout.addWidget(tableView,0,0) #menambahkan Freeze Table ke dalam layout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    app.exec_()
