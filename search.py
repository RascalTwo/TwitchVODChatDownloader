import os
import re
import sys
import json
try:
	import colorama
	colorama.init()
	HIGHLIGHT = colorama.Fore.BLACK + colorama.Back.WHITE
except:
	colorama = None
	HIGHLIGHT = ''

from shared import parse_twitch_timestamp


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('[VOD ID] [Query]')
		sys.exit(1)
	query = sys.argv[2].lower()

	with open(os.path.join('output', f'{sys.argv[1]}.json'), 'r') as f:
		messages = json.load(f)
	start = parse_twitch_timestamp(messages[0]['created_at'])

	pattern = '(' + re.escape(query) + ')'
	replacement: str = HIGHLIGHT + r'\1' + colorama.Style.RESET_ALL if colorama else ''  # type: ignore

	for message in messages:
		if query in message["message"]["body"].lower():
			body = message['message']['body']
			if colorama:
				body = re.sub(pattern, replacement, body, re.IGNORECASE)

			print(f'[{parse_twitch_timestamp(message["created_at"]) - start} {message["commenter"]["display_name"]}]: {body}')