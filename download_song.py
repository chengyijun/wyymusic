import re

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication


class DownloadSong(QThread):
    downloaded = pyqtSignal([str])

    def __init__(self, song, parent=None):
        """
        :param song_id: 歌曲id
        :param parent:
        """
        super(DownloadSong, self).__init__(parent)
        self.song = song

    def download(self):
        song_id = self.song['song_id']
        song_name = self.song['song_name']
        artist = self.song['artist']
        album = self.song['album']
        file_name = f'{song_name}-{artist}-{album}'
        file_name = self.get_safe_file_name(file_name)
        api_url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.394\
            5.88 Safari/537.36'
        }
        try:
            res = requests.get(url=api_url, headers=headers, timeout=10)
        except Exception as e:
            self.downloaded[str].emit('网络不畅，请稍候再试吧...')
            return
        with open(f'./{file_name}.mp3', 'wb') as f:
            f.write(res.content)

        self.downloaded[str].emit(f'{file_name} 下载完毕')

    @staticmethod
    def get_safe_file_name(title):
        """
        过滤文件名中的非法字符 在[]中*不需要转义,此时*不表示多次匹配,就表示本身的字符
        :param title:
        :return:
        """
        return re.sub(r'[\\/:*?"<>|\r\n]+', "_", title)  # 替换为下划线

    def run(self):
        self.download()


def main():
    import sys
    app = QApplication(sys.argv)

    download_song = DownloadSong('190072')
    download_song.downloaded.connect(lambda songs: print(songs))
    download_song.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
