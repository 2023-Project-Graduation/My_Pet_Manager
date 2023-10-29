import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
import threading
import time
import sounddevice
from scipy.io.wavfile import write
from scipy.io.wavfile import read


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("./GUI/appGUI.ui")[0]
form_doginfo_class = uic.loadUiType("./GUI/DogInfoGUI.ui")[0]
form_record_class = uic.loadUiType("./GUI/recordGUI.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.showMaximized()

        self.OnAir.clicked.connect(self.OnAirFunction)
        self.DogInfo.clicked.connect(self.DogInfoFunction)
        self.Record.clicked.connect(self.RecordFunction)
        self.Exit.clicked.connect(self.ExitFunction)


    def OnAirFunction(self):
        self.hide()
        th = threading.Thread(exec(open("./main.py",encoding='UTF8').read()))
        self.show()


    def DogInfoFunction(self):
        self.hide()
        self.Doginfo = DogInfoClass()
        self.Doginfo.exec()
        self.show()

    def RecordFunction(self):
        self.hide()
        self.Record = RecordClass()
        self.Record.exec()
        self.show()


    def ExitFunction(self):
        exit(0)

        
class DogInfoClass(QDialog,form_doginfo_class):
    def __init__(self):
        super(DogInfoClass,self).__init__()
        self.setupUi(self)
        self.showMaximized()

        breed_data_list = self.DogInfoListFunction()
        total_amount = (int)(breed_data_list[1])+(int)(breed_data_list[2])+(int)(breed_data_list[3])

        self.label0.setText(f'종 이름:{breed_data_list[0]}')
        self.label1.setText(f'A 사료 추천량: {breed_data_list[1]}g')
        self.label2.setText(f'B 사료 추천량: {breed_data_list[2]}g')
        self.label3.setText(f'C 사료 추천량: {breed_data_list[3]}g')
        self.label4.setText(f'총 사료량: {total_amount}g')
        self.label5.setText(f'단백질 비율: {breed_data_list[4]}')
        self.label6.setText(f'지방 비율: {breed_data_list[5]}')
        self.label7.setText(f'칼로리 총량: {breed_data_list[6]}kcal')


        self.Exit.clicked.connect(self.returnMainFuncion)


    def DogInfoListFunction(self):
        f = open('./breed_data.txt','r')
        breed_data_list = []
        for i in range(7):
            breed_data_list.append(f.readline().rstrip('\n'))
        f.close()
        return breed_data_list    
        


    def returnMainFuncion(self):
        self.close()



class RecordClass(QDialog,form_record_class):
    seconds = 5
    file = 'dogcall.wav'
    
    def __init__(self):
        super(RecordClass,self).__init__()
        self.setupUi(self)
        self.showMaximized()

        self.record.clicked.connect(self.recordFunction)
        self.play.clicked.connect(self.playFunction)
        self.Exit.clicked.connect(self.returnMainFuncion)

    def recordFunction(self):
        self.record.setText('녹음중')
        self.repaint()
        self.voice_recorder()
        self.record.setText('녹음')

    def playFunction(self):
        self.play.setText('재생중')
        self.repaint()
        self.voice_player()
        self.play.setText('재생')
        

    def voice_recorder(self):
        print("Recording Started")
        recording = sounddevice.rec((self.seconds * 44100), samplerate= 44100, channels=1)
        sounddevice.wait()
        write(self.file, 44100, recording)
        print("Recording Finished")
        

    def voice_player(self):
        print('Playing Started')
        rate, audio_data = read(self.file)
        print(rate,audio_data)
        sounddevice.play(audio_data,rate)
        sounddevice.wait()
        print('Playing Finished')


    def returnMainFuncion(self):
        self.close()



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()