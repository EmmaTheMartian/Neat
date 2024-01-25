import requests
from typing import NamedTuple, Optional
import os


URL_MR = 'https://api.modrinth.com/v2'
URL_CF = 'https://api.curseforge.com/v1'
CF_HEADERS = { 'Accept': 'application/json', 'x-api-key': os.getenv('CF_KEY') }
_MR_CATEGORIES = {
	'mod': 'mod',
	'modpack': 'modpack',
	'resourcepack': 'resourcepack',
	'shader': 'shader'
}
_CF_CATEGORIES = {
	'mod': 6,
	'modpack': 4471,
	'shader': 6552,
	'resourcepack': 12,
	'plugin': 5,
	'world': 17,
	'addon': 4559,
}


def _get(url: str, *args, **kwargs) -> requests.Response | None:
	try:
		return requests.get(url, *args, **kwargs)
	except Exception as e:
		print(f'\033[31;1m_get error:\033[0m {e}')
		return None


def _get_mr(url: str, *args, **kwargs) -> requests.Response | None:
	return _get(URL_MR + url, *args, *kwargs)


def _get_cf(url: str, *args, **kwargs) -> requests.Response | None:
	return _get(URL_CF + url, headers = CF_HEADERS, *args, **kwargs)


class Mod(NamedTuple):
	name: str
	summary: str
	authors: list[str]
	downloads: int
	url: str
	icon_url: str

	@staticmethod
	def from_modrinth(slug: str):
		data = _get_mr(f'/project/{slug}')
		if data == None or data.status_code == 404:
			return 404

		data = data.json()
		members = _get_mr(f'/team/{data['team']}/members')
		if members == None:
			return 404

		members = [
			member['user']['username']
			for member in
			members.json()
		]

		return Mod(
			data['title'],
			data['description'],
			members,
			data['downloads'],
			f'https://modrinth.com/mod/{slug}',
			data['icon_url']
		)

	@staticmethod
	def from_curseforge(project_id: int):
		data = _get_cf(f'/mods/{project_id}')
		if data == None or data.status_code == 404:
			return 404

		data = data.json()['data']
		return Mod(
			data['name'],
			data['summary'],
			[user['name'] for user in data['authors']],
			data['downloadCount'],
			data['links']['websiteUrl'],
			data['logo']['url']
		)


def search_modrinth(query: str, category: str | None = None) -> Optional[list[tuple[str, str, str]]]:
	"""Performs a search using a specific query on Modrinth. Only returns the title, slug, and URL of each mod!"""
	category = 'mod' if category is None else category
	response = _get_mr(f'/search?query={query}&facets=[["project_type:{category}"]]')

	if response == None or response.status_code == 404:
		return None

	return [
		(hit['title'], hit['slug'], f'https://modrinth.com/{_MR_CATEGORIES[category]}/{hit['slug']}')
		for hit in
		response.json()['hits']
	]


def search_curseforge(query: str, category: str | None = None) -> Optional[list[tuple[str, str, str]]]:
	"""Performs a search using a specific query on Curseforge. Only returns the title, slug, and URL of each mod!"""
	category = category if category is not None else 'mod'
	response = _get_cf(f'/mods/search', params = {
		'gameId': 432,
		'searchFilter': query,
		'classId': _CF_CATEGORIES[category],
		'pageSize': 10
	})

	if response == None or response.status_code == 404:
		return None

	return [
		(hit['name'], hit['id'], hit['links']['websiteUrl'])
		for hit in
		response.json()['data']
	]
