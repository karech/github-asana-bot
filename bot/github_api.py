import logging
import re
from typing import Optional

from aioify import aioify
from github import Github, UnknownObjectException

from bot.settings import settings


class GithubAPI:
    _pull_id_re = re.compile(r'\(#(\d+)\)')

    def __init__(self) -> None:
        self._api = Github(settings.GITHUB_TOKEN)

    def get_pull_id(self, commit: str) -> Optional[int]:
        values = self._pull_id_re.findall(commit)

        for pull_id in values:
            try:
                return int(pull_id)
            except ValueError:
                continue

        return None

    @aioify
    def get_pull_body(self, repository: str, pull_id: int) -> Optional[str]:
        try:
            repo = self._api.get_repo(repository, lazy=True)
            pull = repo.get_pull(pull_id)

            return pull.body

        except UnknownObjectException:
            logging.error('Pull #%s not found in %s', pull_id, repository)

        return None
