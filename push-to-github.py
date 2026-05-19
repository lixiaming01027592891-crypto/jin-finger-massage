#!/usr/bin/env python3
"""
金手指按摩網站 - GitHub 推送腳本
自動在 GitHub 創建倉庫並推送代碼

使用方式:
    python3 push-to-github.py

需要:
    - GitHub Personal Access Token (classic 或 fine-grained)
    - 權限: repo (用於創建私人/公開倉庫)

獲取 Token:
    https://github.com/settings/tokens
"""

import urllib.request
import urllib.error
import json
import subprocess
import sys
import os


def run(cmd, capture=True):
    """執行 shell 命令"""
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if capture:
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    return None, None, result.returncode


def get_input(prompt, default=None):
    """獲取用戶輸入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    return value if value else default


def github_api(method, endpoint, token, data=None):
    """調用 GitHub API"""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "jin-finger-massage-push-script",
    }
    if data:
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            error_data = json.loads(body)
            return e.code, error_data
        except:
            return e.code, {"message": body}
    except Exception as e:
        return 0, {"message": str(e)}


def main():
    print("=" * 60)
    print("  金手指按摩網站 - GitHub 推送工具")
    print("=" * 60)
    print()

    # 1. 檢查 git 倉庫
    _, _, code = run("git rev-parse --git-dir")
    if code != 0:
        print("[錯誤] 當前目錄不是 git 倉庫")
        print("        請先執行: git init")
        sys.exit(1)

    # 2. 獲取 GitHub Token
    print("[步驟 1/5] GitHub 認證")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        token = get_input("  請輸入 GitHub Personal Access Token")
    if not token:
        print("[錯誤] 需要提供 GitHub Token")
        print("        請到 https://github.com/settings/tokens 創建")
        sys.exit(1)

    # 3. 驗證 Token
    print("  正在驗證 Token...")
    status, user_data = github_api("GET", "/user", token)
    if status != 200:
        print(f"[錯誤] Token 驗證失敗: {user_data.get('message', 'Unknown error')}")
        sys.exit(1)
    username = user_data["login"]
    print(f"  ✓ 已登入: {username}")
    print()

    # 4. 設置倉庫名稱
    print("[步驟 2/5] 倉庫設置")
    repo_name = get_input("  倉庫名稱", "jin-finger-massage")
    is_private = get_input("  私人倉庫? (y/n)", "n").lower() == "y"
    description = get_input("  倉庫描述", "金手指按摩 - 24小時專業按摩養生會館 SEO 網站")
    print(f"  倉庫: {username}/{repo_name} ({'私人' if is_private else '公開'})")
    print()

    # 5. 創建倉庫
    print("[步驟 3/5] 創建 GitHub 倉庫...")
    status, repo_data = github_api(
        "POST",
        "/user/repos",
        token,
        {
            "name": repo_name,
            "description": description,
            "private": is_private,
            "auto_init": False,
        },
    )

    if status == 201:
        print(f"  ✓ 倉庫已創建: {repo_data['html_url']}")
    elif status == 422 and "already exists" in str(repo_data):
        print(f"  ⚠ 倉庫已存在，將推送到現有倉庫")
        status2, repo_data = github_api("GET", f"/repos/{username}/{repo_name}", token)
        if status2 != 200:
            print(f"[錯誤] 無法訪問現有倉庫: {repo_data.get('message', '')}")
            sys.exit(1)
        print(f"  ✓ 使用現有倉庫: {repo_data['html_url']}")
    else:
        print(f"[錯誤] 創建倉庫失敗 (HTTP {status}): {repo_data.get('message', '')}")
        sys.exit(1)
    print()

    # 6. 配置 git remote
    print("[步驟 4/5] 配置 git remote...")
    repo_url = f"https://{token}@github.com/{username}/{repo_name}.git"

    # 移除現有的 origin remote（如果存在）
    run("git remote remove origin 2>/dev/null")
    _, err, code = run(f"git remote add origin {repo_url}")
    if code != 0:
        print(f"[錯誤] 添加 remote 失敗: {err}")
        sys.exit(1)
    print("  ✓ Remote 已設置")

    # 設置 git 用戶信息（如果沒有）
    name, _, _ = run("git config user.name")
    email, _, _ = run("git config user.email")
    if not name:
        run("git config user.name '金手指按摩'")
    if not email:
        run("git config user.email 'info@goldenfinger.tw'")
    print()

    # 7. 推送到 GitHub
    print("[步驟 5/5] 推送到 GitHub...")
    print("  正在推送 master 分支...")
    out, err, code = run("git push -u origin master")
    if code != 0:
        # 嘗試 main 分支名稱
        out, err, code = run("git push -u origin main")
        if code != 0:
            print(f"[錯誤] 推送失敗:\n{err}\n{out}")
            sys.exit(1)

    print(f"  ✓ 推送成功！")
    print()
    print("=" * 60)
    print(f"  🎉 完成！倉庫地址:")
    print(f"     {repo_data['html_url']}")
    print()
    print(f"  GitHub Pages 部署:")
    print(f"     1. 前往 {repo_data['html_url']}/settings/pages")
    print(f"     2. Source 選擇 'Deploy from a branch'")
    print(f"     3. Branch 選擇 'master' + '/ (root)'")
    print(f"     4. 點擊 Save")
    print()
    print(f"  或者使用 GitHub Actions 自動部署:")
    print(f"     已為您準備 .github/workflows/deploy.yml")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n[錯誤] {e}")
        sys.exit(1)
