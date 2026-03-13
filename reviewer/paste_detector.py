from utils.time_utils import format_ts


def detect_pastes(events, min_length=20):
    results = []
    for ts, event_type, content, _, _, _ in events:
        if event_type == "PASTE" and content:
            if len(content) >= min_length:
                results.append({
                    "timestamp": ts,
                    "time_str": format_ts(ts),
                    "length": len(content),
                    "content": content,
                })
    return results
