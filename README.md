# Pocket-To-Pinboard
Script takes url, description and tags from Pocket and syncs them to Pinboard. Currently no configuration options for what gets synced as it's a work in progress.
<br>
<br>
You'll need to hard code or set environment variables for:
```
POCKET_CONSUMER_KEY
POCKET_ACCESS_TOKEN
PINBOARD_USERNAME
PINBOARD_API_TOKEN
```
Currently the only external dependency is Requests - http://docs.python-requests.org/en/latest/