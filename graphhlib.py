from copy import deepcopy
import random
def addVertex(g:'список смежности'):
    """Добавляет вершину в граф"""
    g.append([])
    return g

def deleteVertex(v:"удаляемая вершина",g:"граф(список смежности) из которого вершина удаляется"):
    """Удаляет вершину из графа"""
    g.pop(v)
    for i in range(len(g)):
        j=0
        while j<len(g[i]):
            if g[i][j]>v:
                g[i][j]=g[i][j]-1
                flag=1
            elif g[i][j]==v:
                g[i].pop(j)
                j-=1
            j+=1
    return g #список смежности с удалённой вершиной, и ребрами, к ней примыкающими; нумерация вершин, больших v сдвинута на 1

def deleteOrientedEdge(fr:'откуда',to:'куда',g:'список смежности'):
    """Удаляет ориентированное ребро из to в fr"""
    for i in range(len(g[fr])):
        if g[fr][i]==to:
            g[fr].pop(i)
            break
    return g


def deleteEdge(fr:'откуда',to:'куда',g:'список смежности'):
    """Удаляет ребро из to в fr"""
    deleteOrientedEdge(fr, to, g)
    deleteOrientedEdge(to, fr, g)
    return g


def addEdge(to:'откуда',fr:'куда',g:'список смежности'):
    
    """Добавляет ребро из to в fr"""
    if fr > len(g) or to > len(g):
        print("No")
    g[fr].append(to)
    g[to].append(fr)
    return g

def addOrientedEdge(to:'откуда',fr:'куда',g:'список смежности'):
    """Добавляет ориентированное ребро из to в fr"""
    if fr > len(g) or to > len(g):
        print("No")
    g[fr].append(to)


def makegraphEdgelist(n=-1,m=-1): #количество вершин и рёбер
    """создаёт неориентированный граф из списка рёбер, при отсутствии аргументов они вводятся в первой строке"""
    if n == -1 and m == -1:
        n,m = map(int, input().split())
    g = [[] for x in range(n+1)]
    for i in range(m):
        f,t = map(int,input().split())
        g[f].append(t)
        g[t].append(f)
    return g #список смежности


def makeOrientedgraphEdgelist(n=-1,m=-1): #количество рёбер
    """Создаёт ориентированный граф из списка рёбер, при отсутствии аргументов они вводятся в первой строке"""
    if n == -1 and m == -1:
        n,m = map(int, input().split())
    g = [[] for x in range(n+1)]
    for i in range(m):
        f,t = map(int,input().split())
        g[f].append(t)
    return g #список смежности


def makegraphMatrix(n=-1): #количество вершин
    """Создаёт граф из матрицы смежности"""
    if n == -1:
        n = int(input())
    matrix=[[]]
    for i in range(n):
        temp = list(map(int,input().split()))
        matrix.append(temp)
    g=[[]]
    for i in range(n):
        g.append([])
    for i in range(1,n+1):
        for j in range(n):
            if matrix[i][j] == 1:
                g[j+1].append(i)
    return g #список смежности
    
    #BFS и DFS алгоритмы

def findDistances(s:'стартовая вершина',g:'список смежности'):
    """Поиск кратчайщих расстояний от вершины s ко всем остальным вершинам графа"""
    used = []
    n = len(g)
    d = [0] * (n)
    p = [0] * (n)
    q = []
    used = [False] * (n)
    q.append(s)
    used[s] = True
    p[s] = -1
    while len(q)!=0:
        v = q.pop(0)
        for i in range(len(g[v])):
            to = g[v][i]
            if used[to]==False:
                
                used[to] = True
                q.append(to)
                d[to] = d[v]+1
                p[to] = v
                
    return d #массив расстояний от s до остальных вершин

def findPath(s:'откуда',s_to:'куда',g:'список смежности'):
    """Поиск кратчайщего пути от вершины до вершины"""
    used = []
    n = len(g)
    d = [0] * (n)
    d[s]=0
    p = [0] * (n)
    q = []
    used = [0] * (n)
    q.append(s)
    used[s] = True
    p[s] = -1
    while len(q)!=0:
        v = q.pop(0)
        for i in range(len(g[v])):
            to = g[v][i]
            if not used[to]:
                used[to] = True
                q.append(to)
                if d[to]==-1:
                    d[to]=0
                d[to] = d[v]+1
                p[to] = v
    path=[]
    v=s_to
    if not used[s_to]:
        return None
    while v!=-1:
        v=p[v]
        path.append(v)
    ans=list(reversed(path[:len(path)-1]))
    if len(ans)>1 or s_to in g[s]:
        ans.append(s_to)
    else:
        ans=None
    return ans #кратчайший путь от s до s_to


prev=-1

def dfsCycle(v,g,cl,p):
    """Всопмогательная функция"""
    global cycle_st
    global cycle_end
    global prev
    cl[v]=1
    for i in range(len(g[v])):
        to=g[v][i]
        if to!=prev:
            if cl[to]==0: #and v not in g[to]:
                p[to]=v
                prev=v
                if(dfsCycle(to,g,cl,p)):
                    return (True,p)
            if cl[to]==1:
                cycle_end=v
                cycle_st=to
                return (True,p)
    cl[v]=2
    
    return (False,p)


def isCyclic(g:'список смежности'):
    """Проверка, есть ли в ориентированном или неориентированном графе цикл"""
    global cycle_st
    global cycle_end
    global prev
    prev=-1
    n = len(g)
    for i in range(len(g)):
        g[i]=sorted(g[i])
    p = [-1] * (n+1)
    cl = [0] * (n+1)
    cycle_end = -1
    cycle_st = -1
    for i in range(n):
        if(dfsCycle(i,g,cl,p)[0]):
            break
    if cycle_st == -1:
        return False
    else:
        return True


def findCycle(g:'список смежности'):
    """Находит один любой цикл в графе"""
    n = len(g)
    global cycle_st
    global cycle_end
    global prev
    prev=-1
    for i in range(len(g)):
        g[i]=sorted(g[i])
    p = [-1] * (n+1)
    cl = [0] * (n+1)
    cycle_st = -1
    cycle_end = -1
    for i in range(n):
        flag,p = dfsCycle(i,g,cl,p)
        if flag:
            break
    if cycle_st == -1:
        return None
    else:
        cycle = []
        cycle.append(cycle_st)
        v = cycle_end
        while v!=cycle_st:
            cycle.append(v)
            v = p[v]
        cycle.append(cycle_st)
        cycle.pop(0)
        for i in range(len(cycle)//2):
            cycle[i], cycle[len(cycle)-i-1] = cycle[len(cycle)-i-1], cycle[i]
        return cycle
def dfsComponents(v,g):
    """вспомогательная функция"""
    global used_comp
    global path_comp
    global components
    global comp
    used_comp[v]=True
    path_comp.append(v)
    components[comp-1].append(v)
    for u in g[v]:
        if used_comp[u]==0:
            dfsComponents(u,g)
            
   
def findComponents(g:'список смежности'):
    """Находит компоненты связности"""
    global path_comp
    global used_comp
    global components
    global comp
    path_comp = []
    components = []
    used_comp = [0] * (len(g))
    comp = 0
    for i in range(1,len(used_comp)):
        if used_comp[i] == 0:
            comp+=1
            components.append([])
            dfsComponents(i,g)
    return components #двумерный массив - компоненты связности, каждый подмассив-набор вершин


def isBridge(fr:'откуда',to:'куда',g:'список смежности'):
    """Проверка, является ли ребро из fr в to мостом"""
    comp=components(g)
    b = -1
    a = -1
    for i in range(len(g[to])):
        if g[to][i] == fr:
            a = i
            break
    for i in range(len(g[fr])):
        if g[fr][i] == to:
            b = i
            break
    g1=deepcopy(g)
    if b !=-1:
        g1[fr].pop(b)
    if a !=-1:
        g1[to].pop(a)
    if components(g1) == comp:
        g1 = g
        return False
    else:
        g1 = g
        return True


N = 10**5
g=[[] for i in range(N)]


def findBridges(graph:'список смежности'):
    """Поиск мостов в неориентированном или ориентированном графе"""
    global g
    global bridges
    global tup_bridges,tin_bridges
    global timer_bridges
    global used_bridges
    N = 10**5
    tup_bridges,tin_bridges=[0]*N,[0]*N
    used_bridges=[False]*N
    timer_bridges=0
    bridges=[]
    g=graph+g
    for i in range(len(used_bridges)):
        if used_bridges[i]==False:
            dfsBridges(i)
    return bridges #массив мостов, представленных в виде подмассивов


def dfsBridges(v,p=-1):
    """Вспомогательная функция"""
    global timer_bridges
    global bridges
    used_bridges[v]=True
    tin_bridges[v]=timer_bridges
    timer_bridges+=1
    tup_bridges[v]=tin_bridges[v]
    for to in g[v]:
      if to==p:
          continue
      if (used_bridges[to]):
          tup_bridges[v] = min(tup_bridges[v], tin_bridges[to]);
      else:
        dfsBridges(to,v)
        tup_bridges[v]=min(tup_bridges[v],tup_bridges[to]);
        if tup_bridges[to]>tin_bridges[v]:
            bridges.append([v,to])



N = 10**5
g=[[] for i in range(N)]


def findEulerianPath(graph:'список смежности'):
    """поиск эйлерова пути в неориентированном графе"""
    g=[]
    count=0
    for i in range(len(graph)):
        if len(graph[i])%2==0:
            count+=1
    
    if count==len(graph) or count == len(graph)-2:
        flag=True
    else:
        flag=False
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if((graph[i][j],i)) not in g:
                g.append((i,graph[i][j]))
    print(g)
    graph=g
    stack = [];
    path = []
 
    stack.append(graph[0][0])
    while len(stack) > 0 and flag==1:
        v = stack[len(stack) - 1]
 
        degree = 0
        for (x, y) in graph:
            if v == x or v == y:
                degree += 1
 
        if degree == 0:
            stack.pop()
            path.append(v)
        else:
            edge = ();
            index = -1
 
            for i in range(len(graph)):
                if (v == graph[i][0] or v == graph[i][1]):
                    edge, index = graph[i], i
                    break
            graph.pop(index)
            stack.append(edge[1] if v == edge[0] else edge[0])
    return path #путь
 
 
count=0


def pathsdfs(v,end,graph,path,visited):
    global count
    if v == end:
        count+=1
        return
    for u in graph[v]:
        if visited[u]==False:
            path.append(u);
            visited[u]=True;
            pathsdfs(u, end, graph, path, visited)
            path.pop();
            visited[u]=False;


def countPaths(start:'откуда',end:'куда',g:'список смежности'):
    """находит количество путей из start в end"""
    visited=[False]*len(g)
    path=[]
    global count
    count=0
    pathsdfs(start,end,g,path,visited)
    return count


def countAllPaths(start:'откуда', g:'список смежности'):
    allcount = []
    for end in range(len(g)):
        allcount.append(countPaths(start, end, g))
    return allcount

def randGraph():
    """делает рандомный граф"""
    n=random.randint(0,25)
    g=[[] for i in range(n+1)]
    for i in range(n+1):
        m=random.randint(0,10)
        for j in range(m):
            v=random.randint(0,n)
            if v not in g[i] and v!=i:
                g[i].append(v)
    return g #список смежности
