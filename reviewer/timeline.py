from utils.time_utils import format_ts


def analyze_timeline(events, pause_threshold_sec=60):
    if not events:
        return []

    timestamps = [e[0] for e in events]
    start = min(timestamps)
    end = max(timestamps)
    total_duration = end - start

    pauses = []
    last_ts = timestamps[0]
    for ts in timestamps[1:]:
        gap = ts - last_ts
        if gap >= pause_threshold_sec:
            pauses.append((last_ts, ts, gap))
        last_ts = ts

    lines = [
        f"Session start: {format_ts(start)}",
        f"Session end: {format_ts(end)}",
        f"Total duration: {int(total_duration)} seconds",
        f"Total events: {len(events)}",
    ]

    if pauses:
        lines.append("Pauses:")
        for p_start, p_end, gap in pauses:
            lines.append(f"- {format_ts(p_start)} to {format_ts(p_end)} ({int(gap)}s)")
    else:
        lines.append("Pauses: none detected")

    return lines
