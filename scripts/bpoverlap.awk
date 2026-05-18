#!/usr/bin/awk -f

###
### bpoverlap.awk

### Usage:
    ### awk -f bpoverlap.awk INPUT.csv partial_OUTPUT.tsv redundant_OUTPUT.tsv summary_OUTPUT.txt

### Takes an input CSV file and prints instances where there is overlap between multiple rows. Partial is 95% base pair overlap cutoff, Redundant is >95%, nested is 100% one element is nested within the other.
###

BEGIN {
    FS = ","
    OFS = "\t"

    REDUNDANCY_FRAC = 0.95
    n = 0

    if (partial_file == "")   partial_file = "partial_overlaps.tsv"
    if (redundant_file == "") redundant_file = "redundant_overlaps.tsv"
    if (summary_file == "")   summary_file = "overlap_summary.txt"

    print "pair\tbp\toverlap_frac\tjaccard\tintervals" > partial_file
    print "pair\tbp\toverlap_frac\tjaccard\tintervals" > redundant_file
}

NR > 1 {

    s   = $3 + 0
    e   = $4 + 0
    cat = $5

    while (head < tail && stop_q[head] < s) {
        head++
    }

    for (i = head; i < tail; i++) {

        os   = start_q[i]
        oe   = stop_q[i]
        ocat = cat_q[i]

        ov_start = (s > os ? s : os)
        ov_end   = (e < oe ? e : oe)

        if (ov_end >= ov_start) {

            bp = ov_end - ov_start + 1

            a_len = e - s + 1
            b_len = oe - os + 1

            min_len = (a_len < b_len ? a_len : b_len)

            max_end = (e > oe ? e : oe)
            min_start = (s < os ? s : os)
            union_len = (max_end - min_start + 1)

            overlap_frac = bp / min_len
            jaccard = bp / union_len

            if (cat < ocat)
                pair = cat " vs " ocat
            else
                pair = ocat " vs " cat

            relation = "partial"

            if (s <= os && e >= oe)
                relation = cat "_contains_" ocat
            else if (os <= s && oe >= e)
                relation = ocat "_contains_" cat
            else if (overlap_frac >= REDUNDANCY_FRAC)
                relation = "redundant"

            total_bp += bp

            pair_bp[pair] += bp
            pair_rel_bp[pair "|" relation] += bp

            if (relation == "redundant") {
                print pair, bp, overlap_frac, jaccard, s "-" e, os "-" oe >> redundant_file
            }

            if (relation == "partial") {
                score[n] = overlap_frac
                key[n] = pair "\t" bp "\t" overlap_frac "\t" jaccard "\t" s "-" e "\t" os "-" oe
                n++
            }
        }
    }

    start_q[tail] = s
    stop_q[tail]  = e
    cat_q[tail]   = cat
    tail++
}

END {

    for (i = 0; i < n; i++) {

        max_i = i
        for (j = i + 1; j < n; j++) {
            if (score[j] > score[max_i])
                max_i = j
        }

        tmp = score[i]
        score[i] = score[max_i]
        score[max_i] = tmp

        tmp = key[i]
        key[i] = key[max_i]
        key[max_i] = tmp

        print key[i] >> partial_file
    }

    print "TOTAL OVERLAPPING BP:", total_bp > summary_file

    print "\n=== SUMMARY BY CATEGORY PAIR ===" >> summary_file
    for (p in pair_bp)
        print p, pair_bp[p] >> summary_file

    print "\n=== SUMMARY BY PAIR + RELATION ===" >> summary_file
    for (p in pair_rel_bp)
        print p, pair_rel_bp[p] >> summary_file
}
