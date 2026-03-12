**High-Level Architecture**

**Overview**
TraceTruth is a local Python desktop app that captures writing events from a student editor, stores them in SQLite, and provides reviewer tools to inspect the writing process, detect paste behavior, replay creation, and visualize a concept map.

**Core Modules**
1. **GUI Shell (PySide6)**
   - `LoginWindow`: Authenticates user, loads role-specific view.
   - `StudentEditorWindow`: Hosts the writing editor and session controls.
   - `ReviewerDashboardWindow`: Loads document review panels.

2. **Editor + Event Capture**
   - `TraceEditor` (subclass of `QTextEdit`) intercepts:
     - `keyPressEvent` → KEYPRESS
     - `insertFromMimeData` → PASTE
     - Delete/backspace via key events
     - Save actions via explicit UI handlers
   - Sends events to `EventLogger`.

3. **Event Logger**
   - Normalizes editor events into a consistent schema.
   - Attaches `session_id`, timestamps, cursor/selection state.
   - Persists to `events` table.

4. **Session Manager**
   - Creates and closes `sessions`.
   - Tracks `start_time`, `end_time`, and metadata (device/app version).
   - Associates the active `document` to the session.

5. **Data Access Layer (SQLite)**
   - Central `database.py` exposes:
     - `create_schema()`
     - `log_event()`
     - `start_session()`, `end_session()`
     - `save_document()`, `load_document()`
   - Encapsulates all SQL statements and migrations.

6. **Reviewer Analytics**
   - **Paste Detector**: Flags large paste events by length threshold.
   - **Timeline Analyzer**: Computes activity bursts, pauses, and total duration.
   - **Process Replay**: Reconstructs text state from event stream.
   - **Mind Map Generator**: Extracts keywords with spaCy and builds a graph with NetworkX → rendered via PyVis/Plotly.

**Data Flow**
1. Student logs in → `StudentEditorWindow`.
2. Session starts → `sessions` row created.
3. Editor events captured → `events` table.
4. On save/close → `documents` updated, session closed.
5. Reviewer selects a submission → loads `documents`, `events`, and derived analytics.
6. Reviewer views:
   - Final text
   - Paste flags
   - Timeline
   - Replay
   - Mind map graph

**Database Schema (Conceptual)**
- `users`: auth and role
- `sessions`: per writing session
- `documents`: final text + session linkage
- `events`: raw keystroke/paste/delete stream
- Optional derived tables: `analysis_summary`, `paste_flags`, `mindmap_nodes`, `mindmap_edges`

**Runtime Boundaries**
- UI thread: PySide6 event loop and view rendering.
- Background work: analytics computations and mind map generation to avoid UI freezes.
- Storage: local SQLite file in `database/events.db`.

**Non-Functional Considerations**
- Performance: event logging must be lightweight and buffered if needed.
- Security: passwords stored with bcrypt hashes.
- Reliability: session end should be written even on unexpected exit.

**Roadmap Mapping**
1. Editor UI + event capture
2. SQLite schema + logging
3. Session tracking
4. Reviewer dashboard
5. Replay + timeline
6. Mind map generation
7. Login system
