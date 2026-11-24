#!/bin/bash
HOST="${HOST:-https://curtinmy-stagehand.chals.io}"
BODY=$(php forge_solver.php "$1" | sed 's/^POSTBODY=//')
curl -s -X POST "$HOST/" --data "$BODY" -c crew.txt >/dev/null
echo "[$1]"; curl -s "$HOST/" -b crew.txt | grep -i 'show report'
