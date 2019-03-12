import folium,os,time
from math import cos, asin, sqrt
from warshall import main # import the algorithm result
from PyQt5 import QtCore, QtWidgets
import folium
from folium import plugins
from folium.plugins import MeasureControl
from PyQt5.QtWidgets import QFileDialog









from geopy.geocoders import Nominatim
from geopy.distance import great_circle
geolacator = Nominatim(user_agent="Hacettepe_Geomatik")


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin...


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 314)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 26))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuSettings.addAction(self.actionHelp)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.pushButton.clicked.connect(self.tamam)
        self.pushButton_2.clicked.connect(self.txt_ac)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Nereye:"))
        self.label.setText(_translate("MainWindow", "Nerden:"))
        self.pushButton.setText(_translate("MainWindow", "Tamam"))
        self.pushButton_2.setText(_translate("MainWindow", "TXT Dosyası"))
        self.menuSettings.setTitle(_translate("MainWindow", "Yardım"))
        self.actionHelp.setText(_translate("MainWindow", "Yardım"))


    def combo(self):
        for i in self.airport_name:
            self.comboBox.addItem(i)
            self.comboBox_2.addItem(i)

    def txt_ac(self):

        self.fname = QFileDialog.getOpenFileName()

        f = open("%s" % (self.fname[0]), "r")

        print("la buraya bak",self.fname[0])

        self.data = []
        for i in f.readlines():
            self.data.append(i.split(","))
        for i in range(len(self.data)):
            self.data[i][0] = str(i +1)

        print(self.data)
        lati = list()
        longi = list()
        self.airport_name = list()
        coor = dict()
        for i in range(len(self.data)):
            lati.append(self.data[i][6])
            longi.append(self.data[i][7])
            self.airport_name.append(self.data[i][1])
            coor[self.data[i][1]] = [self.data[i][7], self.data[i][6]]

        self.combo()
    def __str__(self):
        return self.fname

    def tamam(self):

        self.nereden = self.comboBox.currentText()
        index1 = self.airport_name.index(self.nereden)

        self.nereye = self.comboBox_2.currentText()
        index2 = self.airport_name.index(self.nereye)


        if self.nereden == self.nereye:
            msg = QtWidgets.QMessageBox()
            msg.setText("Aynı havalimanını seçemezsiniz\nProgram kendini imha edicek")
            msg.setWindowTitle("Uyarı")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.exec_()

        m = folium.Map(location=[38, 31], control_scale=True, zoom_start=6)
        m.add_child(folium.LatLngPopup())#Tüm koordinatlar


        folium.raster_layers.TileLayer(  # Farklı tür harita desenleri
            tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr='google',
            name='google maps',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True,
        ).add_to(m)
        folium.raster_layers.TileLayer(
            tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr='google',
            name='google street view',
            max_zoom=20,
            subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
            overlay=False,
            control=True,
        ).add_to(m)
        folium.LayerControl().add_to(m)
        m.add_child(MeasureControl())  # Mesafe ve Alan ölçer

        start = int(self.data[index1][0])
        end = int(self.data[index2][0])
        list_for_sketch = main(self.fname[0])
        for i in range(len(list_for_sketch)):
            if [start, end] == list_for_sketch[i][0]:
                path = list_for_sketch[i][1]

        coor = list()
        for j in path:
            for i in range(len(self.data)):
                if j == int(self.data[i][0]):
                    a = float(self.data[i][6])
                    b = float(self.data[i][7])
                    coor.append([a, b])

        lines = list()
        for i in range(len(path) - 1):
            lines = lines + (
            [{'coordinates': [[coor[i][1], coor[i][0]], [coor[i + 1][1], coor[i + 1][0]], ], 'color': 'green'}])

        features = [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': line['coordinates'],
                },
                'properties': {

                    'style': {
                        'color': line['color'],
                        'weight': line['weight'] if 'weight' in line else 5
                    }
                }
            }
            for line in lines
        ]

        plugins.TimestampedGeoJson({
            'type': 'FeatureCollection',
            'features': features,
        }, period='PT1M', add_last_point=True).add_to(m)




        self.label_3.setText("Yönlendiriliyorsunuz...")
        m.save('shortest_route_map.html')
        time.sleep(2)
        os.startfile('shortest_route_map.html')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
