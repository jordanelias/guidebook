#!/bin/bash
# wrapper: scratch DB inline on every call, repo root, log every verb and its tail to the session folder
cd /home/user/guidebook
export GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm/guidebook.db
python3 scripts/db.py "$@" 2>&1
