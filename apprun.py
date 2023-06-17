from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QWidget
)
import sys
from ticketapp import Ui_MainWindow


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        con = QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName('data.db')
        try: con.open()
        except: sys.exit(1)

        self.modelB = QSqlTableModel(self)
        self.modelB.setTable("Book")
        self.modelB.EditStrategy.OnFieldChange
        self.modelB.setHeaderData(0, Qt.Orientation.Horizontal, "Пользователь")
        self.modelB.setHeaderData(1, Qt.Orientation.Horizontal, "Выступление")
        self.modelB.setHeaderData(2, Qt.Orientation.Horizontal, "Ряд")
        self.modelB.setHeaderData(3, Qt.Orientation.Horizontal, "Место")
        self.modelB.select()
        
        self.modelU = QSqlTableModel(self)
        self.modelU.setTable("Users")
        self.modelU.EditStrategy.OnFieldChange
        self.modelU.setHeaderData(0, Qt.Orientation.Horizontal, "Пользователь")
        self.modelU.setHeaderData(1, Qt.Orientation.Horizontal, "Никнейм")
        self.modelU.setHeaderData(2, Qt.Orientation.Horizontal, "Telegram-ID")
        self.modelU.setHeaderData(3, Qt.Orientation.Horizontal, "Имя")
        self.modelU.select()

        self.modelP = QSqlTableModel(self)
        self.modelP.setTable("Performance")
        self.modelP.EditStrategy.OnFieldChange
        self.modelP.setHeaderData(0, Qt.Orientation.Horizontal, "Выступление")
        self.modelP.setHeaderData(1, Qt.Orientation.Horizontal, "Название")
        self.modelP.setHeaderData(2, Qt.Orientation.Horizontal, "Дата")
        self.modelP.select()

        self.ui.viewB.setModel(self.modelB)
        self.ui.viewB.resizeColumnsToContents()

        self.ui.viewU.setModel(self.modelU)
        self.ui.viewB.resizeColumnsToContents()

        self.ui.viewP.setModel(self.modelP)
        self.ui.viewB.resizeColumnsToContents()
        

    def reset_click(self):
        print('+')
        


        
        
        
 
 
app = QApplication([])
application = mywindow()
application.show()
 
app.exec()
