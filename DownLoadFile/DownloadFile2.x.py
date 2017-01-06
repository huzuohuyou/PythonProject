__author__ = 'jishu12'
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import os
import threading
import pickle



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
    downsize = blocknum * blocksize
    if downsize >= totalsize:
        downsize = totalsize
    s = "%.2f%%" % (percent) + "====>" + "%.2f" % (downsize / 1024 / 1024) + "M/" + "%.2f" % (
    totalsize / 1024 / 1024) + "M \r"
    sys.stdout.write(s)
    sys.stdout.flush()
    if percent == 100:
        print('')
        # input('输入任意键继续...')


def downingArray(dlog,array):
    proxy = {'http': '23.106.157.237:8888'}
    proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler(debuglevel=1))
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

    # 添加头信息，模仿浏览器抓取网页，对付返回403禁止访问的问题
    # i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    # i_headers = {
    #    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}

    for id in array:
        try:
            url = 'http://pubmedcentralcanada.ca/pmcc/articles/PMC{id}/pdf/{id}.pdf'.format(id=id)
            print("PMCID:" + str(id) + url)
            filename = os.path.basename(url)
            # urllib.urlretrieve(url, "D://" + filename, callbackfunc)
            f = urllib2.urlopen(url)
            data = f.read()
            with open("{id}.pdf".format(id=id), "wb") as code:
                code.write(data)
            dlog.logSuccessId(id)
        except:
            dlog.logExId(id)

def downimg():
    # 3128072
    dlog = None
    if (os.path.exists("dlog.pkl")):

        pkl_file = open('dlog.pkl', 'rb')
        dlog = pickle.load(pkl_file)
        pkl_file.close()
        print("exist file dlog.pkl load dlog lastId:{lastId} exArray{exArray}...".format(lastId=dlog.lastId,
                                                                                         exArray=str(dlog.exArray)))
    else:
        dlog = DLog(3128072, [])
        print("didn't exist file dlog.pkl create new one ...")
    # 失败数据重载
    downingArray(dlog, dlog.exArray)
    # 新数据下载
    downingArray(dlog, range(dlog.lastId, 99999999))

# 启动线程下载
threading.Thread(target=downimg, args=('')).start()
