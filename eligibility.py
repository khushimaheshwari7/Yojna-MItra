"""
Eligibility Engine
==================
Evaluates a user profile against a scheme's eligibility_rules JSON.

Rules are a list of condition objects:
  { "field": str, "operator": str, "value": any, "label": str, "required": bool }

Operators:
  eq, neq, gt, gte, lt, lte     — numeric / string equality / comparison
  in, not_in                    — value (list) membership
  contains                      — user extras list contains string
  contains_any                  — user extras list contains any in list
  any                           — always true (informational / open-to-all)

Status classification:
  eligible      — all required criteria met
  almost        — exactly 1 required criterion unmet
  not_eligible  — 2+ required criteria unmet (or income / age way off)
"""

import json


# ─── Operator evaluators ────────────────────────────────────────────────────

def _eval(rule, user):
    field    = rule["field"]
    operator = rule["operator"]
    value    = rule["value"]
    uval     = user.get(field)

    if operator == "any":
        return True
    if operator == "eq":
        return str(uval).lower() == str(value).lower() if uval is not None else False
    if operator == "neq":
        return str(uval).lower() != str(value).lower() if uval is not None else True
    if operator == "gt":
        try: return float(uval) > float(value)
        except: return False
    if operator == "gte":
        try: return float(uval) >= float(value)
        except: return False
    if operator == "lt":
        try: return float(uval) < float(value)
        except: return False
    if operator == "lte":
        try: return float(uval) <= float(value)
        except: return False
    if operator == "in":
        return str(uval).lower() in [str(v).lower() for v in value] if uval else False
    if operator == "not_in":
        return str(uval).lower() not in [str(v).lower() for v in value] if uval else True
    if operator == "contains":
        extras = uval if isinstance(uval, list) else []
        return value in extras
    if operator == "contains_any":
        extras = uval if isinstance(uval, list) else []
        return any(v in extras for v in value)
    return False


# ─── Main evaluator ─────────────────────────────────────────────────────────

def evaluate(scheme_row, user_profile):
    """
    Returns a dict:
      {
        "status":        "eligible" | "almost" | "not_eligible",
        "criteria":      [ { label, met, required } ],
        "missing":       [ label of required unmet ],
        "met_count":     int,
        "total":         int
      }
    """
    rules = json.loads(scheme_row["eligibility_rules"])
    criteria = []

    for rule in rules:
        met = _eval(rule, user_profile)
        criteria.append({
            "label":    rule["label"],
            "met":      met,
            "required": rule["required"]
        })

    required_unmet = [c for c in criteria if c["required"] and not c["met"]]
    met_count      = sum(1 for c in criteria if c["met"])
    total          = len(criteria)

    if len(required_unmet) == 0:
        status = "eligible"
    elif len(required_unmet) == 1:
        status = "almost"
    else:
        status = "not_eligible"

    return {
        "status":    status,
        "criteria":  criteria,
        "missing":   [c["label"] for c in required_unmet],
        "met_count": met_count,
        "total":     total
    }
