import re
from itertools import chain

import asana
from aioify import aioify

from bot.settings import settings


class AsanaAPI:
    _task_link_re = (
        re.compile(r'app\.asana\.com/\d+/\d+/project/\d+/task/(?P<gid>\d+)'),
        re.compile(r'app\.asana\.com/\d+/\d+/inbox/\d+/item/(?P<gid>\d+)/story/'),
        re.compile(r'app\.asana\.com/\d+/\d+/(?P<gid>\d+)'),
    )

    def __init__(self) -> None:
        self._client = asana.Client.access_token(settings.ASANA_TOKEN)

    @classmethod
    def find_task_ids(cls, text: str) -> set[str]:
        return set(chain(*map(lambda r: r.findall(text), cls._task_link_re)))

    @aioify
    def send_message(self, task_id: str, message: str, pin: bool = False) -> None:
        self._client.tasks.add_comment(
            task=task_id,
            params={
                'text': message,
                'is_pinned': pin,
            },
        )
