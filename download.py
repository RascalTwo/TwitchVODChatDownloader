import os
import json
import time
import sys

import requests

from typing import Any, List, Optional

from shared import follow_cursors, parse_twitch_timestamp



def collect_chunks(vid: int, client_id: str):
	print(f'Collecting {vid}...')
	headers = {'Client-Id': client_id}

	count, start, last = 0, None, None
	def cache_or_fetch(cursor: Optional[str]) -> Optional[str]:
		nonlocal count, start, last
		path = os.path.join('cache', f'{vid}_{cursor or 0}.json')
		if os.path.exists(path):
			with open(path, 'r') as f:
				response = json.load(f)
		else:
			url = f'https://api.twitch.tv/v5/videos/{vid}/comments?cursor={cursor}' if cursor else f'https://api.twitch.tv/v5/videos/{vid}/comments?content_offset_seconds=0'
			response = requests.get(url, headers=headers).json()
			with open(path, 'w') as f:
				json.dump(response, f)
			time.sleep(2.5)

		comments = response.get('comments', [])
		if comments:
			if start is None:
				start = comments[0]['created_at']
			last = comments[-1]['created_at']
			count += len(comments)
			print(str(parse_twitch_timestamp(last) - parse_twitch_timestamp(start)).ljust(20, ' ') + '\r', end='', flush=True)

		return response.get('_next', None)

	follow_cursors(cache_or_fetch)
	print()
	print(start, '->', last, '=', count, 'messages')


def merge_chunks(vid: int):
	print(f'Merging {vid}...')
	with open(os.path.join('output', f'{vid}.json'), 'w') as f:
		f.write('[')

		def write_comments(comments: List[Any], has_more: bool):
			if not comments:
				return
			for comment in comments[:-1]:
				f.write('  ' + json.dumps([comment], indent='  ')[1:-1].rstrip() + ',')
			f.write('  ' + json.dumps([comments[-1]], indent='  ')[1:-1].rstrip() + (',' if has_more else ''))

		def collect_comments(cursor: Optional[str]) -> Optional[str]:
			with open(os.path.join('cache', f'{vid}_{cursor or 0}.json'), 'r') as f:
				response = json.load(f)

			cursor = response.get('_next', None)
			write_comments(response.get('comments', []), bool(cursor))

			return cursor

		follow_cursors(collect_comments)
		f.write('\n]')
	print('Merged')


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('[VOD ID] [Client Id]')
		sys.exit(1)

	client_id = sys.argv[-1]
	for vid in map(int, sys.argv[1:-1]):
		collect_chunks(vid, client_id)
		merge_chunks(vid)