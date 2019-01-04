#Binding PySide para interface grafica com o Qt 4.8
#Codigo de licensa GPL
#Mod. Vitor Sgobbi 2014
#Install 'python-qt4' library before using 
import sys, os.path
import gobject
#imports do Qt
from PyQt4 import QtGui, QtCore
from PySide.QtCore import Signal, Qt, SIGNAL
from PySide.QtGui import QApplication, QWidget, QMainWindow, QVBoxLayout
from PySide.QtGui import QLabel, QPushButton, QCheckBox, QIcon, QAction
from PySide.QtGui import QFrame
from PySide.QtGui import QPalette

class UI(gobject.GObject):
    __gsignals__ = {
        'command': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
    }

    def __init__(self, args, continuous):
        self.continuous = continuous
        gobject.GObject.__init__(self)
        #incicio de sempre :D
        self.app = QApplication(args)
        #QMainWindow
        self.window = QtGui.QMainWindow()
        #nome e icone da janela
        self.window.setWindowTitle("Pomeu Qt")
	self.app_icon=QtGui.QIcon()
	self.app_icon.addFile('icon16.png', QtCore.QSize(16,16))
	self.app_icon.addFile('icon32.png', QtCore.QSize(32,32))
	self.app_icon.addFile('icon64.png', QtCore.QSize(64,64))
        #self.window.setWindowIcon(app_icon)
	path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), '/home/vitao/icon.png')
	self.window.setWindowIcon(QtGui.QIcon("icon64.ico"))
	
        #tamanho maximo da janela
	self.window.setGeometry(410,230,250,150)
        self.window.setMaximumSize(410, 230)
        center = QtGui.QWidget()
        self.window.setCentralWidget(center)
        #adicionar outro label de img como icone:
        #self.label = QLabel()
        #layout.addWidget(set_icon())

        layout = QtGui.QVBoxLayout()
        center.setLayout(layout)

        #adicionando um frame com imagem
        #QFrame.__init__(self)
        #palette=QPalette()
        #pixma
        #botao escutar/parar
        self.lsbutton = QtGui.QPushButton("Escutar")
        layout.addWidget(self.lsbutton)
        #botao de modo continuo
        self.ccheckbox = QtGui.QCheckBox("Modo continuo")
        layout.addWidget(self.ccheckbox)

        #conectar "signal and slots"
        self.lsbutton.clicked.connect(self.lsbutton_clicked)
        self.ccheckbox.clicked.connect(self.ccheckbox_clicked)
        #self.lsbutton.clicked(self.lsbutton.clicked())
        #self.ccheckbox.clicked(self.lsbutton.clicked())
        #add label para mostrar o ultimo comando
        self.label = QtGui.QLabel()
        layout.addWidget(self.label)

        #atalho para sair do programa
        quit_action = QtGui.QAction(self.window)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.accel_quit)
        self.window.addAction(quit_action)


    def accel_quit(self):
        #se sair, emitir mensagem
        self.emit("commando", "Sair")

    #checkbox de modo continuo


    def ccheckbox_clicked(self):
        checked = self.ccheckbox.isChecked()
        if checked:
            #Mostrar botao desabilitado
            self.lsbutton.setEnabled(False)
            self.lsbutton_stopped()
            self.emit('command', "Escutando continuamente")
            self.set_icon_active()
        else:
            self.lsbutton.setEnabled(True)
            self.emit('command', "Modo continuo pausado")
            self.set_icon_inactive()


    def lsbutton_stopped(self):
        self.lsbutton.setText("Escutar...")


    def lsbutton_clicked(self):
        val = self.lsbutton.text()
        if val == "Escutar...":
            self.emit("command", "Escutando...")
            self.lsbutton.setText("Pausar")
            #clear the label
            self.label.setText("")
            self.set_icon_active()
        else:
            self.lsbutton_stopped()
            self.emit("command", "Pausado")
            self.set_icon_inactive()


    def run(self):
        self.set_icon_inactive()
	self.window.setWindowIcon(QtGui.QIcon('icon64.png'))
        self.window.show()
        if self.continuous:
            self.set_icon_active()
            #self.ccheckbox.setCheckState(Qt.Checked)
	    self.ccheckbox.checkState()==Qt.Checked
            self.ccheckbox_clicked()
        self.app.exec_()
        self.emit("command", "Sair")

    def finished(self, text):
        print text
        if not self.ccheckbox.isChecked():
            self.lsbutton_stopped()
        self.label.setText(text)


    def set_icon(self, icon):
	icon = self.app_icon
        self.window.setWindowIcon(QtGui.QIcon('icon64.png'))


    def set_icon_active_asset(self, i):
        self.icon_active = i


    def set_icon_inactive_asset(self, i):
        self.icon_inactive = i


    def set_icon_active(self):
        self.window.setWindowIcon(QtGui.QIcon(self.icon_active))


    def set_icon_inactive(self):
        self.window.setWindowIcon(QtGui.QIcon(self.icon_inactive))
