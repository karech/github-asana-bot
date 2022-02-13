import asyncio
import logging
from typing import Any, Iterable

from .asana_api import AsanaAPI
from .github_api import GithubAPI
from .schemas import PullRequestPayload, PushPayload
from .settings import settings


async def handle_pull_request(payload: PullRequestPayload) -> None:
    if payload.action != 'opened':
        logging.debug('handle_pull_request: action != opened, %s', payload.action)
        return

    if not payload.pull_request.body:
        logging.debug('handle_pull_request: PR body is empty')
        return

    asana_api = AsanaAPI()

    task_ids = asana_api.find_task_ids(payload.pull_request.body)
    await _send_message_to_tasks(asana_api, task_ids, f'PR {payload.pull_request.url}')


async def handle_push(payload: PushPayload) -> None:
    if payload.repository is None:
        logging.debug('handle_push: payload repository is empty')
        return

    target = payload.get_branch_name()

    if target not in {settings.DEV_BRANCH, settings.PROD_BRANCH}:
        logging.debug('handle_push: target branch not in dev/prod branches, %s', target)
        return

    repo = payload.repository.full_name
    message_template = f'PR {payload.repository.url}/pull/{{pull_id}} was merged to {target}'

    asana_api = AsanaAPI()
    github_api = GithubAPI()

    pulls: set[int] = set()

    for commit in payload.commits:
        pull_id = github_api.get_pull_id(commit.message)
        if pull_id:
            pulls.add(pull_id)

    if not pulls:
        logging.debug('handle_push: no pulls found')
        return

    results = await asyncio.gather(
        *[_process_pr(asana_api, github_api, repo, pull_id, message_template) for pull_id in pulls],
        return_exceptions=True,
    )
    _log_error_results(results)
    return


async def _send_message_to_tasks(asana_api: AsanaAPI, task_ids: Iterable[str], message: str) -> None:
    results = await asyncio.gather(
        *[asana_api.send_message(task_id, message, pin=True) for task_id in task_ids],
        return_exceptions=True,
    )
    _log_error_results(results)
    return


async def _process_pr(
    asana_api: AsanaAPI,
    github_api: GithubAPI,
    repo: str,
    pull_id: int,
    message_template: str,
) -> None:
    body = await github_api.get_pull_body(repo, pull_id)

    logging.debug('PR body %s', body)

    if not body:
        return

    task_ids = asana_api.find_task_ids(body)
    await _send_message_to_tasks(asana_api, task_ids, message_template.format(pull_id=pull_id))
    return


def _log_error_results(results: Iterable[Any]) -> None:
    for res in results:
        if not isinstance(res, BaseException):
            continue

        logging.error(res)
