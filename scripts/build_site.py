"""Build the committed, dependency-free static project site."""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site"
PAPER_URL = "https://github.com/sanandani/ace-u-trust-framework/blob/main/paper/%5BPaper%5D%20IEEE%20SoutheastCon%20-%20Trust-Aware%20Professional%20Identity%20Representation%20in%20AI-Mediated%20Systems.pdf"


def read_dimensions():
    source = (ROOT / "docs/framework.md").read_text(encoding="utf-8")
    rows = []
    for line in source.splitlines():
        if line.startswith("| ") and not line.startswith("| Dimension") and not line.startswith("|---"):
            cols = [part.strip() for part in line.strip("| ").split("|")]
            if len(cols) == 3:
                rows.append(cols)
    if len(rows) != 4:
        raise ValueError("Expected four ACE-U dimension rows in docs/framework.md")
    return "\n".join(
        f'<article class="dimension"><h3>{escape(name)}</h3><p>{escape(description)}</p><p><strong>Signals:</strong> {escape(signals)}</p></article>'
        for name, description, signals in rows
    )


def page(title, content):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Synthetic-only ACE-U conceptual reference implementation."><title>{escape(title)} | ACE-U Trust Framework</title>
<link rel="stylesheet" href="styles.css"></head><body><header class="top"><a class="brand" href="index.html">ACE-U Trust Framework</a><nav><a href="index.html">Overview</a><a href="evaluation.html">Synthetic evaluation</a><a href="https://github.com/sanandani/ace-u-trust-framework">GitHub</a></nav></header>
{content}<footer><p>Conceptual reference implementation · Synthetic data only · Not empirically validated</p></footer></body></html>'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    abstract_match = re.search(r"## Abstract\s+(.*?)\s+## Citation", readme, re.S)
    if not abstract_match:
        raise ValueError("README abstract section missing")
    abstract = escape(abstract_match.group(1).strip())
    dimensions = read_dimensions()
    index = f'''<main><section class="hero"><p class="eyebrow">Conceptual framework · Synthetic reference implementation</p><h1>Trust-aware professional identity for AI-mediated systems</h1>
<p class="scope">Synthetic data only. This implementation follows the conceptual paper's Section VI architecture and evaluation pathway. It has not been empirically validated and never uses real people's profiles.</p>
<h2>Abstract</h2><p>{abstract}</p><p class="links"><a href="{PAPER_URL}">Read the paper (accepted manuscript)</a><a href="https://github.com/sanandani/ace-u-trust-framework">Source repository</a><a href="https://imshubh.com/blog.html">Oracle ACE series</a><a href="https://raw.githubusercontent.com/sanandani/ace-u-trust-framework/main/CITATION.cff">Citation</a></p></section>
<section><h2>Four dimensions</h2><div class="grid">{dimensions}</div></section>
<section><h2>Four-layer reference architecture</h2><div class="architecture" role="img" aria-label="Data ingestion to feature extraction to ACE-U estimation to application endpoints"><div>Data ingestion<small>Synthetic profiles</small></div><b aria-hidden="true">→</b><div>Feature extraction<small>Authenticity · Credibility · Empathy · Uniqueness</small></div><b aria-hidden="true">→</b><div>ACE-U estimation<small>Vector · uncertainty · explanation</small></div><b aria-hidden="true">→</b><div>Application endpoints<small>Ranking · evaluation · audit</small></div></div></section>
<section><h2>Oracle technology</h2><ul><li>Oracle Database 23ai Free</li><li>python-oracledb</li><li>Oracle AI Vector Search with VECTOR and VECTOR_DISTANCE</li><li>Oracle Unified Auditing</li><li>Deterministic offline bag-of-skills embedding by default; optional OCI adapter</li></ul></section></main>'''
    report_path = ROOT / "eval/REPORT.md"
    report = report_path.read_text(encoding="utf-8") if report_path.exists() else "Synthetic evaluation report has not been generated yet."
    report_html = escape(report)
    evaluation = f'''<main><section class="hero"><p class="eyebrow">Offline simulation</p><h1>Synthetic evaluation</h1><p class="scope">Synthetic data, not empirical validation. The generated scores are illustrative harness outputs, not evidence of effectiveness on real people or systems.</p>
<pre class="report">{report_html}</pre></section></main>'''
    (OUT / "index.html").write_text(page("Overview", index), encoding="utf-8")
    (OUT / "evaluation.html").write_text(page("Synthetic evaluation", evaluation), encoding="utf-8")
    (OUT / "404.html").write_text(page("Page not found", '<main><section class="hero"><h1>Page not found</h1><p>The page may have moved. Return to the <a href="index.html">project overview</a>.</p></section></main>'), encoding="utf-8")
    (OUT / "styles.css").write_text('''
:root{color-scheme:light;--ink:#14213d;--muted:#526078;--accent:#b54708;--paper:#fff;--wash:#f3f6fa;--line:#d9e0e9}*{box-sizing:border-box}body{margin:0;background:var(--wash);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}.top{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1rem max(1.2rem,calc((100% - 1080px)/2));background:var(--paper);border-bottom:1px solid var(--line)}a{color:#8c3100}.brand{font-weight:750;text-decoration:none;color:var(--ink)}nav{display:flex;gap:1rem;flex-wrap:wrap}main{max-width:1080px;margin:auto;padding:2rem 1.2rem 4rem}section{margin:2rem 0;padding:1.5rem;background:var(--paper);border:1px solid var(--line);border-radius:14px}.hero{padding:2rem}.eyebrow{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:.8rem}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.1;max-width:850px}h2{margin-top:0}.scope{padding:1rem;border-left:4px solid var(--accent);background:#fff5eb;font-weight:650}.links{display:flex;gap:.8rem;flex-wrap:wrap}.links a{padding:.4rem .7rem;border:1px solid var(--line);border-radius:7px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.dimension{padding:1rem;border:1px solid var(--line);border-radius:10px;background:#fbfcfe}.dimension h3{margin:.1rem 0;color:var(--accent)}.architecture{display:flex;align-items:center;justify-content:center;gap:.7rem;flex-wrap:wrap}.architecture div{flex:1 1 170px;min-height:95px;padding:1rem;border-radius:10px;background:#eaf0fa;font-weight:700;text-align:center}.architecture small{display:block;font-weight:400;color:var(--muted)}.architecture b{color:var(--accent);font-size:1.5rem}.report{white-space:pre-wrap;overflow-wrap:anywhere;background:#f8fafc;border:1px solid var(--line);border-radius:8px;padding:1rem;font: .9rem/1.6 ui-monospace,SFMono-Regular,Consolas,monospace}footer{text-align:center;padding:1rem;color:var(--muted)}@media(max-width:620px){.top{align-items:flex-start;flex-direction:column}.grid{grid-template-columns:1fr}.architecture{align-items:stretch;flex-direction:column}.architecture b{transform:rotate(90deg);text-align:center}}
'''.strip()+"\n", encoding="utf-8")
    (OUT / "staticwebapp.config.json").write_text('''{
  "navigationFallback": { "rewrite": "/404.html", "exclude": ["/styles.css", "/*.pdf"] },
  "responseOverrides": { "404": { "rewrite": "/404.html", "statusCode": 404 } },
  "globalHeaders": {
    "Content-Security-Policy": "default-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
  }
}
''', encoding="utf-8")


if __name__ == "__main__":
    main()
