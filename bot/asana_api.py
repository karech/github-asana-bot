import re

import asana
from aioify import aioify

from bot.settings import settings


class AsanaAPI:
    _task_link_re = re.compile(r'app\.asana\.com/\d+/\d+/(?P<gid>\d+)')

    def __init__(self) -> None:
        self._client = asana.Client.access_token(settings.ASANA_TOKEN)

    @classmethod
    def find_task_ids(cls, text: str) -> list[str]:
        return cls._task_link_re.findall(text)

    @aioify
    def send_message(self, task_id: str, message: str, pin: bool = False) -> None:
        self._client.tasks.add_comment(
            task=task_id,
            params={
                'text': message,
                'is_pinned': pin,
            },
        )
