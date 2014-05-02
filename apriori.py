import csv
import sys
import math
import operator

def readCsv(csv_file):
    with open(csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        transactions = []
        for row in spamreader:
            transaction = frozenset(row[0].split(','))
            transactions.append(transaction);
#         for t in transactions:
#             for item in t:
#                 sys.stdout.write(item+' ')
#             sys.stdout.write('\n');
    return transactions

def generateSupportSets2(transactions,min_sup):
    C=[]
    sup_dict = {}
    # Add itemsets with length 1
    C.append([])
    for transaction in transactions:
        for item in transaction:
            s=[item];
            if(frozenset(s) in sup_dict.keys()):
                sup_dict[frozenset(s)] += 1
            else:
                sup_dict[frozenset(s)] = 1
                C[0].append(s)
    C[0][:] = [s for s in C[0] if (sup_dict[frozenset(s)]>=min_sup)]
    C[0] = sorted(C[0],key=operator.itemgetter(0))
     
    # Add itemsets to C_k in increasing length
    k=1
    while(k<=len(C)):
        C.append([])
        for i in range(0,len(C[k-1])-1):
            cur_set =  C[k-1][i]
            cur_item = C[k-1][i][-1]
            cur_subset = C[k-1][i][0:-1]
            for j in range(i+1,len(C[k-1])):
                iter_set = C[k-1][j]
                if(set(cur_subset) == set(iter_set[0:-1]) and cur_item <iter_set[-1]):
                #if(set(cur_subset) == set(iter_set[0:-1])):
                    next_set = list(iter_set)
                    next_set.append(cur_set[-1])
                    next_set = sorted(next_set)
                    C[k].append(next_set)
                    sup_dict[frozenset(next_set)]=0
         
        for transaction in transactions:
            for s in C[k]:
                if(set(s).issubset(transaction)):
                    sup_dict[frozenset(s)]+=1
        
#         print sup_dict
        # Prune the C_k by min_sup
        count = 0
        for s in C[k]:
            if (sup_dict[frozenset(s)]<min_sup):
                sup_dict.pop(frozenset(s))
            else:
                C[k][count] = s
                count += 1
        C[k] = C[k][0:count] 
        #C[k][:] = [s for s in C[k] if (sup_dict[frozenset(s)]>=min_sup)]

        if(len(C[k])==0):
            C.pop()
             
        k+=1
             
    return C,sup_dict

def generateOneRHSRules2(C,sup_dict,min_conf,max_conf):
    R = {}
    # Generate all rules 
    for i in range(1,len(C)):
        for cur_set in C[i]:
            sup_cur = sup_dict[frozenset(cur_set)]
            for item in cur_set:
                subset = list(cur_set)
                subset.remove(item)
                sup_sub = sup_dict[frozenset(subset)]
                conf = sup_cur*1.0/sup_sub
                if(conf>=min_conf and conf<=max_conf):
#                     key = str(subset)+" => "+str([item])+' '+str(sup_cur)+' '+str(sup_sub)
                    key = str(subset)+" => "+str([item])
                    R[key] = conf
    return R
    
def generateSupportSets(transactions,min_sup,min_conf,max_conf):
    C = []
    R = {}
    C_prev = set()
    C_cur = set()
    sup_dict = {}
    # Add itemsets with length 1
    for transaction in transactions:
        for item in transaction:
            s=frozenset([item]);
            if(s in sup_dict):
                sup_dict[s] += 1
                C_cur.add(s)
            else:
                sup_dict[s] = 1
                
    C_cur = set(s for s in C_cur if (sup_dict[s]>=min_sup))
     
    # Add itemsets to C_k in increasing length
    k=1
    while(len(C_cur)!=0):
        C.append(C_cur)
        C_prev = C_cur
        C_cur = set()
        for prev_set in C_prev:
            for iter_set in C_prev:
                s=prev_set.union(iter_set)
                if(len(s)==k+1):
                    if(s not in sup_dict):
                        sup_dict[s] = 0;
                        C_cur.add(s)
                        
        for transaction in transactions:
            for s in C_cur:
                if(s.issubset(transaction)):
                    sup_dict[frozenset(s)]+=1
        
        # Prune the C_k by min_sup
        C_cur = set(s for s in C_cur if (sup_dict[frozenset(s)]>=min_sup))

        new_sup_dict = {}
        for key in sup_dict:
            if sup_dict[key]>=min_sup:
                new_sup_dict[key] = sup_dict[key]
        
        # Generate rules
        for prev_set in C_prev:
            for cur_set in C_cur:
                if prev_set.issubset(cur_set):
                    conf = 1.0*sup_dict[cur_set]/sup_dict[prev_set]
                    if (conf>=min_conf and conf<=max_conf):
                        output_left = '['
                        for i in prev_set:
                            output_left += (i + ',')
                        output_left = output_left[0:len(output_left)-1]
                        output_left += ']'
                        
                        output_right = '['
                        for i in cur_set.difference(prev_set):
                            output_right += i
                        output_right += ']'
                        key = output_left+" => "+output_right
                        key += ' (Conf: ' + str(conf*100) + '%, Supp: ' + str(int(float(sup_dict[cur_set])/len(transactions)*100))+'%)'
                        R[key] = conf
        k+=1
                  
    return C,new_sup_dict,R

def main(min_sup, min_conf, max_conf, csv_file):
    transactions = readCsv(csv_file)
    min_sup_count = math.ceil(min_sup*len(transactions))
    C,sup_dict,R = generateSupportSets(transactions,min_sup_count,min_conf,max_conf)
    R = sorted(R.iteritems(),key=operator.itemgetter(1),reverse=True)
    sup_dict_list = sorted(sup_dict.iteritems(),key=operator.itemgetter(1),reverse=True)
    print "==Frequent itemsets (min_sup=" + str(int(min_sup*100)) + "%)" 
    for t in sup_dict_list:
        output = '['
        for i in t[0]:
            output += (i + ',')
        output = output[0:len(output)-1]
        output += '], ' + str(int(float(t[1])/len(transactions)*100)) + '%'
        print output
        
    print ''
    print "==High-confidence association rules (min_conf=" + str(int(min_conf*100)) + "%)"
    for t in R: 
        print t[0]
    
#     C2,sup_dict = generateSupportSets2(transactions,min_sup_count)
#     for c in C2:
#         for l in c:
#             print l,
#             print " Support:",
#             print sup_dict[frozenset(l)]
#             
#     R2 = generateOneRHSRules2(C2,sup_dict,min_conf,max_conf);
#     R2 = sorted(R2.iteritems(),key=operator.itemgetter(1))
#     for key,value in R2:
#         print key,
#         print ' ',
#         print value
    return

if __name__ == '__main__':
    min_sup = 0.0
    min_conf = 0.0
    max_conf = 1.0
    if len(sys.argv) == 4:
        csv_file = sys.argv[1]
        min_sup = float(sys.argv[2])
        min_conf = float(sys.argv[3])
    elif len(sys.argv) == 5:
        csv_file = sys.argv[1]
        min_sup = float(sys.argv[2])
        min_conf = float(sys.argv[3])
        max_conf = float(sys.argv[4])
    else:
        print "python apriori.py csv_file min_sup min_conf [max_conf]"
        sys.exit(1)
    main(min_sup, min_conf, max_conf, csv_file)
