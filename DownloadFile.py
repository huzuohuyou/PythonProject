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
def downimg():
#3128072
    for id in range(3128072,9999999):
        try:
            url='http://pubmedcentralcanada.ca/pmcc/articles/PMC{id}/pdf/{id}.pdf'.format(id=id)
            print("PMCID:"+str(id)+url)
            filename=os.path.basename(url)
            urllib.request.urlretrieve(url, "E://Docs//"+filename, callbackfunc)
        except:
            pass
#启动线程下载
threading.Thread(target=downimg,args=('')).start()