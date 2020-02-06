from collections import defaultdict
import sys

def extract_cluster_conll(data_path):
    docs_clusters = {}
    with open(data_path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line: break

            if (line.find('#begin document') != -1):
                sentence_num = 0
                stack = defaultdict(list)
                clusters = defaultdict(list)
                doc_name = line.split()[2]
                in_docs = True
            elif (line == '\n'):
                if in_docs == True:
                    sentence_num += 1
            elif (line.find('#end document') == -1):
                splited_line = line.strip().split()
                gold_label = splited_line[-1]
                gold_labels = gold_label.split('|')
                for gold in gold_labels:
                    if ((gold == '-') or (gold == '*')):
                        break
                    try:
                        key = str(sentence_num) + '_' + splited_line[2]
                    except:
                        print('a')

                    if ((gold[0] == '(') and (gold[-1] == ')')):
                        idx = gold.replace('(', '')
                        idx = idx.replace(')', '')
                        idx = int(idx)
                        clusters[idx].append(key)
                        continue
                    elif (gold[0] == '('):
                        idx = int(gold.replace('(', ''))
                        stack[idx].append(key)

                    elif (gold[-1] == ')'):
                        idx = int(gold.replace(')', ''))
                        if idx not in stack.keys():
                            print("ERRRRORRRRR")
                            sys.exit()
                        s_key = stack[idx].pop()
                        clusters[idx].append(s_key + "#" + key)

            elif (line.find('#end document') != -1):
                in_docs = False
                #for c in clusters:

                docs_clusters[doc_name] = clusters

    return docs_clusters

