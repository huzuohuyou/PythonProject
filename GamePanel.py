__author__ = 'jishu12'
import sys
import copy
import threading
#sys.setrecursionlimit(1000000) #例如这里设置为一百万
#panel=[[0]*10]*10
gamePanel = [
   [ 5,1,5,1,1,5,1,5,3,1 ]
 , [ 5,1,2,1,3,5,2,5,4,1 ]
 , [ 5,2,5,1,3,2,2,4,1,1 ]
 , [ 5,2,3,1,5,2,2,4,4,1 ]
 , [ 4,2,3,1,5,2,2,4,4,1 ]
 , [ 5,2,3,1,5,2,5,5,1,4 ]
 , [ 1,2,1,1,5,1,5,2,4,4 ]
 , [ 5,1,1,5,5,1,5,4,1,4 ]
 , [ 5,1,3,1,4,3,3,4,5,4 ]
 , [ 4,1,1,1,5,4,3,3,5,4]
]

def initPanel():
    view=[[[] for i in range(10)] for i in range(10)]
    for j in  range(0,10):
        for i in range(0,10):
            #print('gamePanel('+str(i)+str(j)+')'+'='+str(gamePanel[i][j]))
            view[i][j]=gamePanel[9-j][i]
           # print('view     ('+str(i)+str(j)+')'+'='+str(view[i][j]))
    return view



dictGroup = {}
def expand(dictGroup,gameView, x, y):
    if(x>=0 and x<=9 and y>=0 and y<=9):
        start=gameView[x][y]
        if(start!=0):
            if(y+1<=9):
                up=gameView[x][y+1]
            else:
                up=-1
            if(y-1>=0):
                down=gameView[x][y-1]
            else:down=-1
            if(x-1>=0):
                left=gameView[x-1][y]
            else:
                left=-1
            if(x+1<=9):
                right=gameView[x+1][y]
            else:
                right=-1
            if(left!=-1
                and dictGroup.get(str(x-1)+str(y))==None
                and start==left):
                #print('left'+str(x-1)+str(y)+str(left))
                dictGroup[str(x-1)+str(y)]=left
                expand(dictGroup,gameView,x-1,y)
            if(up!=-1
                and dictGroup.get(str(x)+str(y+1))==None
                and start==up):
                #print('up'+str(x)+str(y+1))
                dictGroup[str(x)+str(y+1)]=up
                expand(dictGroup,gameView,x,y+1)
            if(right!=-1
                and dictGroup.get(str(x+1)+str(y))==None
                and start==right ):
                #print('right'+str(x+1)+str(y))
                dictGroup[str(x+1)+str(y)]=right
                expand(dictGroup,gameView,x+1,y)
            if(down!=-1
                and dictGroup.get(str(x)+str(y-1))==None
                and start==down):
                #print('down'+str(x)+str(y-1))
                dictGroup[str(x)+str(y-1)]=down
                expand(dictGroup,gameView,x,y-1)
            return dictGroup
#print(gamePanel.__len__())

#print(globals(panel[8][0]))
#print(globals(panel[8][1]))
#print(globals(panel[9][9]))
#print(globals(panel[0][0]))
def destoryView(tempGroup,view):
    if(tempGroup!=None):
        for key in tempGroup.keys():
            x=key[0:1]
            y=key[1:2]
            #print('key:'+key+'x'+x+' y'+y)
            view[int(x)][int(y)]=0

def drawView(view):
    for j in range(0,10):
        row =''
        for i in range(0,10):
            row+= str(view[i][9-j])+' '
        print(row)

def logView(view):
    log=''
    for j in range(0,10):
        row =''
        for i in range(0,10):
            row+= str(view[i][9-j])+' '
        log=log+row
    return log

def needCleanColumn(view ,x):
    for y in range(0,10):
        if(view[x][y]==0):
            for j in range(y,10):
                if(view[x][j]!=0):
                    return True
    return False

def refreshColumn(view,x):
    while(needCleanColumn(view,x)):
        for y in range(0, 10):
            if(0==view[x][y]):
                for j in range(y,10):
                    #print(str(j))
                    if(j==9):
                        view[x][j]=0
                    else:
                        temp=view[x][j+1]
                        view[x][j] = temp

def needCleanRow(view,x):
    if(view[x][0]==0):
        for i in range(x+1,10):
            if(view[i][0]!=0):
                #print('x-'+str(view[m][0])+' i-'+str(view[i][0])+' step-'+str(i-m))
                return i-x
    return 0

def refreshRow(view,x):
    step=needCleanRow(view,x)
    while(step>0):
        for i in range(x,10):
            if(i>=10-step):
                for j in range(0,10):
                    view[i][j]=0
            else:
                for j in range(0,10):
                    view[i][j]=view[i+step][j]
        step=needCleanRow(view,x)
    #print('step:'+str(step)+'x:'+str(x))


def refreshView(view):
    for x in range(0,10):
        refreshColumn(view,x)
    #print('======================')
    #drawView(view)
    for x in range(0,10):
        #print('x location:'+str(x))
        refreshRow(view,x)
    return view
    #print('======================')
    #drawView(view)


def initGroup(view,x,y):
    expand(view,x,y)
    destoryView(view)
    refreshView(view)
    drawView(view)
    return  view


def getGroupName(group):
    key=''
    for y in range(0,10):
        for x in range(0,10):
            if(group!=None and group.get(str(x)+str(y))!=None):
                key=key+str(x)+str(y)
    return  key

def getGroupList(view):
    panelGroup={}
    for y in range(0,10):
        for x in range(0,10):
            tempGroup={}
            tempGroup=expand(tempGroup,view,x,y)
            #print('('+str(x)+','+str(y)+')'+'=>tempGroup'+str(tempGroup))
            key=getGroupName(tempGroup)
            if(panelGroup.get(key)==None and key!=''):
                panelGroup[key]=tempGroup
            if(tempGroup!=None):tempGroup.clear()
    return  panelGroup

def isCleanPanel(view):
    tempGroup={}
    for j in range(0,10):
        for i in range(0,10):
            tempGroup=expand(tempGroup,view,i,j)
    for key in tempGroup.keys():
        print('!'+str(len(tempGroup))+str(tempGroup))
        if(str(key).__len__()>0):
            tempGroup.clear()
            return  False
    tempGroup.clear()
    return True

class node:
    key=''
    score=0
    view=None
    childs=[]
    groups=None
    log=[]
maxscore=0
processcount=0
record=[]
count=1
def initTree(parent):
    global processcount
    groups=copy.deepcopy(parent.groups)
    #temp=copy.deepcopy(parent.view)
    if(groups.__len__()==0):
        global count
        count=count+1
        #print('************************************************* score:%d'%parent.score+' count:'+str(count))
        if(parent.score>maxscore):
            print('************************************************* score:%d'%parent.score+' count:'+str(count)+' processcount:%d'%processcount)
            #print(str(parent.key)+'\n')
            global maxscore
            maxscore=parent.score
            record.append(parent.score)
            fo=open('d:\\foo.txt', 'a')
            fo.write(str('score:'+str(parent.score))+'\n')
            fo.write(str(parent.key)+'\n')
            fo.close()
        #drawView(parent.view)
        return
    else:
        #print('len:%d '%groups.__len__()+'groups:'+str(groups))
        for item in groups.keys():
            #print('item:'+str(item))
            x = int(str(item)[0:1])
            y = int(str(item)[1:2])
            #print('>>>>>>>>>>>>>>>('+str(x)+','+str(y)+')')
            view=copy.deepcopy(parent.view)
            #view=initGroup(view,x,y)
            tempGroup={}
            tempGroup=expand(tempGroup,view,x,y)
            destoryView(tempGroup,view)
            view=refreshView(view)
            #drawView(view)
            child=node()
            child.key=parent.key+'\n->'+item
            child.view=view
            child.score=parent.score+len(tempGroup)*len(tempGroup)
            child.groups=(getGroupList(view))
            child.log.append(view)
            parent.childs.append(child)
            if(processcount<100):
                processcount=processcount+1
                t1 = threading.Thread(target=initTree,args=(child,))
                t1.setDaemon(True)
                t1.start()
                #t1.join()
            else:
                initTree(child)
threads = []
def startGame():
    temp=initPanel()
    groups=getGroupList(temp)
    #print('----------'+str(groups))
    #for item in groups.keys():
    view=copy.deepcopy(temp)
    #x = int(str(item)[0:1])
    #y = int(str(item)[1:2])
    #print('start at ('+str(x)+','+str(y)+')')
    tempGroup={}
    tempGroup=expand(tempGroup,view,8,0)
    print('tempGroup'+str(tempGroup))
    destoryView(tempGroup,view)
    view=refreshView(view)
    drawView(view)
    #view=initGroup(view,1,0)
    root = node()
    root.key='->'+str(8)+str(0)
    root.view = view
    root.score=len(tempGroup)*len(tempGroup)
    root.groups=getGroupList(view)
    #t1 = threading.Thread(target=initTree,args=(root,))
    #threads.append(t1)
    #t1.setDaemon(True)
    #t1.start()
    #t1.join()
    #for t in threads:
    #    t.setDaemon(True)
    #    t.start()
    #    t.join()
    initTree(root)

startGame()