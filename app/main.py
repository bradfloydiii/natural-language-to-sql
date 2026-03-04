from fastapi import FastAPI
from pydantic import BaseModel
from app.nl2sql import llm_extract_plan, compile_plan_to_sql
from app.db import run_query
from app.masking import mask_row, mask_text
from app.rag import SimpleRAG
import json
from fastapi.responses import Response


app = FastAPI(title="CLEMIS NLQ + RAG Demo")

# Load tiny "policy docs"
POLICY_DOCS = [
    ("policy_alias", "Aliases should be matched case-insensitively. An alias indicates known nickname(s)."),
    ("policy_involving", "Involving means linked via incident_people relationship. Roles include SUSPECT, VICTIM, WITNESS."),
    ("policy_pii", "PII/CJIS fields must be redacted before external processing. Use tokens for correlation where needed."),
]
rag = SimpleRAG(POLICY_DOCS)

class QueryRequest(BaseModel):
    q: str

@app.post("/query")
def query(req: QueryRequest):
    user_q = mask_text(req.q)

    plan = llm_extract_plan(user_q)
    sql, params = compile_plan_to_sql(plan)
    rows = run_query(sql, params)

    masked_rows = [mask_row(r) for r in rows]
    ctx = rag.retrieve(user_q, k=3)

    payload = {
        "input": user_q,
        "plan": plan.model_dump(),
        "sql_preview": sql.strip(),
        "results": masked_rows,
        "rag_context": [{"doc_id": d, "score": s, "content": c} for d, c, s in ctx],
    }

    return Response(
        content=json.dumps(payload, indent=2),
        media_type="application/json"
    )