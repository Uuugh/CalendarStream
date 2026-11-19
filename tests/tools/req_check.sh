#!/bin/bash
# Checks the requirements folder. Errors (exit 1): duplicate IDs, a sub-requirement with no parent, a reference to an
# ID that does not exist. Warnings (listed, exit 0): a number or duration outside DEF-01, history or script wording.
# Uses only bash and awk. Run from the repository root: tests/tools/req_check.sh
cd "$(dirname "$0")/../../requirements" || exit 2
files=$(ls *.md | grep -v -e '^README.md$' -e '^oldkey.md$')
err=0
rows=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{gsub(/ /,"",$2); print FILENAME" "$2}' $files)
ids=$(echo "$rows" | awk '{print $2}' | sort)
echo "== duplicate IDs"; dup=$(echo "$ids" | uniq -d); [ -n "$dup" ] && { echo "$dup"; err=1; } || echo none
echo "== sub-requirements without a parent"
for s in $(echo "$ids" | grep '\.'); do p=${s%%.*}; echo "$ids" | grep -qx "$p" || { echo "$s"; err=1; }; done | grep . || echo none
echo "== references to IDs that do not exist"
awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{s=$4; while (match(s,/[A-Z][A-Z][A-Z]-[0-9]+(\.[a-z]+)?/)) {print $2" -> "substr(s,RSTART,RLENGTH); s=substr(s,RSTART+RLENGTH)}}' $files \
 | awk '{print $1" "$3}' | sort -u | while read from to; do echo "$ids" | grep -qx "$to" || { echo "$from -> $to"; }; done > /tmp/req_missing.txt
[ -s /tmp/req_missing.txt ] && { cat /tmp/req_missing.txt; err=1; } || echo none
echo "== warnings: numbers with units outside DEF-01 (rows not in common.md)"
awk -F"|" 'FILENAME!="common.md" && FILENAME!="theme.md" && /^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if ($4 ~ /[0-9]+ ?(minutes?|seconds?|hours?|days?|characters|px|MB|%)/ && $4 !~ /DEF-01/) print FILENAME": "$2}' $files | sed 's/ $//' | sort | uniq -c | awk '{print $2" "$3" "$4}' | tr '\n' ';'; echo
echo "== warnings: history or script wording"
awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if (tolower($4) ~ /python app|the checked|oracle|sampled|fixture|\(400\)/) print FILENAME": "$2}' $files | tr '\n' ';'; echo
[ $err -ne 0 ] && echo "RESULT: errors" || echo "RESULT: no errors"; exit $err
