import os
import sys
import json

from .shared import parse_twitch_timestamp


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('[VOD ID] [Query]')
		sys.exit(1)
	query = sys.argv[2].lower()

	with open(os.path.join('output', f'{sys.argv[1]}.json'), 'r') as f:
		messages = json.load(f)
	start = parse_twitch_timestamp(messages[0]['created_at'])
	for message in messages:
		if query in message["message"]["body"].lower():
			print(f'[{parse_twitch_timestamp(message["created_at"]) - start} {message["commenter"]["display_name"]}]: {message["message"]["body"]}')