import subprocess
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================
# CONFIGURATION
# ==========================================

PROJECT_DIR = Path(".")
BRANCH = "main"

COMMIT_MESSAGES = [
    "feat: improve project functionality",
    "feat: add project enhancement",
    "fix: resolve project issue",
    "refactor: improve project structure",
    "docs: update documentation",
    "test: improve project tests",
    "chore: update project configuration",
]


# ==========================================
# RUN GIT COMMAND
# ==========================================

def run_git(*args):

    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_DIR,
        text=True,
        capture_output=True
    )

    if result.returncode != 0:
        print("\nGit error:")
        print(result.stderr)

        raise RuntimeError(
            f"Git command failed: git {' '.join(args)}"
        )

    return result.stdout.strip()


# ==========================================
# CHECK GIT REPOSITORY
# ==========================================

def check_repository():

    try:
        run_git("rev-parse", "--is-inside-work-tree")
    except RuntimeError:

        print("❌ This folder is not a Git repository.")
        print("Run this script inside your GitHub project folder.")

        return False

    return True


# ==========================================
# GET CURRENT CHANGES
# ==========================================

def get_changes():

    output = run_git("status", "--porcelain")

    if not output:
        return []

    return output.splitlines()


# ==========================================
# CREATE COMMIT
# ==========================================

def create_commit():

    changes = get_changes()

    if not changes:

        print("\n⚠️ No changes detected.")
        print("Make a real change to your project first.")
        return False

    print("\n📁 Changed files:")

    for change in changes:
        print("   ", change)

    # Add actual project changes
    run_git("add", ".")

    # Use India time
    india_now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    message_index = india_now.day % len(COMMIT_MESSAGES)

    message = COMMIT_MESSAGES[message_index]

    run_git(
        "commit",
        "-m",
        message
    )

    print("\n✅ Commit created:")
    print(message)

    return True


# ==========================================
# PUSH TO GITHUB
# ==========================================

def push_to_github():

    print("\n🚀 Pushing to GitHub...")

    run_git(
        "push",
        "origin",
        BRANCH
    )

    print("✅ Successfully pushed to GitHub.")


# ==========================================
# MAIN
# ==========================================

def main():

    print("\n" + "=" * 55)
    print("       GitHub Activity Helper")
    print("=" * 55)

    # Check repository
    if not check_repository():
        return

    # Show current India time
    india_now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    print(
        "\n🇮🇳 India Time:",
        india_now.strftime(
            "%d-%m-%Y %H:%M:%S %Z"
        )
    )

    # Show repository
    try:

        remote = run_git(
            "remote",
            "get-url",
            "origin"
        )

        print("🔗 Repository:", remote)

    except RuntimeError:

        print("⚠️ No origin remote configured.")

    # Create commit
    committed = create_commit()

    # Push
    if committed:

        try:
            push_to_github()

        except RuntimeError:

            print("\n❌ Push failed.")
            print("Check your GitHub authentication and branch name.")


# ==========================================
# START
# ==========================================

if __name__ == "__main__":
    main()