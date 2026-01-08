# demo_app.py
import time
import random
from xray_sdk import XRay

# Initialize SDK
xray = XRay(pipeline_name="amazon_competitor_v1")
xray.start()

# Mock Data: 50 candidates
candidates = [{"id": i, "name": f"Product_{i}", "price": random.randint(10, 100), "category": "electronics"} for i in range(50)]
candidates.append({"id": 999, "name": "Phone Case", "price": 15, "category": "accessories"}) # The "bad" match

# --- Step 1: Search ---
print("Running Search...")
xray.log(
    step_name="Search Retrieval",
    step_type="API",
    inputs={"query": "Laptop Stand"},
    outputs=candidates, # SDK will truncate this automatically
    reasoning="Retrieved from Catalog API"
)

# --- Step 2: Filter (The Buggy Step) ---
# Logic: We want Laptops ($50+), but we accidentally keep cheap items if they look cool
filtered = []
for c in candidates:
    if c['price'] > 50 or "Case" in c['name']: 
        filtered.append(c)

print("Running Filter...")
xray.log(
    step_name="Price Filter",
    step_type="FILTER",
    inputs={"count": len(candidates)},
    outputs=filtered,
    reasoning="Kept items > $50 OR items with 'Case' in name (Bug?)"
)

# --- Step 3: LLM Rank ---
# Simulating an LLM picking the wrong item
winner = filtered[-1] # It picks the Phone Case because it's the last one
print(f"Winner selected: {winner['name']}")

xray.log(
    step_name="LLM Ranking",
    step_type="LLM",
    inputs=[c['id'] for c in filtered],
    outputs=winner,
    reasoning="LLM selected this as best match based on visual appeal"
)

print("Done! Check Django Admin.")