from flask import Flask, request, jsonify
import re
print("Filter hit:", title)

app = Flask(__name__)

VERSION_INFO = {
    "service": "zap-filter-service",
    "version": "v2.1 – word-boundary matching",
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
        "headquarters","new headquarters","hq","hq moves","head office","new hq","office move","office relocation",
        "sets up office","relocates operations","consolidating offices","shifted base","strategic decision to move",
        "closer to clients","better connected location","improved transport links","co-locating teams",
        "regional hub","new division","builds out team","increased demand for space","access to talent",

        # --- Leasing and tenancy ---
        "lease","leases","leasing","leased","lease signed","new lease","signs lease","long-term lease","pre-let","prelet","pre let",
        "lets space","let","lets","letting","occupancy deal","tenancy secured","agreement with landlord",
        "landlord","new tenant","taking space","occupies space","occupier secured",

        # --- Growth and expansion ---
        "expanding","expand","expands","expansion","growth","grows","scaling up","plans to grow","headcount","new hires",
        "creates jobs","growth plans","larger","next phase","next act","plans to grow","scaling up",

        # --- Construction and development ---
        "construction","development","developments","project","projects","scheme","redevelopment","refurbishment",
        "fit-out","fitout","retrofit","new build","build","builds","building","built","workspace","flexible workspace",
        "facility","facilities","campus","estate","region","new site","new location","new office","new store","new outlet",

        # --- Investment and acquisition ---
        "invest","invests","investing","investment","acquisition","acquisitions","acquire","acquires","acquiring","adds",
        "added","portfolio acquisition","forward purchase","forward funding","sale and leaseback","disposal","divestment",
        "capital partner","joint venture","joint venture partner","backs development","funds scheme","securing finance",
        "raises capital","equity investment","acquires stake","investment vehicle","property fund","real estate fund",
        "asset manager","fund manager","investment trust","pension fund","private equity","sovereign wealth fund",
        "institutional investor","property company","property developer","estate owner","compulsary purchase",

        # --- REIT and institutional names ---
        "reit","ftse","lse-listed","aim-listed","british land","storey","great portland estates","gpe",
        "derwent london","howard de walden estate","howard de walden","the crown estate","cadogan estate","grosvenor","crown estate",
        "portman estate","shaftesbury capital","helical","landsec","canary wharf group","brookfield properties","axa im alts","canary wharf","brookfield",
        "allied london","arup real estate","chelsfield","city of london corporation","city of london","workspace group","landlord london",
        "knight frank","cbre","aviva",
        "legal & general","mitsubishi estate","hb reavis","almacantar",
        "fore partnership","re capital","stanhope","native land","dominvs group","king's cross","kings cross",
        "related argent","howard group","tellon capital","labtech","seaforth land","great western developments",
        "cityhold office partnership","pembroke real estate","quadrant estates","fabrix","greycoat",
        "tishman speyer","hines","northacre","trilogy real estate","orion capital",
        "royal london","capital & counties","capco","helical bar","hb reavis","cls holdings",
        "city developments limited","hanover","sirosa","topland","supermarket income reit",
        "logistics reit","retail reit","student reit",

        # --- Agencies and advisors ---
        "cushman & wakefield","cbre","jll","knight frank","savills","colliers","avison young","bnp paribas real estate","bnp",
        "newton perkins","rx london","brasier freeth","kontor","kirkby diamond","edward charles & partners","edward charles",

        # --- Facilities / FM firms ---
        "mitie","iss uk","sodexo","equans","emcor uk","vinci facilities","cbre gws","bellrock","integral uk",
        "ocs","serco","capita","turner & townsend","faithful+gould","mace operate","aramark","skanska",

        # --- Contractors ---
        "balfour beatty","isg","morgan sindall","kier group","willmott dixon","skanska","sir robert mcalpine",
        "bam construct uk","laing o'rourke","mace","wates group","galliford try","volkerwessels","lendlease",
        "john sisk & son","bouygues","mclaren","overbury","bw workplace experts","tclarke","structuretone",
        "multiplex","oktra","od group","collins construction","modus","fourfront","faithdean","knight harwood",

        # --- Sector types ---
        "logistics park","industrial estate","distribution centre","warehouse","industrial unit","data centre",
        "life sciences","biotech hub","innovation campus","film studio","mixed-use scheme","residential development",
        "build-to-rent","btr","prs","student housing","co-living","hotel","hospitality","care home","retirement village",

        # --- Planning and milestones ---
        "planning permission","planning approved","consent granted","planning application","pre-application",
        "outline consent","construction underway","tops out","completion due","pc achieved","handed over","practical completion",

        # --- Digest markers ---
        "round-up","roundup","weekly roundup","monthly round-up","deal sheet","latest deals","market update",
        "regional update","company moves","property news","openings roundup","sq ft","storey","digest","weekly digest","property digest"
    ]

    matched = []
    for k in keywords:
        pattern = r'\b' + re.escape(k) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            matched.append(k)
    
    is_relevant = len(matched) > 0

    return jsonify({
        "isRelevant": is_relevant,
        "matchedKeywords": matched,
        **VERSION_INFO
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

