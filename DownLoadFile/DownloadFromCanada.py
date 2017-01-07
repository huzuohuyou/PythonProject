__author__ = 'jishu12'
#import urllib
import urllib.request
#import http.client
import sys
import os
import threading
import pickle
import time
import zipfile

dir='E://Docs//'
zip_count=1000
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
            #print(self.exArray)

    def logSuccessId(self,id):
        if(id in self.exArray):
            self.exArray.remove(id)
        if(id>self.lastId):
            self.lastId=id
        output = open('dlog.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self, output,-1)
        output.close()

    def removeId(self,id):
        if(id in self.exArray):
            self.exArray.remove(id)

def fileCountIn(dir):
    return sum([len(files) for root,dirs,files in os.walk(dir)])

def downingArray(dlog,array):
    global  dir
    for id in array:
        try:
            #print('文件个数：'+str(fileCountIn('E:\Docs')))
            if(fileCountIn(dir)>zip_count):
                zipPDF()
                time.sleep(60*60)
            url='http://pubmedcentralcanada.ca/pmcc/articles/PMC{id}/pdf/{id}.pdf'.format(id=id)
            print("PMCID:"+str(id)+url)
            filename='PMC{id}'.format(id=os.path.basename(url))
            urllib.request.urlretrieve(url, dir+filename, callbackfunc)
            #dlog.removeId(id)
            dlog.logSuccessId(id)
        except:
            dlog.logExId(id)

def zip_dir(dirname,zipfilename):
    """
    | ##@函数目的: 压缩指定目录为zip文件
    | ##@参数说明：dirname为指定的目录，zipfilename为压缩后的zip文件路径
    | ##@返回值：无
    | ##@函数逻辑：
    """
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
        #print('------------'+tar)
        os.remove(tar)
    zf.close()

def zipPDF():
    """
    压缩pdf文件，过滤以PMC开头的
    """
    global  dir
    f = zipfile.ZipFile('{dir}{zipName}.zip'.format(dir=dir,zipName='docs_'+str(time.time())),'w',zipfile.ZIP_DEFLATED)
    count=0
    for d in os.listdir(dir):
        if(str(d).startswith('PMC') and count!=zip_count):
            f.write(dir+d)
            os.remove(dir+d)
            count=count+1
    f.close()

def downimg():
#3128072
    dlog=None
    if(os.path.exists("dlog.pkl")):
        pkl_file = open('dlog.pkl', 'rb')
        dlog = pickle.load(pkl_file)
        pkl_file.close()
        print("exist file dlog.pkl load dlog lastId:{lastId} exArray{exArray}...".format(lastId=dlog.lastId,exArray=str(dlog.exArray)))
    else:
        dlog = DLog(3128072,[])
        print("didn't exist file dlog.pkl create new one ...")
    #失败数据重载
    downingArray(dlog,dlog.exArray)
    #新数据下载
    downingArray(dlog,range(dlog.lastId,5128072))

#启动线程下载
threading.Thread(target=downimg,args=('')).start()
#zip_dir('E:\\Docs\\docs','E:\Docs\\docs.zip')
#zipPDF()