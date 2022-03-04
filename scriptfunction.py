import os
import subprocess
import time
from datetime import datetime


class LogHandler(object):
    # 这是用来将各个脚本的输出和报错储存到.txt文件中去
    def __init__(self):
        # 设定日志文件路径
        self.log_path = './log/'
    def write_date(self, name):
        out_log = open(self.log_path + name[:-3] + '_out.txt', 'a+')
        err_log = open(self.log_path + name[:-3] + '_err.txt', 'a+')
        out_log.write('\n' + str(datetime.now()) + '\n\n')
        err_log.write('\n' + str(datetime.now()) + '\n\n')
        out_log.close()
        err_log.close()
    def get_log(self, name):
        # 获取日志，然后创建或追加内容
        # get log of current script
        self.write_date(name)
        # time.sleep(0.1)
        out_log = open(self.log_path + name[:-3] + '_out.txt', 'a+')
        err_log = open(self.log_path + name[:-3] + '_err.txt', 'a+')
        return out_log, err_log

    def reset_log(self, name):
        # 重置脚本日志
        out_log = open(self.log_path + name[:-3] + '_out.txt', 'w')
        err_log = open(self.log_path + name[:-3] + '_err.txt', 'w')
        out_log.write('')
        err_log.write('')
        out_log.close()
        err_log.close()

    def delete_log(self, name):
        # 删除日志
        os.remove(self.log_path + name[:-3] + '_out.txt')
        os.remove(self.log_path + name[:-3] + '_err.txt')


class ScriptManager(object):
    def __init__(self):
        self.log = LogHandler()
        self.path = os.getcwd() + '\\'
        # save all running scripts {'name':process}
        self.processes = {}

    def get_scripts(self):
        # 获取该目录下所有脚本
        # Get a list of scripts(.py file) in the path. (scriptfunction.py not include)
        py_files = [f for f in os.listdir(self.path) if os.path.isfile(f) and f[-3:] == '.py']
        return py_files

    def get_running_status(self, name):
        # 获取该脚本运行状态
        # check if the script is running
        # None 为正在运行 0为不在运行 1为进程终止
        status = self.processes[name].poll()
        if status is None:
            return True
        elif status in [0,1]:
            return False
        else:
            print('running status error')
            return False

    def get_all_status(self):
        # 获取所有脚本的运行状态 是否正在运行
        # Get a list scripts that currently running
        status = {}
        time.sleep(0.1)

        for p in self.processes:
            status[p] = self.get_running_status(p)
        return status

    def run_script(self, name):
        # 运行脚本
        # run the script
        # To avoid run too many scripts at once
        time.sleep(1)
        out_log, err_log = self.log.get_log(name)
        command = 'python ' + self.path + name
        self.processes[name] = subprocess.Popen(command, stdout=out_log, stderr=err_log)
        return True

    def run_scripts(self, names):
        # 运行列表(names)内所有的脚本
        # run a list of scripts
        for name in names:
            if not self.run_script(name):
                return False
        return True

    def stop_script(self, name):
        # 停止脚本
        # stop the script
        # To avoid close too many scripts at once
        time.sleep(0.1)
        if name in list(self.processes.keys()):
            self.processes[name].terminate()
        else:
            print('Script not exist.')
            return False
        return True

    def stop_scripts(self, names):
        # 停止列表内所有脚本
        # stop a list of scripts
        for name in names:
            self.stop_script(name)
        return True

    def restart_script(self, name):
        # 重启脚本
        # restart the script
        if self.stop_script(name):
            if self.run_script(name):
                return True

    def restart_scripts(self, names):
        # 重启列表内所有脚本
        # restart a list of scripts
        for name in names:
            if self.restart_script(name):
                print('Script' + name + 'restart failure.')
        return True

    def restart_all(self):
        # 重启列表内所有脚本
        # restart a list of scripts
        for name in self.processes:
            if self.restart_script(name):
                print('Script' + name + 'restart failure.')
        return True

    def stop_all(self):
        # 停止全部脚本
        # stop all currently running scripts
        for name in self.processes:
            self.stop_script(name)

    def del_script(self, name):
        # 还是手动删除吧
        # delete the script
        return


# class DatabaseChecker(object):
#     def __init__(self):
#         self.address = '192.168.3.189'
#         self.port = 9999
#
#     def get_db_status(self):
#         client = pymongo.MongoClient(self.address, self.port)
#         try:
#             client.server_info()
#         except:
#             return False
#         else:
#             return True


if __name__ == '__main__':
    SM = ScriptManager()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    print('脚本列表: ', SM.get_scripts())
    print('运行脚本1: ', SM.run_script('script1.py'))
    print('运行[脚本1,脚本2]: ', SM.run_scripts(['script1.py', 'script2.py']))
    print('检查脚本1运行状态: ', SM.get_running_status('script1.py'))
    print('待机1s')
    time.sleep(1)
    print('检查脚本2运行状态: ', SM.get_running_status('script2.py'))
    # time.sleep(2)
    # print('停止脚本: ', SM.stop_script('script2.py'))

    print('获取全部脚本运行状态: ', SM.get_all_status())
    # print(LogHandler().reset_log('script1.py'))
    print('end')