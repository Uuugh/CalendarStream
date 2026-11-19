# Requirements: plugins

This file establishes the rules for creating a plugin module: what every plugin does and what each one must state in its own file in `plugins.d/`, and nothing else that is common. A plugin is what a connection requires before it can work (CON-01.b); connections are in connections.md.

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| PLG-01 | backlog | A plugin is set up once and shared by every connection that requires it. | — | — |
