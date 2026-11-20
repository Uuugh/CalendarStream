#!/bin/bash
# Checks the requirements folder. Errors (exit 1): duplicate IDs, a sub-requirement with no parent, a reference to an
# ID that does not exist. Warnings (listed, exit 0): a number or duration outside DEF-01, history or script wording.
# Uses only bash and awk. Run from the repository root: tests/tools/req_check.sh
cd "$(dirname "$0")/../../requirements" || exit 2
echo "Rules: requirements/README.md (rules 1 and 2 are the laws; each rule has its test)"
files=$(ls *.md *.d/*.md | grep -v -e '^README.md$' -e '^oldkey.md$' -e '^open-questions.md$')
err=0
rows=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{gsub(/ /,"",$2); print FILENAME" "$2}' $files)
ids=$(echo "$rows" | awk '{print $2}' | sort)
echo "== malformed rows (not five columns; common.md has its own layout)"
cfiles=$(ls *.md *.d/*.md | grep -v -e '^README.md$' -e '^oldkey.md$' -e '^open-questions.md$' -e '^common.md$')
bad=$(grep -HE '^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|' $cfiles | sed 's/\\|//g' | awk -F'|' 'NF!=7 {split($1,a,":"); print a[1]": "$2}')
[ -n "$bad" ] && { echo "$bad"; err=1; } || echo none
echo "== duplicate IDs"; dup=$(echo "$ids" | uniq -d); [ -n "$dup" ] && { echo "$dup"; err=1; } || echo none
echo "== sub-requirements without a parent"
for s in $(echo "$ids" | grep '\.'); do p=${s%%.*}; echo "$ids" | grep -qx "$p" || { echo "$s"; err=1; }; done | grep . || echo none
echo "== references to IDs that do not exist"
missing=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{s=$4; while (match(s,/[A-Z][A-Z]+-[0-9]+(\.[a-z]+)?/)) {print $2" -> "substr(s,RSTART,RLENGTH); s=substr(s,RSTART+RLENGTH)}}' $files \
 | awk '{print $1" "$3}' | sort -u | while read from to; do echo "$ids" | grep -qx "$to" || { echo "$from -> $to"; }; done)
[ -n "$missing" ] && { echo "$missing"; err=1; } || echo none
echo "== warnings: numbers with units outside DEF-01 (rows not in common.md)"
awk -F"|" 'FILENAME!="common.md" && FILENAME!="theme.md" && /^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if ($4 ~ /[0-9]+ ?(minutes?|seconds?|milliseconds?|ms|hours?|days?|characters|px|mm|KB|MB|%)/ && $4 !~ /DEF-01/) print FILENAME": "$2}' $files | sed 's/ $//' | sort | uniq -c | awk '{print $2" "$3" "$4}' | tr '\n' ';'; echo
echo "== warnings: history or script wording"
awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if (tolower($4) ~ /python app|old app|legacy|rather than uid|\(developer, nov|the checked|oracle|sampled|fixture|\(400\)/) print FILENAME": "$2}' $files | tr '\n' ';'; echo
echo "== errors: the same statement in two rows (rule 1, say it once)"
same=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ s=tolower($4); gsub(/^ +| +$/,"",s); if (length(s)>40) { id=$2; gsub(/ /,"",id); if (s in seen) print seen[s]" = "id; else seen[s]=id } }' $files | tr '\n' ';')
[ -n "$same" ] && { echo "$same"; err=1; } || echo none
echo "== warnings: exception wording (rule 2, no exceptions; a judgment call, read the row)"
awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if (tolower($4) ~ /(^|[^a-z])(except|unless)([^a-z]|$)|never for|only when/) { id=$2; gsub(/ /,"",id); print id } }' $files | tr '\n' ' '; echo
echo "== errors: an agent or tool is named (rule 11)"
named=$(grep -nE 'Claude|ChatGPT|GPT|Codex|Copilot|Anthropic|OpenAI' $files README.md | cut -d: -f1,2 | tr '\n' ';')
[ -n "$named" ] && { echo "$named"; err=1; } || echo none
echo "== errors: a status other than proposed or backlog (README, Line format)"
badstat=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ s=$3; gsub(/^ +| +$/,"",s); if (s != "proposed" && s != "backlog" && s != "proposed (?)" && s != "backlog (?)") { id=$2; gsub(/ /,"",id); print id" ("s")" } }' $files | tr '\n' ';')
[ -n "$badstat" ] && { echo "$badstat"; err=1; } || echo none
echo "== errors: a connection file that does not state its role as a source, a feed or both (connections.md, CON-01.c)"
norole=$(for f in connections.d/*.md; do case $f in connections.d/README.md) continue;; esac; grep -qE '\| [A-Z]+-[0-9]+(\.[a-z]+)? \|[^|]*\|[^|]*(is a source|is a feed|both a source and a feed)' $f || echo $f; done | tr '\n' ';')
[ -n "$norole" ] && { echo "$norole"; err=1; } || echo none
echo "== prefixes: a feature has three letters; a module adds its folder's letter (C connections.d, P plugins.d); see README, Prefixes"
badpre=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ id=$2; gsub(/ /,"",id); split(id,a,"-"); p=a[1]; if (FILENAME ~ /^connections\.d\//) ok=(p ~ /^C[A-Z][A-Z][A-Z]$/); else if (FILENAME ~ /^plugins\.d\//) ok=(p ~ /^P[A-Z][A-Z][A-Z]$/); else ok=(p ~ /^[A-Z][A-Z][A-Z]$/); if (!ok) { k=FILENAME" "p; if (!(k in seen)) { seen[k]=1; print FILENAME": "p } } }' $files | tr '\n' ';')
[ -n "$badpre" ] && { echo "$badpre"; err=1; } || echo none
echo "== errors: a numbered rule in requirements/README.md or a rule in AGENTS.md without a Test line (law 3)"
notest=$(awk '/^## Rules for writing and changing requirements/{inr=1; next} /^## /{inr=0} inr && /^[0-9]+\. \*\*/ { if ($0 !~ /\*\*Test:\*\*/) { split($0,a,"."); print a[1] } }' README.md | tr '\n' ' ')
[ -n "$notest" ] && { echo "rules without a test: $notest"; err=1; } || echo none
notestA=$(awk '/^## (The laws|Standing rules)/{inr=1; next} /^## /{inr=0} inr && /^(- |[0-9]+[.] )[*][*]/ { if (blk != "" && blk !~ /[*][*]Test:[*][*]/) print first; blk=$0; first=substr($0,1,50); next } inr { blk=blk $0 } END { if (blk != "" && blk !~ /[*][*]Test:[*][*]/) print first }' ../AGENTS.md)
[ -n "$notestA" ] && { echo "AGENTS.md rules without a test:"; echo "$notestA"; err=1; } || echo none
echo "== warnings: rules in SCRUM.d, tests and packages READMEs without a Test line (law 3; fix by writing the Test line)"
awk '/^(- |[0-9]+[.] |  - )[*][*]/ { if (blk != "" && blk !~ /[*][*]Test:[*][*]/) n++; blk=$0; next } /^#/ { if (blk != "" && blk !~ /[*][*]Test:[*][*]/) n++; blk=""; next } /^$/ { next } blk != "" { blk=blk $0 } ENDFILE { if (blk != "" && blk !~ /[*][*]Test:[*][*]/) n++; blk="" } END { print n+0" rules" }' ../SCRUM.d/README.md ../tests/README.md ../packages/README.md
echo "== errors: a requirement a story names (SCRUM.d/sprint.md) whose test cell is still — (rule 13)"
if [ -f ../SCRUM.d/sprint.md ]; then
  named=$(grep -o -E '[A-Z]+-[0-9]+([.][a-z]+)?' ../SCRUM.d/sprint.md | sort -u)
  notestS=$(for id in $named; do grep -hE "^[|] ${id}([.][a-z]+)? [|]" $cfiles | sed 's/[\][|]//g' | awk -F'|' '{t=$5; gsub(/ /,"",t); if (t=="—") {i=$2; gsub(/ /,"",i); print i}}'; done | sort -u | tr '\n' ' ')
  [ -n "$notestS" ] && { echo "named rows without a test: $notestS"; err=1; } || echo none
else echo "none (no sprint file)"; fi
echo "== requirement rows whose test cell is still — (rule 13; a count, not an error)"
grep -hE '^[|] [A-Z]+-[0-9]+([.][a-z]+)? [|]' $cfiles | sed 's/[\][|]//g' | awk -F'|' '{t=$5; gsub(/ /,"",t); if (t=="—") n++} END {print n+0" rows"}'
echo "== errors: a requirement row outside its table (a non-table line before it) or a README link to a missing file"
outside=$(awk '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/{ if (prev !~ /^\|/) print FILENAME": line "FNR } { prev=$0 }' $files | tr '\n' ';')
badlink=$(grep -o '](\([^)#]*\))' README.md | sed 's/^](//; s/)$//' | grep -v '^http' | while read p; do [ -f "$p" ] || echo "$p"; done | tr '\n' ';')
[ -n "$outside$badlink" ] && { echo "$outside$badlink"; err=1; } || echo none
echo "== errors: a cited message key (msg:key) missing from messages/app_en.arb, or a locale file lacking a key the template has (rule 14)"
tkeys=$(grep -o '^  "[A-Za-z0-9]*":' messages/app_en.arb | tr -d ' ":' | sort)
cited=$(grep -ho 'msg:[A-Za-z0-9]*' $files | sed 's/^msg://' | sort -u)
missing_cited=$(comm -13 <(echo "$tkeys") <(echo "$cited") | grep . | tr '\n' ' ')
lacking=$(for l in messages/app_*.arb; do case $l in messages/app_en.arb) continue;; esac; k=$(grep -o '^  "[A-Za-z0-9]*":' $l | tr -d ' ":' | sort); n=$(comm -23 <(echo "$tkeys") <(echo "$k") | wc -l); [ "$n" -gt 0 ] && echo "$l lacks $n keys"; done | tr '\n' ';')
[ -n "$missing_cited$lacking" ] && { echo "$missing_cited$lacking"; err=1; } || echo none
echo "   message keys not yet cited by a requirement: $(comm -23 <(echo "$tkeys") <(echo "$cited") | grep -c .) of $(echo "$tkeys" | wc -l)"
echo "== questions: every (?) row is in open-questions.md and every question there has a (?) row (rule 10)"
q=open-questions.md
qrows=$(awk -F'|' '/^\| [A-Z]+-[0-9]+(\.[a-z]+)? \|/ && $3 ~ /\(\?\)/ {id=$2; gsub(/ /,"",id); print id}' $files | sort)
qfile=$(grep -oE '^- \*\*[A-Z]+-[0-9]+(\.[a-z]+)?\*\*' $q | grep -oE '[A-Z]+-[0-9]+(\.[a-z]+)?' | sort)
qbad=$( { comm -23 <(echo "$qrows") <(echo "$qfile") | sed 's/^/no question for row: /'; comm -13 <(echo "$qrows") <(echo "$qfile") | sed 's/^/question without a (?) row: /'; } )
[ -n "$qbad" ] && { echo "$qbad"; err=1; } || echo none
echo "== errors: a .d folder with no README.md, or a requirement file that requirements/README.md does not list (AGENTS.md, Folders)"
badparts=$(for d in *.d ../SCRUM.d; do [ -f $d/README.md ] || echo "$d: no README.md"; done; for f in $files; do grep -q "$(basename $f)" README.md || echo "$f: not listed in requirements/README.md"; done)
[ -n "$badparts" ] && { echo "$badparts"; err=1; } || echo none
echo "== errors: a README or script named in a process file does not exist (links resolve)"
badlinks=$(for f in ../AGENTS.md ../SCRUM.d/README.md ../tests/README.md ../packages/README.md README.md; do grep -o '[`][A-Za-z0-9_./-]*\(README[.]md\|[.]sh\)[`]' $f | tr -d '`' | sort -u | while read p; do [ -e "../$p" ] || [ -e "$p" ] || [ -e "$(dirname $f)/$p" ] || find .. -name "$(basename $p)" -not -path '../WORKING.d/*' -not -path '../.git/*' | grep -q . || echo "$f: $p"; done; done)
[ -n "$badlinks" ] && { echo "$badlinks"; err=1; } || echo none
echo "== errors: a status went backwards (backlog or blank to proposed) against ${REQ_BASE:-HEAD}"
base=${REQ_BASE:-HEAD}
back=$(for f in $files; do git show "$base:requirements/$f" 2>/dev/null | awk -F'|' '/^[|] [A-Z]+-[0-9]+([.][a-z]+)? [|]/ {i=$2; s=$3; gsub(/ /,"",i); gsub(/ /,"",s); print i" "s}' > /tmp/rc_old.txt; awk -F'|' '/^[|] [A-Z]+-[0-9]+([.][a-z]+)? [|]/ {i=$2; s=$3; gsub(/ /,"",i); gsub(/ /,"",s); print i" "s}' $f > /tmp/rc_new.txt; awk 'NR==FNR {o[$1]=$2; seen[$1]=1; next} ($1 in seen) && $2=="proposed" && o[$1]!="proposed" {print $1}' /tmp/rc_old.txt /tmp/rc_new.txt; done | tr '\n' ' ')
[ -n "$back" ] && { echo "status went backwards: $back"; err=1; } || echo none
[ $err -ne 0 ] && echo "RESULT: errors" || echo "RESULT: no errors"; exit $err
