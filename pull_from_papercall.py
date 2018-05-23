from urllib import urlencode
import os
import random
import string

import requests

import logic


API_KEY = os.environ["PAPERCALL_API_KEY"]

def get_papercall_submissions():
    page = 1
    while True:
        url = "https://www.papercall.io/api/v1/submissions"
        qs = {
            "_token": API_KEY,
            "page": page,
            "per_page": 50,
            "order": "created_at",
        }
        response = requests.get(url + "?" + urlencode(qs))
        submissions = response.json()
        if not submissions:
            break

        for submission in submissions:
            if submission["state"] != "submitted":
                continue
            yield submission

        page += 1

def convert_submission(sub, anonymous):
    talk = sub["talk"]
    if anonymous:
        profile = {
            "name": "Anonymous Submitter",
            "email": "".join(random.choice(string.ascii_letters) for _ in range(10)) + "@pygotham.org",
        }
    else:
        profile = sub["profile"]

    return {
        "id": sub["id"],
        "title": talk["title"],
        "authors": [{"email": profile["email"], "name": profile["name"]}],
        "duration": talk["talk_format"],
        "abstract": talk["abstract"],
        "description": talk["description"],
        "category": ", ".join(sorted(talk.get("tag_list", []))),
        "outline": sub["additional_info"],
        "notes": talk["notes"],
        "audience": talk["audience_level"],
        "audience_level": talk["audience_level"],
        "objective": "--objective--",
        "recording_release": True,
        "additional_notes": "--additional notes--",
        "additional_requirements": "--additional requirements--",
    }


def main(anonymous, talk_ids):
    for submission in get_papercall_submissions():
        proposal = convert_submission(submission, anonymous)
        if talk_ids and proposal["id"] not in talk_ids:
            continue
        logic.add_proposal(proposal)


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description="Import talks from PaperCall")
    parser.add_argument("--anonymous", default=False, help="Don't import speaker information")
    parser.add_argument("talk_ids", metavar="TALK_ID", type=int, nargs="+", help="Import only the listed papercall talk IDs")
    opts = parser.parse_args()

    main(opts.anonymous, frozenset(opts.talk_ids))
