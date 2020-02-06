from algorithm.conll import *
from algorithm.scorer import *

if __name__ == "__main__":
    if len(sys.argv) == 3:
        key_dir = sys.argv[1]
        response_dir = sys.argv[2]

    key_dir = "./data/gold.conll"
    response_dir = "./data/pred.conll"

    key = extract_cluster_conll(key_dir)
    res = extract_cluster_conll(response_dir)


    p = AccScore("total_pre", 0, 0)
    r = AccScore("total_rec", 0, 0)
    f = CRF1Score("total_f1", p, r)
    for doc in key.keys():
        k = key[doc]
        re = res[doc]

        k_mentions = []
        r_mentions = []

        for _, c in k.items():
            k_mentions.append(c)
        for _, c in re.items():
            r_mentions.append(c)

        pre, rec, f1= MUCFn(r_mentions, k_mentions)
        print(doc)
        print(pre, rec, f1)
        p.correct += pre.correct
        p.total += pre.total
        r.correct += rec.correct
        r.total += rec.total

    print(p)
    print(r)
    print(f)









