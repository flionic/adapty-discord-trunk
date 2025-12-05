def humanize_event(s: str) -> str:
    return " ".join(word.capitalize() for word in s.replace("_", " ").split())