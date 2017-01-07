import ftplib
import urllib.request
import sys
import os
import threading
import pickle
import time
from ftplib import FTP
__author__ = 'jishu12'

class FtpDownLoad:
    fixBlockSize=1024
    host='107.182.182.93'
    user=''
    passwd=''
    ftp=FTP(host, user, passwd)
    def downloadFileMultiThreads(self, threadIndex, remoteFilePath, localFilePath, \
                                     beginPoint, blockSize, rest = None):
        """
        A sub thread used to download file
        """
        try:
            threadName = threading.currentThread().getName()
            # temp local file
            fp = open(localFilePath + '.part.' + str(threadIndex), 'wb')
            callback = fp.write

            # another connection to ftp server, change to path, and set binary mode
            myFtp = FTP(self.host, self.user, self.passwd)
            myFtp.cwd(os.path.dirname(remoteFilePath))
            myFtp.voidcmd('TYPE I')

            finishedSize = 0
            # where to begin downloading
            setBeginPoint = 'REST ' + str(beginPoint)
            myFtp.sendcmd(setBeginPoint)
            # begin to download
            beginToDownload = 'RETR ' + os.path.basename(remoteFilePath)
            connection = myFtp.transfercmd(beginToDownload, rest)
            readSize = self.fixBlockSize
            while 1:
                if blockSize > 0:
                    remainedSize = blockSize - finishedSize
                    if remainedSize > self.fixBlockSize:
                        readSize = self.fixBlockSize
                    else:
                        readSize = remainedSize
                data = connection.recv(readSize)
                if not data:
                    break
                finishedSize = finishedSize + len(data)
                # make sure the finished data no more than blockSize
                if finishedSize == blockSize:
                    callback(data)
                    break
                callback(data)
            connection.close()
            fp.close()
            myFtp.quit()
            return True
        except:
            return False

    def setupThreads(self, filePath, localFilePath, threadNumber = 20):
        """
        set up the threads which will be used to download images
        list of threads will be returned if success, else
        None will be returned
        """
        try:
            print(str(filePath))
            print(str(self.ftp))
            temp = self.ftp.sendcmd('SIZE ' + filePath)
            print(str(temp))
            remoteFileSize = int(str.split(temp)[1])
            blockSize = remoteFileSize / threadNumber
            rest = None
            threads = []
            for i in range(0, threadNumber - 1):
                beginPoint = blockSize * i
                subThread = threading.Thread(target = self.downloadFileMultiThreads, args = (i, filePath, localFilePath, beginPoint, blockSize, rest,))
                threads.append(subThread)

            assigned = blockSize * threadNumber
            unassigned = remoteFileSize - assigned
            lastBlockSize = blockSize + unassigned
            beginPoint = blockSize * (threadNumber - 1)
            subThread = threading.Thread(target = self.downloadFileMultiThreads, args = (threadNumber - 1, filePath, localFilePath, beginPoint, lastBlockSize, rest,))
            threads.append(subThread)
            return threads
        except:
            #self.recordLog(str(diag), 'error')
            return None