import requests
from typing import NamedTuple
import os


__all__ = ('Mod',)


URL_MR = 'https://api.modrinth.com/api/v1'
URL_CF = 'https://curse.nikky.moe/api'
CF_SEARCH_HEADERS = { 'Accept': 'application/json', 'x-api-key': os.getenv('CF_KEY') }


def _get(url: str, *args, **kwargs):
	return requests.get(url, *args, **kwargs).json()


class Mod(NamedTuple):
	name: str
	summary: str
	authors: list[str]
	downloads: int
	url: str

	@staticmethod
	def from_modrinth(slug: str):
		data = _get(f'{URL_MR}/mod/{slug}')
		members = [
			_get(f'{URL_MR}/user/{member_id}')['username']
			for member_id in
			_get(f'{URL_MR}/team/{data['team']}/members')
		]

		return Mod(
			data['title'],
			data['description'],
			members,
			data['downloads'],
			f'https://modrinth.com/mod/{slug}'
		)

	@staticmethod
	def from_curseforge(slug: str):
		data = _get(f'{URL_CF}/addon/{slug}')
		return Mod(
			data['name'],
			data['summary'],
			[user['name'] for user in data['authors']],
			data['downloadCount'],
			data['websiteUrl']
		)


def search_modrinth(query: str):
	"""Performs a search using a specific query on Modrinth. Only returns the title, slug, and URL of each mod!"""
	return [
		(hit['title'], hit['slug'], f'https://modrinth.com/mod/{hit['slug']}')
		for hit in
		_get(f'{URL_MR}/mod?query={query}')['hits']
	]

def search_curseforge(query: str):
	"""Performs a search using a specific query on Curseforge. Only returns the title, slug, and URL of each mod!"""
	return [
		(hit['name'], hit['id'], hit['websiteUrl'])
		for hit in
		_get(f'https://api.curseforge.com/v1/mods/search?gameId=432&categoryId=&searchFilter={query}', headers = CF_SEARCH_HEADERS)['data']
	]
