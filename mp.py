#pip install PyQt5, pandas


import sys
from PyQt5.Qt import QVBoxLayout, QListWidget, QTableWidget, QWidget, Qt,QSlider,QPushButton,QHBoxLayout, QLabel, QMessageBox,QTableView
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
import pandas as pd

class TableModel(QtCore.QAbstractTableModel):# создание модели для работы с TableWidget
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])


class Window_2(QWidget):#Дочернее окно с результатом                           
    def __init__(self, parent):
        super().__init__()                        

        self.data = w.get_column_data()  

        self.setWindowTitle("Window_2")
        self.resize(250, 175)
        self.list= QListWidget()
        self.list.addItem(w.arg)
        self.tri =QLabel("Триугольный вид матрицы")
        self.cellinfo = QTableView()

        name=[]
        for i in range(w.columms-1):
            name.append(f"{i+1}x")
        name.append("y")

        
        data=pd.DataFrame(w.tri_data, columns = name)

        self.model = TableModel(data)
        self.cellinfo.horizontalHeader().setDefaultSectionSize(100)
        self.cellinfo.setModel(self.model)

        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setGeometry(300, 40, 300, 30)
        self.sld2.valueChanged[int].connect(self.changeValu2)
       
        self.setWindowTitle("Результат")

        self.zna =QLabel("Значение аргументов")

        layout2 = QVBoxLayout(self)
        layout2.addWidget(self.tri)
        layout2.addWidget(self.sld2)
        layout2.addWidget(self.cellinfo)
        layout2.addWidget(self.zna)
        layout2.addWidget(self.list)

    def changeValu2(self, value):
        self.cellinfo.horizontalHeader().setDefaultSectionSize(value*2)
        


                




class Table(QWidget):#Основной код
    def __init__(self):
        super(Table,self).__init__()
        self.rows = 2
        self.columms = 3
        self.w=400
        self.h=200
        self.refresh()
        self.setWindowTitle("линейниый калькуляторор")
        self.setWindowIcon(QtGui.QIcon('a.png'))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("a.png"),
        QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        self.show()

    def refresh(self): # Графические модули
        self.table = QTableWidget(self.rows, self.columms)
        name=[]
        for i in range(self.columms-1):
            name.append(f"{i+1}x")
        name.append("y")
        self.table.setHorizontalHeaderLabels(name)
        i=0

        for i in range(self.columms):
           self.table.horizontalHeaderItem(i).setTextAlignment(Qt.AlignRight)

        self.table.horizontalHeader().setDefaultSectionSize(100)

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setGeometry(300, 40, 300, 30)
        self.sld.valueChanged[int].connect(self.changeValue)
        
        self.addrows = QPushButton(
            "+arg")
        self.addrows.clicked.connect(self.add_rows)

        self.dellrows = QPushButton(
            "-arg")
        self.dellrows.clicked.connect(self.dell_rows)




        self.results = QPushButton("Расчитать")
        self.results.clicked.connect(self.create_window) 


        layout = QVBoxLayout(self)
        layout.addWidget(self.sld)
        layout.addWidget(self.table)
        choose = QHBoxLayout(self)
        choose.addWidget(self.addrows)
        choose.addWidget(self.dellrows)
        layout.addLayout(choose)
        layout.addWidget(self.results)

    def changeValue(self, value): # Функция для скрол бара
        self.table.horizontalHeader().setDefaultSectionSize(value*2)


    def add_rows(self): # Функция для добавление уравнение
        row = self.rows
        self.rows += 1
        colum = self.columms
        self.columms+=1
        self.table.insertRow(row)
        self.table.insertColumn(colum)
        self.rename()
 

    def dell_rows(self):# Функция для удаление уравнение
        if self.rows >2 :
            row = self.rows
            self.rows -=1
            colum = self.columms
            self.columms -= 1
            self.table.removeRow(row-1)
            self.table.removeColumn(colum-1)
            self.rename()



    def cheak_empty(self): # Проверка на пустоту
        process = True
        self.cord_empty = []
        for y in range(self.columms):
            for x in range(self.rows):
                if self.table.item(x, y) == None:
                    process = False
                    self.cord_empty.append([y+1,x+1])
        return process

    def create_window(self): # Несколько проверок и сама реализация Метода Гаусса
        try:
            if self.cheak_empty():
                self.data = self.get_column_data()
                matrix_a =[]
                matrix_b=[]

                for y in range(w.rows):
                    a0=[]
                    for x in range(w.columms-1):
                        a0.append(float(self.data[x][y]))
                    matrix_a.append(a0)
                    matrix_b.append(float(self.data[len(a0)][y]))


                    # преобразование матрицы к треуголному ввиду
 
                def gauss_(aa,bb):
                    n=len(aa)
                    sgn=1
                    for r in range(n): # r - номер опорной строки
                        z=aa[r][r]     # опорный элемент
                        # перебор всех строк, расположенных ниже r
                        if abs(z)<1.0e-10: # ноль на диагонали
                            # ищем ненулевой элемент ниже 
                            for j in range(r+1,n):
                                if abs(aa[j][r])>1.0e-10:
                                    for jj in range(r,n):
                                        aa[j][jj],aa[r][jj]=aa[r][jj],aa[j][jj]
                                bb[j],bb[r]=bb[r],bb[j]       
                                z=aa[r][r]
                                sgn=-sgn
                                break
                            else:
                                return None
                        for i in range(r+1,n):
                            q=aa[i][r]/z
                            for j in range(n):
                                aa[i][j]=aa[i][j]-aa[r][j]*q
                            bb[i]=bb[i]-bb[r]*q
                    return(aa,bb,sgn)
 
                # вычисление главного аргумента
 
                def det_tri(a,sgn=1):
                    n=len(a)
                    p=sgn
                    for i in range(n):
                        p=p*a[i][i]
                    return p    
 
                # вычисление значение аргументов
 
                def rev_calc(a,b):
                    n=len(b)
                    res=[0 for _ in range(n)]
                    i=n-1
                    res[i]=b[i]/a[i][i]
                    i=i-1
                    while(i>=0):
                        s=b[i]
                        for j in range(i+1,n):
                            s=s-a[i][j]*res[j]
                        res[i]=s/a[i][i]
                        i=i-1
                    return res    
 
 
 
                res=gauss_(matrix_a, matrix_b) 
 
                if res is None:
                    Window_2.close
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Critical)
                    msgBox.setText(f"Нет решений")
                    msgBox.setWindowTitle("ERROR")
                    msgBox.setStandardButtons(QMessageBox.Ok)

                    x=msgBox.exec_()
                else:
                    self.tri_data=[]
                    self.arg=''
                    for i in range(self.columms-1):
                        adata=[]
                        for f in range(self.rows):
                            adata.append(res[0][i][f])
                        adata.append(res[1][i])
                        self.tri_data.append(adata)
                        self.arg+=f"{i+1}x={round(rev_calc(res[0],res[1])[i] , 4)}\n"
                    self.window = Window_2(self)                        # !!! self
                    self.window.resize(400,400)
                    self.window.show()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(f"Ячейки не заполенны с кординатами:{self.cord_empty}")
                msgBox.setWindowTitle("ERROR")
                msgBox.setStandardButtons(QMessageBox.Ok)

                x=msgBox.exec_() 

        except ValueError as e:

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(f"Введен неправильный тип переменных")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)

            x=msgBox.exec_()   

        except ZeroDivisionError as e:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(f"Неправильная матрица")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)

            x=msgBox.exec_() 
            

                

 





    def get_column_data(self):   #Получение данных с начальной таблицы
        rows = self.table.rowCount()         
        columns = self.table.columnCount()  
         
        data = [ 
                   [self.table.item(row, column).text()
                       for row in range(rows)
                       if self.table.item(row, column) is not None
                   ] 
                   for column in range(columns)
               ]
               
        return data



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Table()
    w.resize(400, 250)
    w.show()
    sys.exit(app.exec_())