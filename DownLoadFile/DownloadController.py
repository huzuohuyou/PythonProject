from threads.DownLoadService import FtpDownLoad

def Do():

    service = FtpDownLoad()
    service.setupThreads('ftp://107.182.182.93/pub/test.tgz','D://Docs/test.tgz',20)

Do()