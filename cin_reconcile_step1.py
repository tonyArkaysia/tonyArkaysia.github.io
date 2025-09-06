
#!/usr/bin/env python3
"""
CIN Step 1: Reconcile JSON sources & produce seed CSVs

Usage:
  python cin_reconcile_step1.py --strain /path/to/strain_db.json --tiers /path/to/neuroterp_matrix_tiers.json --out ./out

What it does:
  • Reads both JSON files (robust to different wrappers)
  • Summarizes structure (keys, counts)
  • Guesses columns for brand/strain/category/product_type/SKU
  • Extracts distinct Brands, Strains, Products -> CSVs
  • Extracts NeuroTerp tiers/tags -> CSVs if present
  • Checks for mismatches: unknown tier codes, dupes, nulls
  • Writes a reconciliation report (report.txt)
"""
import argparse, json, os, sys
from collections import defaultdict, Counter
from datetime import datetime
import pandas as pd

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_records(obj):
    if isinstance(obj, list):
        if all(isinstance(x, dict) for x in obj):
            return obj, {"wrapper": None}
        return [{"value": x} for x in obj], {"wrapper": None, "coerced": True}
    if isinstance(obj, dict):
        # prefer the longest list of dicts
        candidates = []
        for k, v in obj.items():
            if isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
                candidates.append((k, len(v)))
        if candidates:
            key = max(candidates, key=lambda t: t[1])[0]
            return obj[key], {"wrapper": key}
        # dict of dicts -> values
        if obj and all(isinstance(v, dict) for v in obj.values()):
            return list(obj.values()), {"wrapper": "dict_values"}
        return [obj], {"wrapper": "single"}
    return [{"value": obj}], {"wrapper": "scalar"}

def to_df(records):
    if not records:
        return pd.DataFrame()
    return pd.json_normalize(records, sep="__")

def guess_cols(df, patterns):
    pats = [p.lower() for p in patterns]
    out = []
    for c in df.columns:
        cl = c.lower()
        if any(p in cl for p in pats):
            out.append(c)
    return out

def distinct_nonempty(df, colnames, limit=100000):
    vals = []
    for c in colnames:
        if c in df.columns:
            vals.extend([str(x).strip() for x in df[c].dropna().astype(str) if str(x).strip() not in ("", "nan", "none")])
    uniq = sorted(set(vals))
    return uniq[:limit]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strain", required=True, help="Path to strain DB JSON")
    ap.add_argument("--tiers", required=True, help="Path to NeuroTerp tiers JSON")
    ap.add_argument("--out", required=True, help="Output directory")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    report_lines = []
    def w(line=""):
        report_lines.append(line)

    # Load
    s_raw = load_json(args.strain)
    t_raw = load_json(args.tiers)

    s_records, s_meta = extract_records(s_raw)
    t_records, t_meta = extract_records(t_raw)

    s_df = to_df(s_records)
    t_df = to_df(t_records)

    # Summaries
    w(f"[{datetime.now().isoformat()}] CIN reconcile step 1")
    w("== INPUT SUMMARY ==")
    w(f"Strain file: {args.strain}")
    w(f" - Wrapper: {s_meta}")
    w(f" - Rows: {len(s_df)}")
    w(f" - Columns: {len(s_df.columns)}")
    w(f" - Sample cols: {list(s_df.columns)[:20]}")
    w(f"Tiers file: {args.tiers}")
    w(f" - Wrapper: {t_meta}")
    w(f" - Rows: {len(t_df)}")
    w(f" - Columns: {len(t_df.columns)}")
    w(f" - Sample cols: {list(t_df.columns)[:20]}")
    w("")

    # Guess columns
    brand_cols = guess_cols(s_df, ["brand","producer","company"])
    strain_cols = guess_cols(s_df, ["strain","cultivar","variety","name"])
    category_cols = guess_cols(s_df, ["category","type","class"])
    product_type_cols = guess_cols(s_df, ["product_type","size","package","unit"])
    sku_cols = guess_cols(s_df, ["sku","product_code","id","item_number"])
    tier_cols = guess_cols(s_df, ["tier","neuroterp","matrix"])

    w("== GUESSED COLUMN SETS ==")
    w(f"brand_cols: {brand_cols}")
    w(f"strain_cols: {strain_cols}")
    w(f"category_cols: {category_cols}")
    w(f"product_type_cols: {product_type_cols}")
    w(f"sku_cols: {sku_cols}")
    w(f"tier_cols_in_strain_db: {tier_cols}")
    w("")

    # Build seeds
    def choose_first(df, cols, default=None):
        for c in cols:
            if c in df.columns:
                return c
        return default

    brand_c = choose_first(s_df, brand_cols)
    strain_c = choose_first(s_df, strain_cols)
    category_c = choose_first(s_df, category_cols)
    product_type_c = choose_first(s_df, product_type_cols)
    sku_c = choose_first(s_df, sku_cols)
    tier_c = choose_first(s_df, tier_cols)

    # Canonicalize helpers
    def canon(s):
        if s is None: return None
        s = str(s).strip()
        return s if s != "" and s.lower() not in ("nan","none","null") else None

    # Brands
    brands = []
    if brand_c:
        brands = sorted({canon(x) for x in s_df[brand_c] if canon(x)})
    brand_df = pd.DataFrame({"name": brands})
    brand_df.to_csv(os.path.join(args.out, "seed_brands.csv"), index=False)

    # Strains
    strains = []
    if strain_c:
        strains = sorted({canon(x) for x in s_df[strain_c] if canon(x)})
    strain_df = pd.DataFrame({"name": strains, "is_classic": False})
    strain_df.to_csv(os.path.join(args.out, "seed_strains.csv"), index=False)

    # Products (brand+strain+category+product_type+sku)
    prows = []
    for _, row in s_df.iterrows():
        b = canon(row.get(brand_c)) if brand_c else None
        st = canon(row.get(strain_c)) if strain_c else None
        cat = canon(row.get(category_c)) if category_c else None
        ptype = canon(row.get(product_type_c)) if product_type_c else None
        sku = canon(row.get(sku_c)) if sku_c else None
        if b or st or sku:
            prows.append({"brand_name": b, "strain_name": st, "category": cat, "product_type": ptype, "sku": sku})
    product_df = pd.DataFrame(prows).drop_duplicates().reset_index(drop=True)
    product_df.to_csv(os.path.join(args.out, "seed_products.csv"), index=False)

    # Tier codes from NeuroTerp file
    # Try common shapes
    nt_tiers = []
    if not t_df.empty:
        # Try to find tier code & description columns
        code_cols = [c for c in t_df.columns if any(k in c.lower() for k in ("code","tier","id","key","name"))]
        desc_cols = [c for c in t_df.columns if "description" in c.lower() or "desc" in c.lower()]
        # Fallback: take entire row as JSON string
        for _, r in t_df.iterrows():
            code = None
            for c in code_cols:
                val = r.get(c)
                if isinstance(val, str) and val.strip():
                    code = val.strip()
                    break
            desc = None
            for c in desc_cols:
                val = r.get(c)
                if isinstance(val, str) and val.strip():
                    desc = val.strip()
                    break
            if code:
                nt_tiers.append({"code": code, "display_name": code, "description": desc})
    tiers_df = pd.DataFrame(nt_tiers).drop_duplicates()
    tiers_df.to_csv(os.path.join(args.out, "seed_neuroterp_tiers.csv"), index=False)

    # If strain DB has a tier column, compare
    unknown_tier_values = []
    if tier_c and not tiers_df.empty:
        known = set(tiers_df["code"].str.lower())
        seen = [canon(x) for x in s_df[tier_c] if canon(x)]
        # split multi-tier strings like "Sapphire Amethyst Onyx"
        split_vals = []
        for v in seen:
            parts = [p.strip() for p in v.replace("/", " ").replace(",", " ").split() if p.strip()]
            split_vals.extend(parts if parts else [v])
        for x in set(s.lower() for s in split_vals):
            if x not in known:
                unknown_tier_values.append(x)

    # Duplication checks
    dup_brands = brand_df[brand_df["name"].duplicated(keep=False)] if not brand_df.empty else pd.DataFrame()
    dup_strains = strain_df[strain_df["name"].duplicated(keep=False)] if not strain_df.empty else pd.DataFrame()
    dup_products = product_df[product_df.duplicated(keep=False)] if not product_df.empty else pd.DataFrame()

    # Report
    w("== OUTPUT SEEDS ==")
    w(f"seed_brands.csv rows: {len(brand_df)}")
    w(f"seed_strains.csv rows: {len(strain_df)}")
    w(f"seed_products.csv rows: {len(product_df)}")
    w(f"seed_neuroterp_tiers.csv rows: {len(tiers_df)}")
    w("")
    w("== RECONCILIATION CHECKS ==")
    if tier_c:
        w(f"Strain DB tier column detected: {tier_c}")
        if unknown_tier_values:
            w("Unknown tier tokens (not present in NeuroTerp tiers): " + ", ".join(sorted(set(unknown_tier_values))))
        else:
            w("No unknown tier tokens detected, or NeuroTerp tiers empty.")
    else:
        w("No tier column detected in strain DB.")
    w("")
    # Null checks
    if not product_df.empty:
        nulls = product_df.isna().sum().to_dict()
        w(f"Null counts in product seed: {nulls}")
    # Duplicate checks (counts)
    def dup_count(df):
        return int(df.duplicated().sum()) if not df.empty else 0
    w(f"Duplicate rows — brands: {dup_count(brand_df)}, strains: {dup_count(strain_df)}, products: {dup_count(product_df)}")
    w("")

    # Write report
    report_path = os.path.join(args.out, "report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("Wrote outputs to:", args.out)
    print("Files: seed_brands.csv, seed_strains.csv, seed_products.csv, seed_neuroterp_tiers.csv, report.txt")

if __name__ == "__main__":
    main()
