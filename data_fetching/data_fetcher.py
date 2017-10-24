import json
import os.path
import urlparse
from youtube_downloader import downloader
import configurations

#  Fetches comments from Youtube.
#  If comments are already fetched, they are stored in comments.json file,
#  read the comments from file.


class YoutubeCommentsDataFetcher(object):
    def __init__(self, url):
        self.VIDEO_URL = url
        url_data = urlparse.urlparse(self.VIDEO_URL)
        query = urlparse.parse_qs(url_data.query)
        videoid = query["v"][0]
        self.COMMENTS_FILE_PATH = configurations.PROJECT_ROOT + '/comments_file/comments_' + videoid + '.json'
        print "[YoutubeCommentsDataFetcher] Fetching comments for: " + self.VIDEO_URL + " and writing to: " + self.COMMENTS_FILE_PATH
        if not self.is_comments_file_available():
            downloader.fetch_comments_from_youtube(self.VIDEO_URL, self.COMMENTS_FILE_PATH)

    def is_comments_file_available(self):
        return os.path.exists(self.COMMENTS_FILE_PATH)

    def read_comments_json_from_file(self):
        with open(self.COMMENTS_FILE_PATH) as comments_file:
            json_data = json.load(comments_file)
        return json_data

    def get_comments(self):
        if self.is_comments_file_available():
            print "[get_comments] Comments already downloaded for this video. Reading from file."
            return self.read_comments_json_from_file()
        else:
            print "[get_comments] Comments for " + self.VIDEO_URL +" not downloaded yet. Downloading and creating json file."
            downloader.fetch_comments_from_youtube(self.VIDEO_URL, self.COMMENTS_FILE_PATH)
            return self.read_comments_json_from_file()