from googleapiclient.discovery import build
import os
from src.video import PLVideo, Video
import datetime
import isodate

class PlayList:
    api_key: str = os.getenv('DZ_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_video = self.youtube.playlists().list(id=self.playlist_id,
                                                        part='snippet'
                                                        ).execute()
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.title = playlist_video['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

    @property
    def total_duration(self):
        '''возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста'''
        count_time = []
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            durations = isodate.parse_duration(iso_8601_duration)
            count_time.append(durations)
        duration = sum(count_time, datetime.timedelta())
        return duration

    def show_best_video(self):
        '''Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков) '''
        best_video = None
        max_likes = 0

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > max_likes:
                max_likes = int(video['statistics']['likeCount'])
                best_video = f'https://youtu.be/{video["id"]}'

        return best_video


#pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
#for video in pl.video_response['items']:
#    print(video)
