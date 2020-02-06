from algorithm.Score import *
from collections import defaultdict

def partition(cur_s, clusters):
    dummy = -1
    id_list = [] #cur_s내의 mention들의 clusters 기준 clusters id

    for m in cur_s:
        mention = m

        isFound = False
        for id, cluster in clusters.items():
            for c in cluster:
                if mention == c:
                    id_list.append(id)
                    isFound = True
                    break
            if isFound: break
        if not isFound:
            id_list.append(dummy)
            dummy -= 1

    return id_list

def MUCFn(pred, gold):
    '''
    :param pred: list of list, 개체들의 list. 개체는 같은 개체를 나타내는 멘션의 key값 list.
    :param gold: pred와 같다.
    :return:
    '''
    pre = AccScore("MUC_PRE", 0, 0)
    rec = AccScore("MUC_REC", 0, 0)
    f1 = CRF1Score("MUC_F1", pre, rec)

    g_mentions = defaultdict(list)
    p_mentions = defaultdict(list)

    p_clusters = pred
    g_clusters = gold

    for i, g_cluster in enumerate(g_clusters):
        for m in g_cluster:
            g_mentions[i].append(m)
            g_mentions[i] = list(set(g_mentions[i]))

    for i, p_cluster in enumerate(p_clusters):
        for m in p_cluster:
            p_mentions[i].append(m)
            p_mentions[i] = list(set(p_mentions[i]))

    for g_cluster in g_clusters:
        pt = partition(g_cluster, p_mentions)
        rec.total += len(g_cluster) - 1
        rec.correct += len(g_cluster) - len(set(pt))
        diff_cluster = [x for x in set(pt) if x > 0]
        if len(diff_cluster) > 1:
            #같은 개체를 pred에서 다른 개체로 나눈 경우.
            dict = defaultdict(list)
            for i, id in enumerate(pt):
                if id < 0:
                    continue
                dict[id].append(g_cluster[i])

    for p_cluster in p_clusters:
        pt = partition(p_cluster, g_mentions)
        pre.total += len(p_cluster) - 1
        pre.correct += len(p_cluster) - len(set(pt))
        diff_cluster = [x for x in set(pt) if x > 0]
        if len(diff_cluster) > 1:
            # 다른 개체를 구축팀에서 같은 개체로 판단한 경우.
            dict = defaultdict(list)
            for i, id in enumerate(pt):
                if id < 0:
                    continue
                dict[id].append(p_cluster[i])

    return pre, rec, f1