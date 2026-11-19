#!/bin/bash
# Checks the requirements folder. Errors (exit 1): duplicate IDs, a sub-requirement with no parent, a reference to an
# ID that does not exist. Warnings (listed, exit 0): a number or duration outside DEF-01, history or script wording.
# Uses only bash and awk. Run from the repository root: tests/tools/req_check.sh
cd "$(dirname "$0")/../../requirements" || exit 2
echo "Rules: requirements/README.md (rules 1 and 2 are the laws; each rule has its test)"
files=$(ls *.md *.d/*.md | grep -v -e '^README.md$' -e '^oldkey.md$')
err=0
rows=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{gsub(/ /,"",$2); print FILENAME" "$2}' $files)
ids=$(echo "$rows" | awk '{print $2}' | sort)
echo "== malformed rows (not five columns; common.md has its own layout)"
cfiles=$(ls *.md *.d/*.md | grep -v -e '^README.md$' -e '^oldkey.md$' -e '^common.md$')
bad=$(grep -HE '^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|' $cfiles | sed 's/\\|//g' | awk -F'|' 'NF!=7 {split($1,a,":"); print a[1]": "$2}')
[ -n "$bad" ] && { echo "$bad"; err=1; } || echo none
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
echo "== errors: the same statement in two rows (rule 1, say it once)"
same=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ s=tolower($4); gsub(/^ +| +$/,"",s); if (length(s)>40) { id=$2; gsub(/ /,"",id); if (s in seen) print seen[s]" = "id; else seen[s]=id } }' $files | tr '\n' ';')
[ -n "$same" ] && { echo "$same"; err=1; } || echo none
echo "== warnings: exception wording (rule 2, no exceptions; a judgment call, read the row)"
awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if (tolower($4) ~ /(^|[^a-z])(except|unless)([^a-z]|$)|never for|only when/) { id=$2; gsub(/ /,"",id); print id } }' $files | tr '\n' ' '; echo
echo "== errors: an agent or tool is named (rule 11)"
named=$(grep -nE 'Claude|ChatGPT|GPT|Codex|Copilot|Anthropic|OpenAI' $files README.md | cut -d: -f1,2 | tr '\n' ';')
[ -n "$named" ] && { echo "$named"; err=1; } || echo none
echo "== questions: every (?) row is in open-questions.md and every question there has a (?) row (rule 10)"
q=../build_rules/open-questions.md
qrows=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/ && $3 ~ /\(\?\)/ {id=$2; gsub(/ /,"",id); print id}' $files | sort)
qfile=$(grep -oE '^- \*\*[A-Z]+-[0-9]+(\.[a-z]+)?\*\*' $q | grep -oE '[A-Z]+-[0-9]+(\.[a-z]+)?' | sort)
qbad=$( { comm -23 <(echo "$qrows") <(echo "$qfile") | sed 's/^/no question for row: /'; comm -13 <(echo "$qrows") <(echo "$qfile") | sed 's/^/question without a (?) row: /'; } )
[ -n "$qbad" ] && { echo "$qbad"; err=1; } || echo none
[ $err -ne 0 ] && echo "RESULT: errors" || echo "RESULT: no errors"; exit $err
