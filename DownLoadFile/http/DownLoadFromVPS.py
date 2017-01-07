__author__ = 'jishu12'

import threading
import urllib.request
import zipfile
import socket
import time

max_thread = 100
# 初始化锁
lock = threading.RLock()

class Downloader(threading.Thread):
    """
    多线程http下载
    python3.5.X
    """
    def __init__(self, url, start_size, end_size, fobj, buffer):
        self.url = url
        self.buffer = buffer
        self.start_size = start_size
        self.end_size = end_size
        self.fobj = fobj
        threading.Thread.__init__(self)

    def run(self):
        """
            马甲而已
        """
        with lock:
            print ('starting: %s' % self.getName())
        self._download()

    def _download(self):
        """
            我才是搬砖的
        """
        socket.setdefaulttimeout(30*60)
        req = urllib.request.Request(self.url)
        # 添加HTTP Header(RANGE)设置下载数据的范围
        req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        f = urllib.request.urlopen(req)
        # 初始化当前线程文件对象偏移量
        offset = self.start_size
        while 1:

            if offset+self.buffer>self.end_size:
                block=f.read(self.end_size-offset)
            else:
                block = f.read(self.buffer)
            #print('%s ing.' % offset)
            # 当前线程数据获取完毕后则退出
            if (offset==self.end_size+1 or offset==self.end_size):
                with lock:
                    print ('%s done.' % self.getName()+str(offset))
                    break
            # 写如数据的时候当然要锁住线程
            # 使用 with lock 替代传统的 lock.acquire().....lock.release()
            # 需要python >= 2.5
            with lock:
                #sys.stdout.write('%s saveing block...' % self.getName())
                # 设置文件对象偏移地址
                self.fobj.seek(offset)
                # 写入获取到的数据
                self.fobj.write(block)
                offset = offset + len(block)
                #print('offset:'+str(offset))
                #sys.stdout.write('done.\n')


def main(url, thread=3, save_file='', buffer=1024*16):
    # 最大线程数量不能超过max_thread
    thread = thread if thread <= max_thread else max_thread
    # 获取文件的大小
    req = urllib.request.urlopen(url)
    #print('---------------headers---------------\n'+str(req.headers))
    size = int(req.info()['Content-Length'])
    # 初始化文件对象
    fobj = open(save_file, 'wb')
    # 根据线程数量计算 每个线程负责的http Range 大小
    avg_size, pad_size = divmod(size, thread)
    plist = []
    for i in range(thread):
        start_size = i*avg_size
        end_size = start_size + avg_size - 1
        if i == thread - 1:
            # 最后一个线程加上pad_size
            end_size = end_size + pad_size + 1
        print('start:{start}=========end:{end}'.format(start=start_size,end = end_size))
        t = Downloader(url, start_size, end_size, fobj, buffer)
        plist.append(t)
    print('开始搬砖')
    #  开始搬砖
    for t in plist:
        t.start()
    print('等待所有线程结束')
    # 等待所有线程结束
    for t in plist:
        t.join()
    print('结束当然记得关闭文件对象')
    # 结束当然记得关闭文件对象
    fobj.close()
    print ('Download completed!')

def unZip(filename):
    #filename = 'callofdutyblackopszombies_1349649132343_my.zip'  #要解压的文件
    filedir = 'E://Docs//'  #解压后放入的目录
    r = zipfile.is_zipfile(filename)
    if r:
        starttime = time.time()
        fz = zipfile.ZipFile(filename,'r')
        for file in fz.namelist():
            print(file)  #打印zip归档中目录
            fz.extract(file,filedir)
        endtime = time.time()
        times = endtime - starttime
    else:
        print('This file is not zip file')
    print('times' + str(time.time()))


if __name__ == '__main__':
    #unZip('E://Docs//docs.zip')
    main(url='http://23.106.147.204/204.tgz', thread=10, save_file='E://Docs//PMC{id}.tgz'.format(id='test'), buffer=1024*1024)
    #for id in range(3138886,3138897):
    #    url = 'http://107.182.182.93/PMC{id}.pdf'.format(id=id)
    #    print('===>'+url)
    #    main(url=url, thread=10, save_file='E://Docs//PMC{id}.pdf'.format(id=id), buffer=4096)

