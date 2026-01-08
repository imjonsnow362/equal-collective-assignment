# X-Ray Architecture

## 1. Overview
X-Ray is a lightweight observability system, X-Ray focuses on **Data Provenance** and **Decision Logic**.

## 2. System Design
The system consists of three components:
1.  **SDK (Python):** A non-blocking wrapper that captures inputs/outputs and samples large datasets.
2.  **API (Django):** An ingest service that normalizes logs into `Runs` and `Steps`.
3.  **Storage (SQLite/Postgres):** A relational DB using JSONB columns for schema flexibility.

### Data Model
I chose a **Hybrid Relational/Document Model**:
* **`PipelineRun` (Relational):** High-level metadata (Time, ID, Pipeline Name). Structured for fast indexing and time-range queries.
* **`PipelineStep` (Document/JSON):** Stores the actual decision data in `JSONField`.
    * *Why?* Different steps (LLM vs. SQL Filter) have vastly different data shapes. A rigid SQL schema would require constant migrations. JSON allows us to log `{"prompt_tokens": 50}` for LLMs and `{"sql_latency": 0.1}` for DBs in the same table.

## 3. Key Design Decisions

### A. Performance & Scale (The "5,000 Candidates" Problem)
Logging full payloads for large datasets (e.g., 5,000 products) is prohibitively expensive.
* **Solution:** The SDK implements **Client-Side Truncation**.
* **Mechanism:** If a list exceeds 10 items, the SDK logs a sample (first 10) and a metadata field `{"total_count": 5000, "truncated": true}`.
* **Trade-off:** We lose 100% fidelity for debugging specific edge cases in the tail, but we preserve system stability and network bandwidth.

### B. Queryability
The API exposes `GET /api/runs/`.
To answer questions like *"Show runs where filtering eliminated >90% of candidates"*:
* **Current MVP:** We fetch the JSON blob and calculate this in Python (Client-side analysis).
* **Production V2:** We would move to PostgreSQL. Postgres allows JSONB indexing, enabling SQL queries like:
    ```sql
    SELECT * FROM core_pipelinestep 
    WHERE metadata->>'dropped_percentage' > 0.90
    ```

### C. Developer Experience
* **Non-Blocking:** The SDK uses Python `threading` to send logs. If the X-Ray API goes down, the main application **must not crash**. The logging fails silently in the background.
* **Minimal Setup:** `xray = XRay(pipeline="name")` is all that is needed.

## 4. Debugging Scenario (Competitor Selection)
**Scenario:** A phone case is matched to a laptop.
1.  **Query:** Developer filters X-Ray for `pipeline_name="competitor_selection"` and `status="success"`.
2.  **Drill Down:** They open the specific Run ID.
3.  **Trace:**
    * *Step 1 (Search):* Inputs: "Laptop". Outputs: [Laptop A, Laptop B, Phone Case]. *Insight: The Search API returned bad data.*
    * *Step 2 (Filter):* Logic: "Price > $10". *Insight: The Phone Case was $15, so it survived the filter. The filter was too loose.*
4.  **Fix:** The developer sees exactly *why* the Phone Case survived (Price Filter) without guessing.
