"""
Parkly.uz - GitHub Collaborators avtomatik qo'shish skripti.
Foydalanish:
1. GitHub > Settings > Developer Settings > Personal access tokens (Tokens classic) dan 'repo' huquqi bilan token oling.
2. Quyidagi TEAM ro'yxatiga jamoangiz a'zolarining GitHub username'larini kiriting.
3. Skriptni ishga tushiring: python add_collaborators.py
"""

import json
import urllib.request
import urllib.error

# 1. Sozlamalar
GITHUB_TOKEN = "SIZNING_GITHUB_TOKENINGIZ"  # ghp_ bilan boshlanuvchi token
REPO_OWNER = "erjigitvv5"
REPO_NAME = "Parkly.uz"

# 2. Jamoa a'zolari va ularning rollari
# Ruxsatlar:
# - 'push'     -> Developerlar (Write: kod yozadi, branch ochadi, PR yuboradi)
# - 'triage'   -> Project Manager (Issues, Projects, Labels boshqaradi)
# - 'maintain' -> Lead / Senior Developer (PR ko'radi, merge qiladi)
# - 'admin'    -> Co-founder / Texnik direktor
TEAM = [
    {"username": "pm_username", "role": "triage", "description": "Project Manager"},
    {"username": "dev1_username", "role": "push", "description": "Backend Dasturchi"},
    {"username": "dev2_username", "role": "push", "description": "Frontend Dasturchi"},
    {"username": "dev3_username", "role": "push", "description": "Mobile (Flutter) Dasturchi"},
    {"username": "dev4_username", "role": "push", "description": "IoT / Simulyator Dasturchi"},
    {"username": "qa_username", "role": "triage", "description": "QA Tester"},
]

def add_collaborator(username, permission):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/collaborators/{username}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Parkly-Setup-Script"
    }
    data = json.dumps({"permission": permission}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="PUT")

    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [201, 204]:
                print(f"✅ Taklifnoma yuborildi: {username} ({permission})")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Xatolik ({username}): HTTP {e.code} - {error_body}")
    except Exception as e:
        print(f"❌ Xatolik ({username}): {str(e)}")

if __name__ == "__main__":
    if GITHUB_TOKEN == "SIZNING_GITHUB_TOKENINGIZ":
        print("⚠️ Iltimos, avval GITHUB_TOKEN o'rniga o'zingizning GitHub tokeningizni kiriting!")
    else:
        print(f"🚀 {REPO_NAME} repozitoriyasiga jamoa a'zolari qo'shilmoqda...\n")
        for member in TEAM:
            print(f"👤 Qo'shilmoqda: {member['description']} (@{member['username']})...")
            add_collaborator(member["username"], member["role"])
        print("\n🎉 Barcha taklifnomalar muvaffaqiyatli yuborildi!")
