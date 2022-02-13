# Example project with github-webhooks - Asana bot  

This project shows how can [github-webhooks][1] can be used - to notify in asana that task's PR was merged. 


# How to use it
1. add to all PRs link to asana task
2. configure `.env` file: 
```dotenv
GITHUB_WEBHOOKS_TOKEN = 'webhooks-secret'
GITHUB_TOKEN = 'github-personal-token'
ASANA_TOKEN = 'asana-token'

DEV_BRANCH = 'dev'
PROD_BRANCH = 'prod'
```
3. run service `uvicorn bot.server:app`
4. configure repository webhooks to `{url}/hook` (where `url` is url where service is running) 


[1]: https://github.com/karech/github-webhooks/
