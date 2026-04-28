# -*- coding: utf-8 -*-
import argparse
import os
import re
from github import Github
from datetime import datetime

# 终极美化版 README 模板
README_TEMPLATE = """

<h1 align="center">🚀 {user_name} DebugDiary</h1>

<p align="center">
  <a href="https://{user_name}.github.io/{repo_name}/"><strong>🌐 访问在线博客</strong></a> | 
  <a href="https://github.com/{user_name}/{repo_name}/issues"><strong>💬 订阅文章</strong></a> |
  <a href="https://github.com/{user_name}/{repo_name}/actions"><strong>⚙️ 运行状态</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/{user_name}/{repo_name}?style=flat-square&label=Last%20Update&color=blue">
  <img src="https://img.shields.io/github/issues/{user_name}/{repo_name}?style=flat-square&label=Posts&color=orange">
</p>

---

### 📝 最近讨论
{communication}

### 📚 全部博文
{posts}

---

<p align="right">
  <i>最后同步于: {update_time}</i>
</p>
"""

BACKUP_DIR = "BACKUP"
ANCHOR_NUMBER = 5

def get_me(user):
    return user.get_user().login

def format_time(time):
    return str(time)[:10]

def login(token):
    return Github(token)

def save_post(issue):
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    title = re.sub(r'[\\/:*?"<>|]', "_", issue.title)
    with open(os.path.join(BACKUP_DIR, f"{issue.number}_{title}.md"), "w", encoding="utf-8") as f:
        f.write(issue.body)

def main(token, repo_full_name, issue_number=None):
    user = login(token)
    me = get_me(user)
    repo = user.get_repo(repo_full_name)
    user_name, repo_name = repo_full_name.split("/")
    
    issues = repo.get_issues(state="all", creator=me)
    posts = [i for i in issues if not i.pull_request]

    # 备份文件
    for post in posts:
        save_post(post)

    # 格式化博文列表
    posts_md = ""
    for post in posts:
        posts_md += f"* [{post.title}](https://github.com/{repo_full_name}/issues/{post.number}) `({format_time(post.created_at)})` \n"

    # 格式化最近更新
    communication_md = ""
    for post in posts[:ANCHOR_NUMBER]:
        communication_md += f"* [{post.title}](https://github.com/{repo_full_name}/issues/{post.number})\n"

    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 填充并写入 README
    new_readme = README_TEMPLATE.format(
        user_name=user_name,
        repo_name=repo_name,
        communication=communication_md,
        posts=posts_md,
        update_time=update_time
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token")
    parser.add_argument("repo_name")
    parser.add_argument("--issue_number", default=None)
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
