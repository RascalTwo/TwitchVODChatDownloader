# Twitch VOD Chat Downloader

Yet another Twitch Chat downloader, it does exactly what it says in the title: it downloads Twitch chat.

It *only* has been tested on Twitch VODs, use on a actually live stream at your own risk.

## Installation

Install the `requests` dependency

> If you wish to have terminal highlighting when using `search.py`, also install `colorama`

## Downloading

```shell
python3 [VOD ID] [Client ID]
```

- `VOD ID`
  - ID of Twitch VOD chat to download
- `Client ID`
  - The ID of the application to make requests with, every request - even browsers - must use this, you can obtain one from Twitch itself

It will cache the results as it downloads within the `cache` directory, and finally when finished will output the JSON at `output/[VOD ID].json`.

## Searching

In addition exists a script for simple searching through the generated JSON file.

```shell
python3 search.py [VOD ID] [Query]
```

It will output the offset time, author, and message of all messages that contain the `Query`

> If `colorama` is installed, the query within outputted messages will be highlighted

### Messages

The message objects are formatted as such:

```json
{
  "_id": "uuid4",
  "created_at": "isodate",
  "updated_at": "isodate",
  "channel_id": "00000000",
  "content_type": "video",
  "content_id": "0000000000",
  "content_offset_seconds": 0.278,
  "commenter": {
    "display_name": "display_name",
    "_id": "000000000",
    "name": "display_name",
    "type": "user",
    "bio": "vio",
    "created_at": "isodate",
    "updated_at": "isodate",
    "logo": "url"
  },
  "source": "chat",
  "state": "published",
  "message": {
    "body": "body",
    "fragments": [],
    "is_action": false,
    "user_badges": [],
    "user_color": "#ffffff",
    "user_notice_params": {}
  }
}
```
