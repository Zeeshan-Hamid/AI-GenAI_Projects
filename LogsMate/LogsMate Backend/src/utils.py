from src.config import CONFIG, ACTIVE_LOG_TYPE

def apply_severity_bonus(score, severity):
    severity = severity.lower() if severity else "low"
    if severity == "critical":
        return score * 1.2
    elif severity == "high":
        return score * 1.1
    return score

def apply_error_type_bonus(score, error_type):
    if not error_type:
        return score
    error_type_lower = error_type.lower()
    critical_errors = CONFIG.get(ACTIVE_LOG_TYPE, {}).get("critical_errors", [])
    for crit in critical_errors:
        if crit.lower() in error_type_lower:
            return score * 1.05
    return score

def compute_metadata_bonus(doc):
    bonus = 0
    error_code = doc.metadata.get("error_code", "").strip().upper()
    bonus += CONFIG.get("error_code_bonus", {}).get(error_code, 0)
    log_level = doc.metadata.get("log_level", "").strip().lower()
    if log_level == "error":
        bonus += 1.5
    elif log_level == "warn":
        bonus += 1.0
    return bonus
