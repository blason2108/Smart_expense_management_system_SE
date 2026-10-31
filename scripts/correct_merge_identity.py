#!/usr/bin/env python3
"""Correct one accidental merge identity; preserve file trees and other authors.

Default: prepare a backup and report only. --apply atomically updates affected
remote branch heads using exact expected-head leases. Owner approval is required.
AI assistance remains documented; this does not create student contributions.
"""

import argparse
import json
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

REPOSITORY = "https://github.com/blason2108/Smart_expense_management_system_SE.git"
TARGET = "3e0aee4d98a4e7684e1b732f426ed6d5f759cae4"
OLD_IDENTITY = b"Codex <codex@openai.com>"
NEW_IDENTITY = b"Bollavaram Santosh Kumar <santoshkumarbollavaram@gmail.com>"


def git(repo, *args, input_bytes=None):
    return subprocess.check_output(
        ["git", "--git-dir", str(repo), *args], input=input_bytes
    )


def rewrite(repo, target=TARGET):
    refs = {}
    for line in (
        git(repo, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads")
        .decode()
        .splitlines()
    ):
        ref, sha = line.split()
        refs[ref] = sha
    if not refs:
        raise RuntimeError("No branch heads found.")
    # Tags are not silently rewritten. A tag retaining the old merge needs a separate decision.
    for tag in (
        git(repo, "for-each-ref", "--format=%(refname)", "refs/tags")
        .decode()
        .splitlines()
    ):
        commit = subprocess.run(
            ["git", "--git-dir", str(repo), "rev-parse", tag + "^{commit}"],
            capture_output=True,
            check=False,
            text=True,
        )
        if commit.returncode == 0:
            result = subprocess.run(
                [
                    "git",
                    "--git-dir",
                    str(repo),
                    "merge-base",
                    "--is-ancestor",
                    target,
                    commit.stdout.strip(),
                ],
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                raise RuntimeError(
                    f"{tag} retains the target merge. Stop for an explicit tag-handling decision."
                )
    order = (
        git(repo, "rev-list", "--reverse", "--topo-order", *refs.values())
        .decode()
        .splitlines()
    )
    if target not in order:
        raise RuntimeError(
            "Original merge not reachable from branch heads; it may already be corrected. No writes."
        )
    mapping = {}
    stripped_signatures = 0
    for sha in order:
        raw = git(repo, "cat-file", "commit", sha)
        header, message = raw.split(b"\n\n", 1)
        groups = []
        for line in header.split(b"\n"):
            if line.startswith(b" "):
                groups[-1].append(line)
            else:
                groups.append([line])
        parents = [
            group[0].split(b" ", 1)[1].decode()
            for group in groups
            if group[0].startswith(b"parent ")
        ]
        if sha != target and not any(parent in mapping for parent in parents):
            continue
        output = []
        corrected_roles = 0
        for group in groups:
            line = group[0]
            if line.startswith((b"gpgsig ", b"gpgsig-sha256 ", b"mergetag ")):
                stripped_signatures += 1
                continue
            if line.startswith(b"parent "):
                old = line.split(b" ", 1)[1].decode()
                group = [b"parent " + mapping.get(old, old).encode()]
            if sha == target and line.startswith((b"author ", b"committer ")):
                role, value = line.split(b" ", 1)
                if not value.startswith(OLD_IDENTITY + b" "):
                    raise RuntimeError(
                        "Target identity differs from the reviewed identity. No writes."
                    )
                group = [role + b" " + NEW_IDENTITY + value[len(OLD_IDENTITY) :]]
                corrected_roles += 1
            output.extend(group)
        if sha == target and corrected_roles != 2:
            raise RuntimeError(
                "Expected exactly one author and one committer on target merge."
            )
        new = (
            git(
                repo,
                "hash-object",
                "-t",
                "commit",
                "-w",
                "--stdin",
                input_bytes=b"\n".join(output) + b"\n\n" + message,
            )
            .decode()
            .strip()
        )
        if git(repo, "rev-parse", sha + "^{tree}") != git(
            repo, "rev-parse", new + "^{tree}"
        ):
            raise RuntimeError("File tree changed. No writes.")
        mapping[sha] = new
    updates = {
        ref: {"before": sha, "after": mapping[sha]}
        for ref, sha in refs.items()
        if sha in mapping
    }
    for ref, values in updates.items():
        subprocess.run(
            [
                "git",
                "--git-dir",
                str(repo),
                "diff",
                "--exit-code",
                values["before"],
                values["after"],
            ],
            check=True,
        )
    return {
        "target": target,
        "mapping": mapping,
        "updates": updates,
        "signature_headers_removed": stripped_signatures,
        "file_trees_unchanged": True,
    }


def apply(repo, report):
    updates = report["updates"]
    if not updates:
        raise RuntimeError("No branch updates prepared.")
    args = ["push", "--atomic"]
    args += [
        f"--force-with-lease={ref}:{values['before']}"
        for ref, values in updates.items()
    ]
    args += ["origin"]
    args += [f"{values['after']}:{ref}" for ref, values in updates.items()]
    subprocess.run(
        ["git", "--git-dir", str(repo), "-c", "remote.origin.mirror=false", *args],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the owner-approved history correction.",
    )
    args = parser.parse_args()
    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    parent = Path.cwd().parent / "history-identity-backups"
    parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=stamp + "-", dir=parent))
    mirror = work / "repository.git"
    subprocess.run(["git", "clone", "--mirror", REPOSITORY, str(mirror)], check=True)
    bundle = work / "before-correction.bundle"
    subprocess.run(
        ["git", "--git-dir", str(mirror), "bundle", "create", str(bundle), "--all"],
        check=True,
    )
    subprocess.run(
        ["git", "--git-dir", str(mirror), "bundle", "verify", str(bundle)], check=True
    )
    # Keep the required AI log: the correction does not remove its contents.
    ai_log = git(mirror, "show", "refs/heads/main:docs/llm-prompts.md")
    if not ai_log.strip():
        raise RuntimeError("Expected AI assistance log is missing. No writes.")
    report = rewrite(mirror)
    report["backup_bundle"] = str(bundle)
    report["repository"] = REPOSITORY
    (work / "correction-review.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Backup:", bundle, flush=True)
    print("Changed commit objects:", len(report["mapping"]), flush=True)
    for ref, values in report["updates"].items():
        print(ref, values["before"], "->", values["after"], flush=True)
    print(
        "Every changed commit retains its original file tree; other student identities are unchanged.",
        flush=True,
    )
    print(
        "Signatures removed from rewritten headers:",
        report["signature_headers_removed"],
        flush=True,
    )
    if not args.apply:
        print(
            "PREPARED ONLY. No remote history changed. Use --apply only after owner approval."
        )
        return
    apply(mirror, report)
    report["applied"] = True
    (work / "correction-review.json").write_text(json.dumps(report, indent=2) + "\n")
    print("APPLIED: all affected branch updates succeeded atomically.")
    print(
        "Keep the backup. Existing clones still contain old history; use a fresh clone for future development."
    )
    print("Your current worktree, SQLite database and .env were not modified.")
    print(
        "GitHub caches and historical PR refs may retain old identities; the contributor display may not update immediately."
    )


if __name__ == "__main__":
    main()
