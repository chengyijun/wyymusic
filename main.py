# import fix_qt_import_error  # 解决打包报错问题 必须在pyqt5之前导入
from PyQt5.Qt import *
from download_song import DownloadSong
from search_song import SearchSong
from wyy import Ui_MainWindow
from about import Ui_Dialog


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 窗口位置
        self.move(600, 200)
        # 窗口大小
        self.resize(400, 400)
        # 窗口透明度
        # self.setWindowOpacity(0.9)
        # 导入qt designer设计的布局样式
        self.setupUi(self)
        # 自定义布局样式
        self.setup_ui()

    def paintEvent(self, event):
        """
        设置主窗口背景图片
        :param event:
        :return:
        """
        painter = QPainter(self)
        # todo 1 设置背景颜色
        painter.setBrush(Qt.green)
        painter.drawRect(self.rect())

        # #todo 2 设置背景图片，平铺到整个窗口，随着窗口改变而改变
        pixmap = QPixmap("./main_bg.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    def setup_ui(self):
        # 设置关于我们弹窗的信号与槽
        self.actionabout_us.triggered.connect(self.show_about_widget)
        # 设置表格 单元格宽度自动适应
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        keyword = self.lineEdit.text()
        # 开始查询歌曲 利用查询结果 填充表格
        if not keyword:
            return
        self.search_song = SearchSong(keyword)
        self.search_song.searched[list].connect(self.fill_table)
        self.search_song.searched[str].connect(self.show_searched_exception)
        self.search_song.start()

    def show_searched_exception(self, searched_exception):
        self.textBrowser.append(searched_exception)

    def download_the_song(self, i):
        # print(f'下载第{i+1}首歌曲，歌曲信息为{self.songs[i]}')
        self.textBrowser.append(f'正在下载第{i+1}首歌曲...')
        song = self.songs[i]

        self.download_song = DownloadSong(song)
        self.download_song.downloaded.connect(self.show_download_info)
        self.download_song.start()

    def show_download_info(self, info):
        # print(info)
        self.textBrowser.append(info)

    def download_btn(self, i):
        wg = QWidget()
        btn = QPushButton('下载')
        btn.setObjectName('btn')
        btn.setStyleSheet("#btn{\n"
                          "color:white;\n"
                          "border-color:white;\n"
                          "background:transparent;\n"
                          "}")
        btn.setMinimumHeight(20)
        btn.clicked.connect(lambda: self.download_the_song(i))
        hbl = QHBoxLayout()
        hbl.addWidget(btn)
        hbl.setContentsMargins(0, 0, 0, 0)
        wg.setLayout(hbl)
        return wg

    def fill_table(self, songs):
        """
        填充表格
        :param songs: 与该槽函数对应的信号发射的数据，也就是歌曲列表
        :return:
        """
        # print(songs)
        # print('填充表格')
        # 保存一份songs数据到主窗体对象中 以便后面方便使用

        self.songs = songs
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(len(songs))
        for index, song in enumerate(songs):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(song['song_name']))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(song['artist']))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(song['album']))
            self.tableWidget.setCellWidget(index, 3, self.download_btn(index))

    def show_about_widget(self):
        self.ui_about = Ui_Dialog()
        self.about_win = QDialog()
        self.ui_about.setupUi(self.about_win)
        self.about_win.setWindowTitle('关于我们')
        self.about_win.show()


def main():
    import sys
    app = QApplication(sys.argv)
    my_window = MyWindow()
    # 窗口标题
    my_window.setWindowTitle('Abel的音乐下载器')
    # 窗口图标
    my_window.setWindowIcon(QIcon(':/ico/icon.ico'))
    my_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
