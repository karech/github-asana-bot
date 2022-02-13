from typing import Optional

from github_webhooks.schemas import WebhookCommonPayload
from pydantic import BaseModel, Field


class PullRequestPayload(WebhookCommonPayload):
    class PullRequest(BaseModel):
        title: str
        body: Optional[str] = ''
        url: str = Field(alias='html_url')

    action: str
    pull_request: PullRequest


class PushPayload(WebhookCommonPayload):
    class Commit(BaseModel):
        message: str

    ref: str
    commits: list[Commit]

    def get_branch_name(self) -> str:
        if 'refs/heads/' not in self.ref:
            return ''

        return self.ref.removeprefix('refs/heads/')
