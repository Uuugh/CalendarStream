# UI/UX Design Standards

## 1. Purpose and authority

Apply these requirements to all CalendarStream web interfaces and future mobile clients. This file governs usability, accessibility, information architecture, and interaction quality. `build_rules/theme.md` remains authoritative for exact visual tokens, spacing, typography, component dimensions, status meanings, animations, and documented Developer decisions. Do not silently change established design rules. Where requirements appear to conflict, flag the conflict to the Developer during PLAN; do not invent a new visual system.

## 2. Standards baseline

- ISO 9241-110:2020 — interaction principles: suitability for tasks, self-descriptiveness, conformity with user expectations, learnability, controllability, error robustness, and engagement.
- ISO 9241-210 — human-centred design: evaluate workflows in the context of real user tasks and iterate using evidence.
- ISO 9241-11 — usability evaluated by effectiveness, efficiency, and satisfaction in a stated context.
- ISO/IEC 25010:2023 — product quality model, including interaction capability and related quality characteristics.
- WCAG 2.2 Level AA — accessibility acceptance baseline for applicable web content and controls.
- WAI-ARIA Authoring Practices Guide — implementation patterns for custom interactive controls.
- Nielsen Norman Group's ten usability heuristics — supplementary inspection checklist, not a formal ISO/IEEE standard.

These references inform project requirements; do not claim ISO certification or complete WCAG conformance without an actual assessment. If a normative standard is paywalled, use its publicly available descriptions and do not invent clause-specific mandates.

## 3. Mandatory design requirements

1. **Consistency:** Reuse existing CalendarStream controls, labels, placement, and behavior. Before adding a component, identify its closest existing counterpart in `theme.md`.
2. **Task clarity:** The primary action, current state, and next step must be identifiable without guessing. Keep user-facing instructions short, following `theme.md` section 13.
3. **Navigation and orientation:** Show the current context; preserve logical focus and navigation order after transitions and redraws.
4. **User control:** Provide Cancel where appropriate, and confirmation or recovery for destructive actions. Preserve established History/Undo and removal flows.
5. **Feedback:** Every user action has an observable state or result. Follow `theme.md` status/action meanings and timing; do not add competing color semantics.
6. **Error prevention and recovery:** Validate at the appropriate point, explain the problem in actionable language, preserve user-entered values, and never silently discard work.
7. **Accessibility:** Support keyboard-only operation, visible focus, meaningful labels and accessible names, semantic roles, status announcements, and non-color cues. Use native controls where practical; custom controls must follow appropriate ARIA patterns. A control revealed on hover also appears on keyboard focus and on touch screens, and has a keyboard alternative.
8. **Contrast and readability:** Test text, controls, and focus indicators against applicable WCAG 2.2 AA criteria in both themes, including tinted calendar/feed modules. Do not rely on color alone.
9. **Responsive behavior:** Test at desktop and the established 390 px phone viewport; avoid unintended horizontal scrolling.
10. **Motion:** Honor `prefers-reduced-motion: reduce` exactly as required by `theme.md`; essential state information remains available without animation. Motion that starts on its own stops within 5 seconds or can be paused (WCAG 2.2.2); the state it shows stays visible without motion.
11. **Efficiency:** Avoid unnecessary steps, repeated entry, unexpected context switches, and unnecessary confirmation for reversible low-risk actions.
12. **Localization:** Avoid hard-coded interface strings. Translated text, date/time formats, clipping, and accessible names in supported languages are checked at DEPLOY (`5-deploy.md`), not in each beta.
13. **Data and privacy:** Do not expose sensitive calendar, account, or credential data in screenshots, client-side errors, logs, or test fixtures. Follow `0-overview.md` ground rules.

## 4. CalendarStream-specific applications

- **Calendar/feed modules:** Preserve the established 50 px header, section/module borders, selected-color tinting, expand/close placement, and status/action controls. A color choice never replaces a textual status.
- **Event editing:** Keep fields aligned consistently, associate each label with its input, preserve unsaved edits on validation errors, and use the established Cancel/Save interaction.
- **Dialogs and dropdowns:** Manage initial focus, keyboard dismissal where appropriate, focus containment for modal dialogs, and focus restoration to the invoking control. Preserve `theme.md` dimensions and transitions.
- **Calendar views:** Distinguish selected, current, modified, deleted, and conflicting events with accessible text or symbols in addition to color. Ensure event details are reachable by keyboard.
- **Sync and import:** Expose progress, outcomes, external-service errors, and recoverable actions using the established green/pressed/amber/red status meanings. Preserve the established date-range and import layout.
- **Inactive controls:** A control that does nothing is `disabled` (greyed, not focusable, announced as unavailable). A control that can be pressed meets contrast.
- **Light/dark/system themes:** Verify every new state in both palettes and the system-selected theme; use centralized tokens, never one-off colors.

## 5. Review and acceptance

For each UI change, document the user task, affected views/states, existing component reused, applicable accessibility criteria, and tests. Check normal, empty, loading, error, success, and post-redraw states as relevant. Verify keyboard navigation, focus order, focus visibility, labels, contrast, reduced motion, phone layout, and both themes. Include automated checks where reliable and manual inspection where automation cannot establish usability or accessibility.

Use the existing `tests/suite_44.py` theme suite, `tests/run.sh`, and before/after screenshot workflow required by `build_rules/2-build.md`. Add regression coverage for new requirements; do not weaken existing checks to make a change pass. Report findings with severity (High, Medium or Low as `4-review.md` defines them: a failed WCAG 2.2 AA criterion that users would hit is Medium, anything else Low), reproducible steps, expected versus observed behavior, and a standards/design-rule reference. Distinguish a genuine standards violation from a subjective preference.

## 6. Change management

This document is a project-specific interpretation of standards, not a replacement for them. Changes to exact visual appearance or interaction timing require corresponding updates to `build_rules/theme.md`, its Theme Rules pictures, and the relevant tests, following existing repository workflow. New rules or conflicts require Developer approval through the Dashboard's PLAN/BUILD process.
