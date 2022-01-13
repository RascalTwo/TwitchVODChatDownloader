
import datetime

from typing import Callable, Optional


def follow_cursors(func: Callable[[Optional[str]], Optional[str]]):
	cursor = None
	while True:
		next_cursor = func(cursor)
		if cursor == next_cursor or next_cursor is None:
			break
		cursor = next_cursor

def parse_twitch_timestamp(timestamp: str) -> datetime.datetime:
	return datetime.datetime.strptime(timestamp.replace('Z', ''), '%Y-%m-%dT%H:%M:%S' + ('.%f' if '.' in timestamp else ''))
