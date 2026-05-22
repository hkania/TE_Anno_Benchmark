#!/usr/bin/env python3

import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


"""
redundancy_heatmap.py

Usage:
    python3 redundancy_heatmap.py ref.csv test.csv output.pdf
"""

def load_csv(csv):

    data = defaultdict(list)

    with open(csv) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) < 4:
                continue

            s = int(parts[2])
            e = int(parts[3])
            c = parts[4] if len(parts) > 4 else "NA"

            data[c].append((s, e))

    return dict(data)

def overlap_len(a, b):

    i = j = 0
    ov = 0

    a = sorted(a)
    b = sorted(b)

    while i < len(a) and j < len(b):

        as_, ae = a[i]
        bs, be = b[j]

        s = max(as_, bs)
        e = min(ae, be)

        if s <= e:
            ov += (e - s)

        if ae < be:
            i += 1
        else:
            j += 1

    return ov

def coverage_len(intervals):

    if not intervals:
        return 0

    intervals = sorted(intervals)

    merged = []
    cs, ce = intervals[0]

    for s, e in intervals[1:]:
        if s <= ce:
            ce = max(ce, e)
        else:
            merged.append((cs, ce))
            cs, ce = s, e

    merged.append((cs, ce))

    return sum(e - s for s, e in merged)


def build_matrix(A, B):

    A_classes = sorted(A.keys())
    B_classes = sorted(B.keys())

    mat = np.zeros((len(A_classes), len(B_classes)), dtype=float)

    A_cov = {c: coverage_len(A[c]) for c in A_classes}
    B_cov = {c: coverage_len(B[c]) for c in B_classes}

    for i, a in enumerate(A_classes):
        for j, b in enumerate(B_classes):

            ov = overlap_len(A[a], B[b])
            denom = min(A_cov[a], B_cov[b])

            mat[i, j] = ov / denom if denom > 0 else 0.0

    return A_classes, B_classes, mat

def plot_dual(gt_classes, test_classes, gt_test, test_test, outfile):

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

#Plots the reference annotation versus the test annotation

    sns.heatmap(
        gt_test,
        xticklabels=test_classes,
        yticklabels=gt_classes,
        cmap="magma",
        vmin=0,
        vmax=1.5,
        linewidths=0.5,
        annot=True,
        ax=axes[0]
    )
    axes[0].set_title("REF × TEST (Accuracy / Misclassification)")
    axes[0].set_xlabel("TEST classes")
    axes[0].set_ylabel("REF classes")

#Plots the test by itself to understand TE redundancy a bit better
    sns.heatmap(
        test_test,
        xticklabels=test_classes,
        yticklabels=test_classes,
        cmap="magma",
        vmin=0,
        vmax=1.5,
        linewidths=0.5,
        annot=True,
        ax=axes[1]
    )
    axes[1].set_title("TEST × TEST (Redundancy / Fragmentation)")
    axes[1].set_xlabel("TEST classes")
    axes[1].set_ylabel("TEST classes")

    plt.tight_layout()
    plt.savefig(outfile, dpi=300)
    plt.close()

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python3 redundancy_dual_heatmap.py ref.csv test.csv output.pdf")
        sys.exit(1)

    gt_csv = sys.argv[1]
    test_csv = sys.argv[2]
    outfile = sys.argv[3]

    gt = load_csv(gt_csv)
    test = load_csv(test_csv)

    gt_classes, test_classes, gt_test = build_matrix(gt, test)

    _, _, test_test = build_matrix(test, test)

    print("Ref classes:", gt_classes)
    print("Test classes:", test_classes)

    print("\nSaved dual heatmap as", outfile)

    plot_dual(gt_classes, test_classes, gt_test, test_test, outfile)
