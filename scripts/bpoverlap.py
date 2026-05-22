#!/usr/bin/env python3

import csv
import sys
from collections import defaultdict, deque

"""
Usage python3 bpoverlap.py /dev/stdin partial.tsv redundant.tsv summary.txt
"""

if len(sys.argv) != 5:
    print("Usage: python3 bpoverlap.py input.csv partial.tsv redundant.tsv summary.txt")
    sys.exit(1)

input_source   = sys.argv[1]
partial_file   = sys.argv[2]
redundant_file = sys.argv[3]
summary_file   = sys.argv[4]

REDUNDANCY_FRAC = 0.95

active = deque()

pair_bp = defaultdict(int)
pair_rel_bp = defaultdict(int)

pair_unique_rows = defaultdict(int)
pair_rel_unique_rows = defaultdict(int)

seen_rows = set()

total_bp = 0
partial_rows = []

with open(partial_file, "w") as f:
    f.write("pair\tbp\toverlap_frac\tjaccard\tintervals\n")

with open(redundant_file, "w") as f:
    f.write("pair\tbp\toverlap_frac\tjaccard\tintervals\n")

current_chrom = None

if input_source == "/dev/stdin":
    f = sys.stdin
else:
    f = open(input_source)

reader = csv.reader(f)
next(reader)

for row_id, row in enumerate(reader, start=2):

    chrom = row[0]
    s = int(row[2])
    e = int(row[3])
    cat = row[4]

    if chrom != current_chrom:
        active.clear()
        current_chrom = chrom

    while active and active[0]["end"] < s:
        active.popleft()

    for other in active:

        if other["id"] >= row_id:
            continue

        os = other["start"]
        oe = other["end"]
        ocat = other["cat"]

        ov_start = max(s, os)
        ov_end = min(e, oe)

        if ov_end < ov_start:
            continue

        bp = ov_end - ov_start + 1

        a_len = e - s + 1
        b_len = oe - os + 1

        min_len = min(a_len, b_len)

        union_len = max(e, oe) - min(s, os) + 1

        overlap_frac = bp / min_len
        jaccard = bp / union_len

        pair = " vs ".join(sorted([cat, ocat]))

        relation = "partial"

        if s <= os and e >= oe:
            relation = f"{cat}_contains_{ocat}"
        elif os <= s and oe >= e:
            relation = f"{ocat}_contains_{cat}"
        elif overlap_frac >= REDUNDANCY_FRAC:
            relation = "redundant"

        pairrel = f"{pair}|{relation}"

        total_bp += bp

        pair_bp[pair] += bp
        pair_rel_bp[pairrel] += bp

        k1 = (pair, row_id)
        k2 = (pair, other["id"])

        if k1 not in seen_rows:
            pair_unique_rows[pair] += 1
            pair_rel_unique_rows[pairrel] += 1
            seen_rows.add(k1)

        if k2 not in seen_rows:
            pair_unique_rows[pair] += 1
            pair_rel_unique_rows[pairrel] += 1
            seen_rows.add(k2)

        line = (
            f"{pair}\t{bp}\t{overlap_frac:.6f}\t"
            f"{jaccard:.6f}\t{s}-{e}\t{os}-{oe}\n"
        )

        if relation == "redundant":
            with open(redundant_file, "a") as out:
                out.write(line)

        elif relation == "partial":
            partial_rows.append((overlap_frac, line))

    active.append({
        "id": row_id,
        "start": s,
        "end": e,
        "cat": cat
    })

if input_source != "/dev/stdin":
    f.close()


partial_rows.sort(reverse=True, key=lambda x: x[0])

with open(partial_file, "a") as out:
    for _, line in partial_rows:
        out.write(line)


with open(summary_file, "w") as out:

    out.write(f"TOTAL OVERLAPPING BP:\t{total_bp}\n")

    out.write("\n=== OVERLAPPING BASE PAIR COUNTS BY CATEGORY PAIR ===\n")
    for p in pair_bp:
        out.write(f"{p}\t{pair_bp[p]}\n")

    out.write("\n=== OVERLAPPING BASE PAIR COUNTS BY CATEGORY PAIR + OVERLAP RELATIONSHIP ===\n")
    for p in pair_rel_bp:
        out.write(f"{p}\t{pair_rel_bp[p]}\n")

    out.write("\n=== UNIQUE OVERLAPPING ROW COUNTS BY CATEGORY PAIR ===\n")
    for p in pair_unique_rows:
        out.write(f"{p}\t{pair_unique_rows[p]}\n")

    out.write("\n=== UNIQUE OVERLAPPING ROW COUNTS BY CATEGORY PAIR + OVERLAP RELATIONSHIP ===\n")
    for p in pair_rel_unique_rows:
        out.write(f"{p}\t{pair_rel_unique_rows[p]}\n")
