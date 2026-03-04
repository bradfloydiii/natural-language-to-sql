# You’re not letting the model emit raw SQL (reduces injection risk).
# You’re using a constrained “plan” that you compile.

from pydantic import BaseModel, Field
from typing import List, Literal, Optional

ALLOWED_TABLES = {"people", "aliases", "identifiers", "incidents", "incident_people"}
ALLOWED_COLUMNS = {
    "people": {"id", "first_name", "last_name"},
    "aliases": {"person_id", "alias"},
    "identifiers": {"person_id", "type", "value"},
    "incidents": {"id", "incident_date", "description", "offense_code"},
    "incident_people": {"incident_id", "person_id", "role"},
}

class SQLPlan(BaseModel):
    """
    The LLM is asked to output a constrained plan, not arbitrary SQL.
    We compile it into SQL ourselves.
    """
    person_name: Optional[str] = None
    alias: Optional[str] = None
    days_back: int = 30
    include_ident_types: List[str] = Field(default_factory=lambda: ["PLATE"])
    role: Optional[str] = None  # e.g., "SUSPECT", "VICTIM"

def compile_plan_to_sql(plan: SQLPlan) -> tuple[str, dict]:
    # Simple, safe compilation. No free-form SQL from the model.
    where = []
    params = {"days_back": plan.days_back}

    # Person match
    if plan.person_name:
        # naive split for demo; in real: more robust parsing
        parts = plan.person_name.strip().split()
        params["first_name"] = parts[0]
        params["last_name"] = parts[-1]
        where.append("(p.first_name = :first_name AND p.last_name = :last_name)")

    if plan.alias:
        params["alias"] = plan.alias
        where.append("a.alias = :alias")

    if plan.role:
        params["role"] = plan.role
        where.append("ip.role = :role")

    # Identifiers filter
    params["ident_types"] = list(plan.include_ident_types)

    sql = f"""
    SELECT
      i.id as incident_id,
      i.incident_date,
      i.offense_code,
      i.description,
      p.first_name,
      p.last_name,
      a.alias,
      idf.type as identifier_type,
      idf.value as identifier_value,
      ip.role
    FROM incidents i
    JOIN incident_people ip ON ip.incident_id = i.id
    JOIN people p ON p.id = ip.person_id
    LEFT JOIN aliases a ON a.person_id = p.id
    LEFT JOIN identifiers idf ON idf.person_id = p.id
    WHERE
      date(i.incident_date) >= date('now', '-' || :days_back || ' days')
      AND ({' OR '.join(where) if where else '1=1'})
      AND (idf.type IN :ident_types OR idf.type IS NULL)
    ORDER BY i.incident_date DESC
    LIMIT 50
    """
    return sql, params

def llm_extract_plan(user_text: str) -> SQLPlan:
    """
    Demo stub. In production, this would call Bedrock Claude/Titan
    with a JSON schema requirement and examples.
    """
    txt = user_text.lower()
    plan = SQLPlan()

    if "red" in txt:
        plan.alias = "Red"
    if "john" in txt and "smith" in txt:
        plan.person_name = "John Smith"
    if "plate" in txt or "vehicle" in txt:
        plan.include_ident_types = ["PLATE"]
    if "suspect" in txt:
        plan.role = "SUSPECT"
    if "7 days" in txt:
        plan.days_back = 7

    return plan