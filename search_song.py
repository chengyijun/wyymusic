import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication


class SearchSong(QThread):
    searched = pyqtSignal([list], [str])

    def __init__(self, keyword, parent=None):
        """
        :param keyword: 查询条件
        :param parent:
        """
        super(SearchSong, self).__init__(parent)
        self.keyword = keyword

    def search(self):
        api_url = 'http://music.163.com/api/search/pc'
        data_dict = {
            's': self.keyword,
            'offset': 0,
            'limit': 10,
            'type': 1
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.394\
            5.88 Safari/537.36'
        }
        try:
            res = requests.post(url=api_url, data=data_dict, headers=headers, timeout=10)
        except Exception as e:
            self.searched[str].emit('网络不畅，请稍候再试吧...')
            return
        songs_origin = res.json()['result']['songs']
        # print(songs_origin)
        songs = []
        for song in songs_origin:
            song = {
                'song_id': song['id'],
                'song_name': song['name'],
                'artist': song['artists'][0]['name'],
                'album': song['album']['name']
            }
            songs.append(song)

        self.searched[list].emit(songs)

    def run(self):
        self.search()


def main():
    import sys
    app = QApplication(sys.argv)

    search_song = SearchSong('周传雄')
    search_song.searched.connect(lambda songs: print(songs))
    search_song.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
