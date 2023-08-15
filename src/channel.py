from googleapiclient.discovery import build
import os
import json

class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('DZ_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        info = self.get_channel_data()
        self.title = info['snippet']['title']
        self.description = info['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = info['statistics']['subscriberCount']
        self.video_count = info['statistics']['videoCount']
        self.view_count = info['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def get_channel_data(self):
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        channel = channel['items'][0]
        return channel

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, new_file):
        with open (new_file, 'w') as file:
            json.dump(self.__dict__, file)
