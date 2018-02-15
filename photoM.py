import sys, os
from PIL import Image
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from contants import *

class Form(QtWidgets.QDialog):
    setResultTextSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.myui = uic.loadUi("photoUI.ui", self)
        self.setResultTextSignal.connect(self.setResultText)
        self.baseListView.doubleClicked.connect(self.baseItemSelected)
        self.cmpListView.doubleClicked.connect(self.cmpItemSelected)
        self.myui.show()

    def baseLoadBtnClicked(self):
        baseDir = QtWidgets.QFileDialog.getExistingDirectory(self,"Select base file path","./")
        self.basePath.setText(baseDir)
        self.baseListView.setModel(self.addAllFilesToList(baseDir))
        self.setResultTextSignal.emit(NOTIFY_LOAD_SUCCESS)

    def cmpLoadBtnClicked(self):
        cmpDir = QtWidgets.QFileDialog.getExistingDirectory(self,"Select compare file path","./")
        self.comparePath.setText(cmpDir)
        self.cmpListView.setModel(self.addAllFilesToList(cmpDir))
        self.setResultTextSignal.emit(NOTIFY_LOAD_SUCCESS)

    def cmpBtnClicked(self):
        # TBD : ListView에 있는 list를 가져와서 비교하는걸로 바꾸기.
        print("cmpBtnClicked()")
        sameList = []
        basePath = self.basePath.text().strip()
        cmpPath = self.comparePath.text().strip()
        baseFileList = os.listdir(basePath)
        cmpFileList = os.listdir(cmpPath)
        for bf in baseFileList:
            try:
                baseImg = Image.open(basePath+'/'+bf)
                for cf in cmpFileList:
                    if basePath != cmpPath:
                        try:
                            cmpImg = Image.open(cmpPath+'/'+cf)
                            if baseImg == cmpImg:
                                print("same ",basePath+'/'+bf, cmpPath+'/'+cf)
                                sameList.append(cmpPath+'/'+cf)
                        except Exception as e:
                            #print('*** Caught exception: %s: %s' % (e.__class__, e))
                            continue
            except Exception as e:
                #print('*** Caught exception: %s: %s' % (e.__class__, e))
                continue
        self.setResultTextSignal.emit(NOTIFY_COMPARE_SUCCESS)
        print("Same List : ",sameList)
        # TBD : sameList에 있는 list들을 cmpList에서 background 색 변경해주기

    def setResultText(self, str):
        self.resultText.setText(str)

    def baseItemSelected(self):
        # QListView에서는 selectedIndexes()로 현재 선택된 list들을 가져올 수 있다.
        # 그결과 list의 row()로 row 번호, data()로 list 값을 가져올 수 있다.
        imgPath = str(self.basePath.text().strip() + self.baseListView.selectedIndexes()[0].data().strip()).strip()
        #img = Image.open(imgPath)
        # 이미지를 Label에 출력하려면 QPixmap을 사용해야한다.
        imgLabel = QPixmap(imgPath)
        imgLabel = imgLabel.scaledToHeight(self.baseImgView.height())
        self.baseImgView.setPixmap(imgLabel)

    def cmpItemSelected(self):
        imgPath = str(self.comparePath.text().strip() + self.cmpListView.selectedIndexes()[0].data().strip()).strip()
        imgLabel = QPixmap(imgPath)
        imgLabel = imgLabel.scaledToHeight(self.cmpImgView.height())
        self.cmpImgView.setPixmap(imgLabel)

    def addAllFilesToList(self, path):
        if os.path.exists(path):
            model = QStandardItemModel()
            fileList = []
            self.loadAllFiles(path, fileList, 1, '')
            for fName in fileList:
                item = QStandardItem(fName)
                item.setEditable(False)
                model.appendRow(item)
            return model
        return None

    def loadAllFiles(self, path, files, emptyVol, parent):
        try:
            if os.path.exists(path):
                fileList = os.listdir(path)
                for f in fileList:
                    filePath = path+"/"+f
                    if os.path.isdir(filePath):
                        # 현재 file이 directory인 경우 list에 추가하고 재귀호출을 한다.
                        # 이 때, 현재 파일이 directory 하위임을 표시하기 위해 emptyVol에 1을 더해주고 현재 폴더 이름을 전달한다.
                        # emptyVol은 들여쓰기 단계를 표기하기 위해 존재한다.
                        files.append(str(emptyVol*" ")+"/"+f)
                        self.loadAllFiles(filePath, files, emptyVol+1, parent+'/'+f)
                    elif os.path.isfile(filePath):
                        files.append(str(emptyVol*" ")+" /"+parent+'/'+f)
                    else:
                        continue
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            self.setResultTextSignal.emit('%s: %s' % (e.__class__, e))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())