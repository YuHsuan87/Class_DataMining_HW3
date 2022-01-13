# Data Mining HW3
###### tags: `data_mining`,`hw`
## folder and File
Folder:
* hw3dataset: 各種graph.txt，**為了方便操作，我將ibm-dataset改成graph_7.txt**
* result: 放置結果.txt檔的位置

Files:
* load_data.py: 讀取graph_num.txt 及 graph node and link分析
* method.py: Implement **HITS/PageRank/SimRank** Algorithm
* main.py:執行algo 及生成 結果.txt
 
## Implementation Detail
### Initial Set
* node_matrix = 計算所有node與其連接的node and link，形成一個matrix
* node_sum = 所有node的總數

### Hyperlink-Induced Topic Search (HITS)
1. 初始化每個node的 **hubs** 及 **authorities**，都先設定為一
2. 開始進行迭代：
    生成一個**temp_Hubs** and **temp_Auths**，避免本次node的計算結果影響其餘node的計算
    for A in each node {
    * Compute $temp\_Hubs_k(A) = \sum_{}Auth_{k-1}(A\_out)$ 
    * Compute $temp\_Auth_k(A) = \sum_{}Hubs_{k-1}(in\_A)$
    * Normalize temp_Hubs and temp_Auths
    * Hubs = temp_Hubs 、 Auths = temp_Auths
}
3. return Hubs and Auths, End
    
### PageRank(PR)
* Set **Damping Factor** = 0.15
* $formula$
![](https://i.imgur.com/7y6h9ns.png)

用本圖來方便說明
![](https://i.imgur.com/MjyUj0l.png)

1. Iter 0 : 初始化整體 **PR**， $PR(i) = 1/node\_sum$
2. 開始進行迭代 : 
    * 生成**temp_PR**，避免本次node_pr計算影響其餘node_pr計算結果
    * Compute $temp\_PR(C)_{k} = \sum_{}(PR_{k-1}(in\_C)/Hubs(in\_C))$， in_C's node = A and D
    * temp_PR_result = Damping Factor/node_sum + (1-Damping Factor) * temp_PR
    * PR = temp_PR_result
3. Normalize 最終 PR，避免PR整體總和不為一的情況發生
4. return PR, End    
### SimRank
* Set **C** = **Decay_Factor_C** = 0.9
* $formula$
![](https://i.imgur.com/SvyD6bp.png)
1. 初始化 sim
 ![](https://i.imgur.com/gEEq2bQ.png)
2. 開始進行迭代
    * 生成**temp_sim**，避免本次node_sim計算影響其餘node_sim計算結果
    * Compute temp_sim(node_A, node_B): 
        if A == B: $s_t(A, B) =1$ 
        else: 統計 in_A_node ($I(A)$) and in_B_neighbor($I(B)$)
        \begin{cases}
        s_t(A, B) =0, &若I(A)或I(B)其中一個的個數為 0  \\
        s_t(A, B) = formula, &I(A) 或 I(B)的個數均不為0
        \end{cases}
    * $formula$ 為 $C/(I(A)的個數*I(B)的個數)再乘上\sum_{}S_{t-1}(union\_pair\_ofI(A)、I(B))$
    * sim = temp_sim
3. return sim, End
## Result analysis and discussion
### Original Graph
* Graph_1
![](https://i.imgur.com/XQbCBqt.png)
* Graph_2
![](https://i.imgur.com/ySDRtik.png)
* Graph_3
![](https://i.imgur.com/7S8A0tg.png)
* Graph_4
![](https://i.imgur.com/nqAXOay.png)
### HITS
* Graph_1 and Graph_2:
![](https://i.imgur.com/DrY4TmF.png)
這兩張圖的結果相似，差別僅只在於graph1尾node的hubs及初始node的Auths，原因在於graph1並不像graph2形成一個cycle，所以頭少了node連接、尾少了接出去的link。
* Graph_3:
![](https://i.imgur.com/LMgDdk3.png)
Total_Auths 與 Total_Hubs 的結果相同，且node2及node3兩數值比較高，是因為node2與node3皆個別雙向連接node1及node4，彼此再互相連接。
    | un_normalize | node1 | node2 | node3 | node4 |
    |:------------:|:-----:|:-----:|:-----:|:-----:|
    | Authorities  |   1   |   2   |   2   |   1   |
    |     Hubs     |   1   |   2   |   2   |   1   |

    因為hubs與Auths相互影響，由上表所見兩者均相同，所以總結果也相同
* Graph 4:
![](https://i.imgur.com/uauv0NN.png)
![](https://i.imgur.com/T0amzQn.png)
由於數值較細，節點多，以圖表來表示結果:
我們可以觀察到，node3及node5的Auths相同且最多的，不過以in_node_link來看，node3只有三條，而node5的in_link卻有五條，原因在於node5也為node3的in_neighbor，所以能夠通過迭代過程來獲得node5累積的Auths，因此結果仍然維持相同。
### PageRank
* Graph_1
![](https://i.imgur.com/BKiKMoV.png)
pr的分數是遞增的情況，主要是因為本圖為單向，所以越後面的node在迭代多次的情況下可以累積越多前面node的pr總和。
* Graph_2
![](https://i.imgur.com/iI9tyDn.png)
pr有點在計算HITS Auths的感覺，只是多了decay_factor及normalize使其更好的收斂，在這張graph為cycle的情況下，彼此相互影響且link皆不重疊的情況下，收斂結果每個node均相同。
* Graph_3
![](https://i.imgur.com/kefsCxG.png)
同Graph_2的概念，與計算HITS的Auths所得結果差不多，同樣為node2、node3相同且高於node1、node4，因為node2連接了node1、3，而node1只連接node2，同理node3和node4。
* Graph_4
![](https://i.imgur.com/GEcO3DY.png)
由表可以看到node1的PR最高，但奇怪的地方在於node1及node5同樣位於整體圖的中心點且link數都為最多的4條，但兩者PR卻足足相差10%，原因在於neighbor的關係，因為node5的兩條link分別連接到node6、7，而這兩個node link都非常少，因此導致最終node5的PR較低的結果。

### SimRank
由所有結果可以得知一個有趣的發現
**SimRank[node1][node2] = SimRank[node2][node1]**
* Graph_1 and Graph_2
![](https://i.imgur.com/yM8buMt.png)
Sim值是根據in_neighbor來計算兩個node的同質性，而根據結果可得，兩種Graph相似性極高，除了對角線 node本身的1，其餘均為0。會產生這樣的結果是因為，沒有相異兩node具備共同的in_neighbor。
* Graph_3
![](https://i.imgur.com/bXNJyeI.png)
純粹node1跟node3有共同in_neighbor_node2，同理node2與node4，所以其值不為0。
* Graph_4
![](https://i.imgur.com/iZoPhIh.png)
由於node彼此之間link連接性很高，在迭代多次的情況下，彼此node的in_neighbor的相關性也很高，所以總體的Sim值相差不大。

### Damping_Factor and Decay_Factor analysis
以Graph_4來作為本次討論
* Damping Factor
![](https://i.imgur.com/HN5vsMQ.png)
**Analysis**:
DF決定in_neighbor_node持續往當前node瀏覽的概率，從結果可以發現，當數值越大的情況下，整體數值是越趨於相同，代表就算彼此link連結很多，但DF越大，隨機走的機率就越高，所以整體數值就較沒有分析價值，普遍設定DF=(0.1~0.15)。

* Decay_Factor
![](https://i.imgur.com/7hzvHje.png)
**Analysis**:
DF決定node彼此相似度的比率，由設定不同的decay_factor結果可以發現，當DF上升，SimRank整體數值是同步一起上升的，那會設定高也是因為當整體sim值除了node對自己本身的1以為，其餘都過低的話，那差異度會過高，導致除了自己以外，其他的node就沒有相似度的意義。 普遍設定DF= (0.8~0.9)

## Find a Way to Increase Node1(Hubs,Auths,PageRank)
**結論部份有增加前/後的比較表**
* Graph1
1. link(node1, node6)增加hubs
![](https://i.imgur.com/81kFVIQ.png)
2. link(node5, node1)增加Auths
![](https://i.imgur.com/bqja5bH.png)
3. link(node6, node1)增加PR
![](https://i.imgur.com/OLAPEnU.png)
* Graph2
1. link(node1, node4)增加hubs
![](https://i.imgur.com/75U5ia7.png)
2. link(node4, node1)增加Auths
![](https://i.imgur.com/N65b0jS.png)
3. link(node4, node1)增加PR
![](https://i.imgur.com/NHejHnt.png)
* Graph3
1. link(node1, node4)增加hubs
![](https://i.imgur.com/dtRRx0w.png)
2. link(node4, node1)增加Auths
![](https://i.imgur.com/abLctfl.png)
3. link(node4, node1)增加PR
![](https://i.imgur.com/qNRsb61.png)
* **Conclusion**:
直接從定義下手，**hubs就增加連出去的link，Auths就增加連入的link**，最後會發現其實計算Auths與PR概念相似，所以作相同動作通常也能獲得不錯的效果，用下表來比較：
    | Graph |   Hubs    | Authorities | PageRank  |
    |:-----:|:---------:|:-----------:|:---------:|
    | old_1 |    0.2    |      0      |   0.061   |
    | new_1 | **0.617** |   **0.5**   | **0.166** |
    | old_2 |    0.2    |     0.2     |    0.2    |
    | new_2 | **0.617** |  **0.617**  | **0.225** |
    | old_3 |   0.191   |    0.191    |   0.175   |
    | new_3 |  **0.5**  |   **0.5**   | **0.25**  |
    
## Computation performance analysis
透過兩種方式進行performance分析：
1. **convergence rate**
2. **excution time**
### Convergence Rate
由於迭代次數是我們能夠設定的，加上不管是hit或是pagerank所計算出的值都會因為iter多寡收斂，因此要判斷compute性能我們會以iter設定值使整體值趨於穩定的前提下進行分析。
**將針對convergence rate 去當作 computation perform的依據**
#### HITS
由於graph1~graph3的圖形簡單，收斂極快，無比較效益，所以我們以graph4與5來作比較:
* Graph_4:
![](https://i.imgur.com/DhaFOsu.png)
![](https://i.imgur.com/GoWnfQ3.png)
* Graph_5:
![](https://i.imgur.com/L2OOkva.png)
![](https://i.imgur.com/t9hBjvt.png)
**conclusion**:看起來好像都在**iter6到8**就差不多完成收斂，但graph5因為node、link都較多，所以在**iter9到11**還有些許微小變化。由此可知在node及link越多的情況下，收斂所需iter也可能會較多。
#### PageRank
* Graph_1:
![](https://i.imgur.com/o2wfvDX.png)
* Graph_4:
![](https://i.imgur.com/De7Bleg.png)
**conclusion**: 這裡可以看到一個有趣的發現，雖然graph_1 的 node、link 都比 graph_4少很多，也十分簡單，但整體收斂的iter比起graph_4卻是差不多的，所以有時node、link的數目並不能當作收斂的絕對標準，還是得根據整體graph的架構來判斷。

#### SimRank
以Graph_4為例
* Sim(**node1**, other_node)
![](https://i.imgur.com/D4ePWdz.png)
* Sim(**node2**, other_node)
![](https://i.imgur.com/g4zF1DD.png)
* Sim(**node7**, other_node)
![](https://i.imgur.com/z5IYFhc.png)
**conclusion**:simrank相較於HITS及PR的曲線更加容易掌握，除了對本身node的value均為1，其餘均呈現平滑緩慢上升最後趨於收斂，這跟我們所想像的simrank整體計算概念非常符合，藉由不斷迭代來累積獲得兩點彼此之間的相似度。也可以得知，當graph node及link越多，是肯定會讓整體收斂時間上升的。
### Execution Time
Iteration = 20
![](https://i.imgur.com/AtL4jEY.png)
在每個迭代過程，由於當前node都需要回到各個in_neighbor來作計算，整體計算呈現發散式的概念，因此能夠發現node and link數越多，往外擴張計算越龐大，尤其是SimRank兩兩pair的Sim計算，牽扯到in_neighbor的Sim(union_pair)，執行時間與node數直接成指數成長關係，所以不管是HITS、PR或者是SimRank，都是graph_5、6的執行時間遠大於1~4。
* Execution Time Table(Sec)

| Graph |  hits   | pagerank | simrank |
|:-----:|:-------:|:--------:|:-------:|
|   1   | 0.00013 |  0.0002  | 0.0031  |
|   2   | 0.00011 | 0.00017  | 0.0007  |
|   3   | 0.00009 | 0.00015  | 0.0006  |
|   4   | 0.00018 | 0.00026  | 0.0018  |
|   5   | 0.2214  |  0.2303  | **148.06**  |
|   6   |  1.538  |  1.686   |  **3000**   |

## Discussion
這次的作業做了三種針對node_web的演算法，有分析網頁之間的連結排名及節點之間的相似度分析等等。並針對各個主項做了多面向的比較，也能夠去體會在甚麼情況node的串接及走訪之下，會獲得怎麼樣的反饋。這樣的模式也套用在大家所熟知的推薦系統，用於搜尋引擎的推薦及超連結等等。
其實在這次實作前有稍微去查詢作法，發覺HITS及PageRank的做法其實有很多，如何針對node的整體計算數值收斂也有多元的做法:
1. 像是HITS有透過norm_sqrt的收斂也有我們傳統式normalize
2. 又或者是有跟學長討論到，當graph其中有node並未link出去，導致PageRank最終計算結果總和並不為一，那有多樣的處理方式，而我最後所使用最常見的根據整體比例normalize. 甚至有些做法PR是會大於1的。

希望後續有時間及機會針對這些不同的方式進行探討。
