import requests
import os
import json
from pprint import pprint
from datetime import datetime

POCKET_CONSUMER_KEY = os.environ['POCKET_CONSUMER_KEY']
POCKET_ACCESS_TOKEN = os.environ['POCKET_ACCESS_TOKEN']
PINBOARD_USERNAME = os.environ['PINBOARD_USERNAME']
PINBOARD_API_TOKEN = os.environ['PINBOARD_API_TOKEN']

class PocketPinboard:
    def get_pocket_items(self, time=1):
        '''Gets items from pocket, returns a list of '''
        r = requests.get("https://getpocket.com/v3/get", 
                        params={'consumer_key' : POCKET_CONSUMER_KEY, 
                                'access_token' : POCKET_ACCESS_TOKEN, 
                                'since' : time,
                                'sort' : 'newest',
                                'detailType' : 'complete',
                                'state' : 'all'})
        url_tag_list = []
        pocket_items = r.json()
        if len(pocket_items['list']) > 0:
            for key, value in pocket_items['list'].iteritems():
                if all(k in value.keys() for k in ('resolved_url', 'resolved_title', 'excerpt')):
                    item = {'url' : value['resolved_url'],
                            'title' : value['resolved_title'],
                            'excerpt' : value['excerpt'],
                            'tags' : []}
                    if 'tags' in value.keys():
                        item['tags'] = [tag for tag in value['tags']]
                    url_tag_list.append(item)
        return url_tag_list

    def post_items_to_pinboard(self):
        time = self.get_last_update()
        items = self.get_pocket_items(time=time)
        for item in items:
            tags = [t.replace(" ", "_") for t in item['tags']]
            r = requests.get('https://api.pinboard.in/v1/posts/add?auth_token={}'.format(PINBOARD_API_TOKEN),
                            params={'url' : item['url'],
                                    'description' : item['title'],
                                    'extended' : item['excerpt'],
                                    'tags' : ', '.join(tags)})
            print r.url
            print r.text
        self.update_timestamp()

    def update_timestamp(self):
        current_time = int((datetime.now() - datetime.utcfromtimestamp(0)).total_seconds())
        with open("timestamp.txt", "w") as stamp_file:
            stamp_file.write("{}".format(current_time))

    def get_last_update(self):
        with open("timestamp.txt") as stamp_file:
            content = stamp_file.readlines()
        return int(content[0])

    def run(self):
        self.post_items_to_pinboard()

if __name__ == '__main__':
    p = PocketPinboard()
    p.run()