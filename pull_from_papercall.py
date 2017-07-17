from urllib import urlencode
import os

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

def convert_submission(sub):
    talk = sub["talk"]
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


def main():
    for submission in get_papercall_submissions():
        proposal = convert_submission(submission)
        logic.add_proposal(proposal)


if __name__ == "__main__":
    main()