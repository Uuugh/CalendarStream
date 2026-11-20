"""Check the consolidated CSS components without adding a package dependency.

Checks duplicate selector/property definitions within the same conditional context and component ownership.
This intentionally covers the migrated components, not unused selectors or every legacy CSS file.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OWNERS = {
    'calhead': '19-calendar-header.css', 'calright': '19-calendar-header.css',
    'monthwrap': '19-calendar-header.css', 'viewwrap': '19-calendar-header.css',
    'navbtn': '19-calendar-header.css',
    'monthpick': '13-dropdowns.css', 'viewmenu': '13-dropdowns.css', 'langmenu': '13-dropdowns.css',
}


def split_top(text, delimiter):
    parts, start, quote, depth, escaped = [], 0, '', 0, False
    for i, char in enumerate(text):
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif quote:
            if char == quote:
                quote = ''
        elif char in "\"'":
            quote = char
        elif char in '([':
            depth += 1
        elif char in ')]':
            depth -= 1
        elif char == delimiter and depth == 0:
            parts.append(text[start:i].strip()); start = i + 1
    parts.append(text[start:].strip())
    return parts


def blocks(text):
    """Yield balanced CSS blocks; comments are removed by the caller, strings kept intact."""
    start, opening, depth, quote, escaped = 0, None, 0, '', False
    for i, char in enumerate(text):
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif quote:
            if char == quote:
                quote = ''
        elif char in "\"'":
            quote = char
        elif char == '{':
            if depth == 0:
                opening = i
            depth += 1
        elif char == '}':
            depth -= 1
            if depth < 0:
                raise ValueError('unbalanced closing brace')
            if depth == 0:
                yield text[start:opening].strip(), text[opening + 1:i]
                start = i + 1
    if depth or quote or text[start:].strip():
        raise ValueError('unbalanced or trailing CSS')


def rules(text, context=()):
    for selector, body in blocks(text):
        if selector.startswith('@'):
            yield from rules(body, context + (selector,))
        else:
            yield context, selector, body


def check(root=ROOT):
    errors = []
    for path in sorted((root / 'app/styles').glob('*.css')):
        text = re.sub(r'/\*.*?\*/', '', path.read_text(), flags=re.S)
        # Shared print visibility is the sole cross-component ownership exception.
        # It may only hide controls; ordinary component declarations still belong to their owner.
        for context, selector, body in rules(text):
            for cls, owner in OWNERS.items():
                if path.name == owner or not re.search(r'\.' + re.escape(cls) + r'(?![\w-])', selector):
                    continue
                shared_print = (path.name == '09-spacing-print.css' and '@media print' in context
                                and re.fullmatch(r'\s*display\s*:\s*none\s*!important\s*;?\s*', body))
                if not shared_print:
                    errors.append(f'{path.name}: .{cls} belongs in {owner}')
        if path.name not in set(OWNERS.values()):
            continue
        definitions = set()
        try:
            for context, selector, body in rules(text):
                for declaration in split_top(body, ';'):
                    if not declaration:
                        continue
                    property_, sep, value = declaration.partition(':')
                    if not sep or not value.strip():
                        errors.append(f'{path.name}: invalid declaration {declaration!r}')
                    for single in split_top(selector, ','):
                        key = (context, re.sub(r'\s+', ' ', single), property_.strip().lower())
                        if key in definitions:
                            errors.append(f'{path.name}: repeated {single} / {property_.strip()} in {context or "base"}')
                        definitions.add(key)
        except ValueError as exc:
            errors.append(f'{path.name}: {exc}')
    return errors


if __name__ == '__main__':
    findings = check()
    print('\n'.join(findings) if findings else 'CSS component checks passed')
    sys.exit(bool(findings))
