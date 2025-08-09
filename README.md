FocusFlow (Local MVP)

What’s included
- Today view with draggable tasks
- Backlog you can drag into Today
- Weekly/daily recurrence generation
- Exercise progression (advances on complete; configurable miss rule)
- Simple analytics: 8-week heatmap and time stats
- Local “morning briefing” text

How to run
- Open `index.html` in your browser. No build, no install.

Tips
- Add quick tasks via the Today view button.
- Add backlog items via the inline input; drag them into Today.
- Click the circle on a task to toggle complete and advance progression tasks.
- Use the date arrows to review past/future days.
- Settings lets you tweak day rollover hour and progression miss behavior.

Data
- Stored in `localStorage` under `focusflow_state_v1`.
- Seeded with your routines and backlog. You can clear storage to reset.

Next steps (when moving to full stack)
- Replace local storage with Supabase (Auth + Postgres + RLS).
- Add per-task percent tracking and timers with actual time capture.
- Add per-task streak views and detailed time vs estimate charts.
- Implement server cron for daily rollovers and AI briefings.
- Add iOS app with offline sync.

