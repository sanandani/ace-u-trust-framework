"""Apply schema to an Oracle 23ai Free instance and verify key objects."""
import os
from pathlib import Path
import oracledb

def statements():
    lines=[line for line in Path(__file__).with_name('schema.sql').read_text().splitlines() if not line.lstrip().startswith('--')]
    out=[]; buf=[]; is_pl=False
    for line in lines:
        if not buf and not line.strip(): continue
        if not buf: is_pl=line.lstrip().upper().startswith('CREATE OR REPLACE FUNCTION')
        if line.strip()=='/' and is_pl:
            out.append('\n'.join(buf)); buf=[]; is_pl=False; continue
        if not is_pl and ';' in line:
            parts=line.split(';')
            for part in parts[:-1]:
                buf.append(part)
                stmt='\n'.join(buf).strip()
                if stmt: out.append(stmt)
                buf=[]
            if parts[-1].strip(): buf.append(parts[-1])
        else: buf.append(line)
    if buf and '\n'.join(buf).strip(): out.append('\n'.join(buf).strip())
    return out

def main():
    conn=oracledb.connect(user=os.environ['ORACLE_USER'], password=os.environ['ORACLE_PASSWORD'], dsn=os.environ.get('ORACLE_DSN','localhost:1521/FREEPDB1'))
    cur=conn.cursor()
    for statement in statements(): cur.execute(statement)
    cur.execute("SELECT table_name FROM user_tables WHERE table_name IN ('PROFILES','ARTIFACTS','SIGNALS','SCORES','CONTEST_LOG')")
    assert len(cur.fetchall())==5
    conn.close()
    admin=oracledb.connect(user=os.environ.get('ORACLE_ADMIN_USER','system'), password=os.environ['ORACLE_ADMIN_PASSWORD'], dsn=os.environ.get('ORACLE_DSN','localhost:1521/FREEPDB1'))
    ac=admin.cursor()
    try: ac.execute('CREATE AUDIT POLICY aceu_score_read_policy ACTIONS SELECT ON aceu.scores')
    except oracledb.DatabaseError as exc:
        if 'ORA-00955' not in str(exc): raise
    ac.execute('AUDIT POLICY aceu_score_read_policy')
    ac.execute("SELECT policy_name FROM audit_unified_policies WHERE policy_name='ACEU_SCORE_READ_POLICY'")
    assert ac.fetchone()
    admin.close()
if __name__=='__main__': main()
