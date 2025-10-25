from flask import Flask, request, jsonify
import re

print("zap-filter-service ready and waiting for incoming RSS items...")

app = Flask(__name__)

VERSION_INFO = {
    "service": "zap-filter-service",
    "version": "v2.2 – simplified substring matcher",
    "description": "Flask prefilter for Zapier RSS relevance"
}

@app.route("/", methods=["GET"])
def version():
    """Return version info for health checks and observability."""
    return jsonify(VERSION_INFO)


@app.route("/filter_keywords", methods=["POST"])
def filter_keywords():
    """Evaluate RSS title + description for relevance based on keyword list."""
    data = request.get_json(force=True)
    title = (data.get("title") or "").lower()
    description = (data.get("description") or "").lower()
    text = f"{title} {description}"
    print("Filter hit:", title)

    # Massive keyword list ported from Zapier JS
    keywords = [
        # --- New developments ---
        "new hq","new headquarters","new head-quarters","new office","new site","new location","new store","new outlet",
        "new facility","new building","new campus","new space","new workspace","new premises","new studio",
        "new distribution","new warehouse","new development","new scheme",
        "new project","new division","new hub","new branch","new regional office","new production site",
        "new logistics park","new innovation centre","new science park","new headquarters building",
        "new london office","new uk hq","new european hq","new company office",

        # --- Occupier and movement ---
        "relocating","relocation","relocate","relocates","move","moves","moving","move-in","move-out","move office","move hq",
        "headquarters","office move","office relocation","sets up office","relocates operations","consolidating offices",
        "regional hub","builds out team","increased demand for space","access to talent",

        # --- Leasing and tenancy ---
        "lease","leases","leasing","leased","new lease","signs lease","pre-let","prelet","taking space","new tenant",

        # --- Growth and expansion ---
        "expanding","expand","expands","expansion","growth","grows","creates jobs","headcount","new hires",

        # --- Construction and development ---
        "construction","development","scheme","redevelopment","refurbishment","fit-out","fitout","retrofit",
        "workspace","facility","facilities","campus","estate","region",

        # --- Investment and acquisition ---
        "invest","invests","investing","investment","acquisition","acquire","acquires","funds scheme","backs development",
        "joint venture","real estate fund","asset manager","fund manager","property company","property developer",
        "reit","landlord","pension fund","investment trust","institutional investor","private equity",

        # --- Names and advisors ---
        "cbre","jll","savills","knight frank","avison young","bnp paribas real estate","cushman & wakefield",
        "british land","landsec","derwent london","canary wharf","grosvenor","helical","brookfield","axa im alts",
        "legal & general","aviva","hines","tishman speyer","mace","skanska","isg","balfour beatty","morgan sindall",

        # --- Sector types ---
        "logistics park","industrial estate","distribution centre","warehouse","data centre","life sciences",
        "innovation campus","film studio","mixed-use scheme","residential development","student housing","hotel",

        # --- Planning and milestones ---
        "planning permission","planning approved","consent granted","planning application","construction underway",
        "completion due","practical completion",

        # --- Digest markers ---
        "round-up","roundup","weekly roundup","monthly round-up","deal sheet","market update","property news","digest"
    ]

    matched = [k for k in keywords if k.lower() in text]
    is_relevant = bool(matched)

    return jsonify({
        "isRelevant": is_relevant,
        "matchedKeywords": matched,
        **VERSION_INFO
    })


print("=== REGISTERED ROUTES ON STARTUP ===")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule} [{','.join(rule.methods)}]")
print("=====================================")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
