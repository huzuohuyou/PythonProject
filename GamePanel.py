__author__ = 'jishu12'
import sys
sys.setrecursionlimit(1000000) #例如这里设置为一百万
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
def expand(gameView, x, y):
    if(x<0 or x>9 or y<0 or y>9):
        return
    #print(gameView[x][y])
    start=gameView[x][y]
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
        expand(gameView,x-1,y)
    if(up!=-1
        and dictGroup.get(str(x)+str(y+1))==None
        and start==up):
        #print('up'+str(x)+str(y+1))
        dictGroup[str(x)+str(y+1)]=up
        expand(gameView,x,y+1)
    if(right!=-1
        and dictGroup.get(str(x+1)+str(y))==None
        and start==right ):
        #print('right'+str(x+1)+str(y))
        dictGroup[str(x+1)+str(y)]=right
        expand(gameView,x+1,y)
    if(down!=-1
        and dictGroup.get(str(x)+str(y-1))==None
        and start==down):
        #print('down'+str(x)+str(y-1))
        dictGroup[str(x)+str(y-1)]=down
        expand(gameView,x,y-1)
#print(gamePanel.__len__())

#print(globals(panel[8][0]))
#print(globals(panel[8][1]))
#print(globals(panel[9][9]))
#print(globals(panel[0][0]))
def destoryView(view):
    global dictGroup
    for key in dictGroup.keys():
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
            if(i==9):
                for j in range(0,10):
                    view[9][j]=0
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
    #print('======================')
    #drawView(view)


def initGroup(view,x,y):
    #global panel
    expand(view,x,y)
    print(dictGroup)
    destoryView(view)
    #drawView(view)
    print('======================')
    refreshView(view)
    #drawView(view)
    return  view


def getGroupName(group):
    key=''
    for item in dictGroup.keys():
        key=key+str(item)
    print(key)
    return  key

def getGroupList(view):
    panelGroup={}
    for y in range(0,10):
        for x in range(0,10):
            expand(view,x,y)
            key=getGroupName(dictGroup)
            if(panelGroup.get(key)==None and key!=''):
                panelGroup[key]=dictGroup
            dictGroup.clear()
    return  panelGroup

def isCleanPanel(view):
    for j in range(0,10):
        for i in range(0,10):
            expand(view,i,j)
    for key in dictGroup.keys():
        if(str(key).__len__()>0):
            dictGroup.clear()
            return  False
    dictGroup.clear()
    return True

def startGame(view):
    if(isCleanPanel(view)):
        return
    else:
        groups= getGroupList(view)
        print(groups)
        for item in groups.keys():
            temp=view
            print(item)
            x = int(str(item)[0:1])
            y = int(str(item)[1:2])
            print('>>>>>>>>>>>>>>>'+str(x)+str(y))
            temp=initGroup(temp,x,y)
            startGame(temp)

view=initPanel()
view=initGroup(view,1,0)
startGame(view)