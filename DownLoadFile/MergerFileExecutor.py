__author__ = 'jishu12'
import urllib.request
import sys
import os
import threading
import pickle
import time
def mergerFile(self, localFile, threadNumber):
    """
    Meger all the sub parts of the file into 1 file
    another thread will be call to do this
    """
    try:
        while 1:
            subThread = threading.Thread(target = self.mergeFileExecutor, args = (localFile, threadNumber,))
            subThread.start()
            subThread.join()
            if 1 == self.mergerFlag:
                self.mergerFlag = 0
                return False
            # check if total size of part file equals to size of the whole file
            localFileSize = os.path.getsize(localFile)
            totalSize = 0
            for i in range(0, threadNumber):
                totalSize += os.path.getsize(localFile + '.part.' + str(i))
            if localFileSize == totalSize:
                break
        return True
    except:
        pass
        #self.recordLog(str(diag), 'error')
        return False

def mergerFileExecutor(self, localFile, threadNumber):
    try:
        errorFlag = 0
        fw = open(localFile, 'wb')
        for i in range(0, threadNumber):
            fname = localFile + '.part.' + str(i)
            if not os.path.exists(fname):
                errorFlag = 1
                break
            fr = open(fname, 'rb')
            data = fr.read()
            time.sleep(2)
            fr.close()
            fw.write(data)
            fw.flush()
            time.sleep(1)
        fw.close()
        if 1 == errorFlag:
            # some part file is not available
            self.mergerFlag = 1
    except:
        pass
        # error occr
        #self.mergerFlag = 1
        #self.recordLog(str(diag), 'error')

def checkSizeEqual(self, remoteFile, localFile):
    '''
    check the remote file size and the local file size.
    if =, return true,
    else, return false
    '''
    try:
        remoteFileSize = self.ftp.size(remoteFile)
        localFileSize = os.path.getsize(localFile)
        if localFileSize == remoteFileSize:
            return True
        else:
            return False
    except:
        pass
        #print diag