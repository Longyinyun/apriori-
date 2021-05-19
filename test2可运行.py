#-*- coding: utf-8 -*-
from time import sleep    
import time          
from tqdm import tqdm
 
def load_data_set():              #读入数据集
   
    #test_data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    with open(r"C:\Users\19146\Desktop\data mining\实验一：Apriori实验数据\Apriori实验数据\T10I4D100K.dat") as f:
        data_set = f.readlines()
        data_set = [x.strip().split() for x in data_set]
    return data_set


def create_C1(data_set):
    """
    扫描数据集，创建元素个数为1的项集C1，作为频繁项集的候选项集C1（频繁一项集）
    """
    C1 = set()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)
    return C1


def is_apriori(Ck_item, Lksub1):
    """
    进行剪枝，如果满足支持度，返回True
    否则返回False，删除
    """
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True


def create_Ck(Lksub1, k):                 #生成候选频繁项集
    """
    由Lk-1生成Ck
    具体实现方法是在Lk-1中，对所有两个项集之间只有最后一项item不同的项集的并集
    """
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]           #求并集
                # 剪枝
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck


def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):        #len(list(Lk)[0])     求是频繁几项集
    """
    由候选频繁k项集Ck生成频繁k项集Lk
    主要内容是对Ck中的每个项集计算支持度，去掉不满足最低支持度的项集
    返回Lk，记录support_data
    """
    Lk = set()
    item_count = {}
    for t in data_set:                              #扫描所有商品，计算候选频繁项集C中项集的支持度，t为订单
        for item in Ck:                             #item为C中的项集
            if item.issubset(t):                    #如果C中的项集是t订单的子集
                if item not in item_count:          #如果item_count中还没有这个项集，计数为1
                    item_count[item] = 1            # item_count[item]是计数，总计数除以总订单数=支持度
                else:                               #如果item_count中已经有了这个项集，计数加1
                    item_count[item] += 1
    t_num = float(len(data_set))                    #t_num，订单总数
    for item in item_count:                         #item_count中已经有了所有的候选项集，计算支持度
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)                            #满足最小支持度的项集add进频繁项集Lk中
            support_data[item] = item_count[item] / t_num       #记录支持度，返回Lk
    return Lk                                                  #Lk是频繁项集


def generate_L(data_set, k, min_support):
    """
    生成频繁集Lk，通过调用generate_Lk_by_Ck
    从C1开始共进行k轮迭代，将每次生成的Lk都append到L中，同时记录支持度support_data
    """
    support_data = {}
    C1 = create_C1(data_set)            #生成C1
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)     #由C1生成L1，调用generate_Lk_by_Ck函数
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):                                             #由k已知进行重复迭代
        Ci = create_Ck(Lksub1, i)                                       #由Lk生成Lk+1，调用create_Ck函数
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


if __name__ == "__main__":                  #主程序入口
    """
    Test
    
    for i in tqdm(range(20)):
        sleep(0.5)
    """
    i=0
    data_set = load_data_set()              #加载测试数据集
    L, support_data = generate_L(data_set, k=5, min_support=0.01)            #数据集中最大商品数为5，给定默认最低支持度为0.2，调用generate_L函数                                              
    '''
    for Lk in L:
       
        f.write("="*50)
        s="\n".format("frequent " ,str(len(list(Lk)[0])) , "-itemsets\t\tsupport")
		f.write(s)
		f.close()
        f.write("="*50)
       
        for freq_set in Lk:
            s="\n".format(freq_set, support_data[freq_set])
            f.write(s)
            i=i+1
    
    ss="\n".format(i)
    f.write(ss)
    print('done')
    f.close() 
'''
 
i=0   
with open(r"C:\Users\19146\Desktop\outcome_0.01.txt",'w') as f:
    
    for Lk in L:
        '''
        print ("="*50)
        print ("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")   
        print ("="*50)
        '''
        for freq_set in Lk:
            print (freq_set, support_data[freq_set])
            f.write(str(freq_set))
            f.write(str(support_data[freq_set]))
            f.write('\n')
            i=i+1
    f.close()
    print('频繁项集个数：',i)
	
