import sys,os
from loguru import logger
#获得该项目的绝对路径
root_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir=os.path.join(root_dir,"logs")#存放日志的绝对路径
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
Log_file="translation.log"

class mylogger:
    def __init__(self):
        self.logger=logger#添加写日志的对象
        self.logger.remove()#清空所有的设置
        #添加控制台商输出的格式，sys.stdout为输出到屏幕
        self.logger.add(sys.stdout,level="DEBUG",
                        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                            "{process.name}|"#进程名
                            "{thread.name}|"#线程名
                            "<cyan>{module}:</cyan>.<cyan>{function}</cyan>"#模块名。方法名
                            ":<cyan>{line}</cyan>|"#行号
                            "<level>{level}</level>:" #等级
                            "<level>{message}</level>", #日志内容
                        )
        #输出到文件的格式，注释下面的add，则关闭日志写入
        log_file_path = os.path.join(log_dir, Log_file)
        self.logger.add(log_file_path, level="DEBUG",encoding="utf-8",
                        format="{time:YYYY-MM-DD HH:mm:ss}-"
                               " {process.name}|"
                               " {thread.name}|"
                                '{module}:{function}:{line} -{level}-{message}',
                        rotation="10 MB",
                        retention="20 days",
                        )
    def get_logger(self):
        return self.logger
log=mylogger().get_logger()

if __name__=="__main__":
    # log.debug("这是debug")
    # log.info("这是info")
    # log.warning("warning")
    # log.error("error")
    # log.trace("trace")
    print('str.pdf'['str.pdf'.rindex('.'):])
    def test():
        try:
            print(3/0)
        except ZeroDivisionError as e:
            log.exception(e)
    test()
