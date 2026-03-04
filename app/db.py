from sqlalchemy import create_engine, text, bindparam

ENGINE = create_engine("sqlite:///./clemis_demo.db", future=True)

def run_query(sql: str, params: dict):
    stmt = text(sql)

    # Apply expanding bind param when ident_types is used
    if "ident_types" in params:
        stmt = stmt.bindparams(bindparam("ident_types", expanding=True))

    with ENGINE.connect() as conn:
        rows = conn.execute(stmt, params).mappings().all()
        return [dict(r) for r in rows]