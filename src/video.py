from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('DZ_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id
        info = self.get_channel_data()
        self.title = info['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}' #не знаю как определить начало ссылки. эта ссылка работает через watch?v=. почему и как узнать?
        self.number_views = info['statistics']['viewCount']
        self.number_likes = info['statistics']['likeCount']
        self.playlist_id = info['statistics']

    def get_channel_data(self):
        channel = self.youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
        channel = channel['items'][0]
        return channel

    def __str__(self):
        return self.title

class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        #youtube = self.youtube
        self.playlist_Id = playlist_id


    def get_playlist(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        return playlist_videos

    def __str__(self):
        return self.title

