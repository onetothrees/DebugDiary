# -*- coding: utf-8 -*-
import argparse
import os
import re

from github import Github
from marko import Markdown

# 修改后的简洁模板，去掉了原作者的个人信息
README_TEMPLATE = """
# {user_name} DebugDiary


> 记录技术、生活与思考。由 GitHub Issues 驱动的个人博客。
> A dedicated tech diary for developers to record debugging experiences and technical growth.   
## 最近更新
{communication}

## 博文列表
{posts}

---

*生成于: {update_time}*
"""

# 这里的链接已替换为你自己的仓库
MD_HEAD = """---
layout: post
title: {title}
date: {date}
tags: [{tags}]
---

## [{title}](https://github.com/{repo_name}/issues/{number})

"""

BACKUP_DIR = "BACKUP"
ANCHOR_NUMBER = 5
TOP_ISSUES_LABELS = ["Top"]


def get_me(user):
    return user.get_user().login


def is_me(issue, me):
    return issue.user.login == me


def format_time(time):
    return str(time)[:10]


def login(token):
    return Github(token)


def get_repo(user, repo_name):
    return user.get_repo(repo_name)


def parse_markdown(issue):
    content = issue.body
    # 简单的处理，你可以根据需要增加更复杂的解析
    return content


def get_posts(repo, me):
    issues = repo.get_issues(state="all", creator=me)
    posts = []
    for issue in issues:
        if issue.pull_request:
            continue
        posts.append(issue)
    return posts


def get_post_content(issue):
    return issue.body


def save_post(issue):
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    title = issue.title
    # 过滤文件名非法字符
    title = re.sub(r'[\\/:*?"<>|]', "_", title)
    date = format_time(issue.created_at)
    with open(os.path.join(BACKUP_DIR, f"{issue.number}_{title}.md"), "w", encoding="utf-8") as f:
        f.write(issue.body)


def main(token, repo_name, issue_number=None):
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)
    posts = get_posts(repo, me)

    # 保存所有博文到 BACKUP 文件夹
    for post in posts:
        save_post(post)

    # 构建 README 内容
    posts_md = ""
    for post in posts:
        posts_md += f"* [{post.title}](https://github.com/{repo_name}/issues/{post.number}) - {format_time(post.created_at)}\n"

    # 获取最近讨论（此处简化处理，展示最近的几个 issue）
    communication_md = ""
    for post in posts[:ANCHOR_NUMBER]:
        communication_md += f"* [{post.title}](https://github.com/{repo_name}/issues/{post.number})\n"

    from datetime import datetime
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 填充模板
    new_readme = README_TEMPLATE.format(
        user_name=me,
        communication=communication_md,
        posts=posts_md,
        update_time=update_time
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README.md updated successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument("--issue_number", help="issue_number", default=None, required=False)
    options = parser.parse_args()
    main(options.github_token, options.repo_name, options.issue_number)
