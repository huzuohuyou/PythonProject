import urllib.request
import sys
import os
import threading
import pickle
def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    global url
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    downsize=blocknum * blocksize
    if downsize >= totalsize:
    	downsize=totalsize
    s ="%.2f%%"%(percent)+"====>"+"%.2f"%(downsize/1024/1024)+"M/"+"%.2f"%(totalsize/1024/1024)+"M \r"
    sys.stdout.write(s)
    sys.stdout.flush()
    if percent == 100:
        print('')
        #input('输入任意键继续...')

class DLog:
    def __init__(self, lastId, exArray):
      self.lastId = lastId
      self.exArray = exArray

    def logExId(self,lastId):
        if(lastId in self.exArray):
            pass
        else:
            self.exArray.append(lastId)
            output = open('dlog.pkl', 'wb')
            # Pickle dictionary using protocol 0.
            pickle.dump(self, output,-1)
            output.close()
            print(self.exArray)

    def logLastId(self,lastId):
        self.lastId=lastId
        output = open('dlog.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self, output,-1)
        output.close()

    def getLastId(self):
        return self.lastId

def downingArray(dlog,array):
    for id in array:
        print("reloading exid " +str(dlog.exArray)+'...')
        try:
            url='http://pubmedcentralcanada.ca/pmcc/articles/PMC{id}/pdf/{id}.pdf'.format(id=id)
            print("PMCID:"+str(id)+url)
            filename='PMC{ID}'.format(id=os.path.basename(url))
            urllib.request.urlretrieve(url, filename, callbackfunc)
            dlog.logLastId(id)
        except:
            dlog.logExId(id)

def downimg():
#3128072
    dlog=None
    if(os.path.exists("dlog.pkl")):

        pkl_file = open('dlog.pkl', 'rb')
        dlog = pickle.load(pkl_file)
        pkl_file.close()
        print("exist file dlog.pkl load dlog lastId:{lastId}...".format(lastId=dlog.lastId))
    else:
        dlog = DLog(3128072,[])
        print("didn't exist file dlog.pkl create new one ...")
    #失败数据重载
    downingArray(dlog,dlog.exArray)
    #新数据下载
    downingArray(dlog,range(dlog.lastId,99999999))

#启动线程下载
threading.Thread(target=downimg,args=('')).start()