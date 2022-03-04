import pandas as pd
import time
from scriptfunction import ScriptManager


class ScriptChecker(object):
    def __init__(self, df):
        self.df = df
        self.scripts = SM.get_all_status()

    def run_checker(self):
        # 检查是否需要运行脚本
        # 首先获取列表中需要运行所有脚本
        # 然后检查processes中的脚本: 如果不存在或为False, 那么启动它
        should_running = list()
        for script in df.index:
            if self.df['type'][script]:
                should_running.append(script + '.py')
        running_script = [s for s in self.scripts if self.scripts[s]]
        should_run = [s for s in should_running if s not in running_script]
        SM.run_scripts(should_run)
        return should_run

    def stop_checker(self):
        # 检查是否需要停止脚本
        should_stop = list()
        # 检查processes中的脚本: 如果正在运行并且应该停止，那么终止它
        for script in self.scripts.keys():
            if self.scripts[script] and not self.df['type'][script[:-3]]:
                should_stop.append(script)
        SM.stop_scripts(should_stop)
        return should_stop

    def restart_checker(self, restart_time, last_time):
        # 检查是否需要重启脚本
        # 确认是否在重启时间，以及上次重启跟这次重启必须间隔1h
        if time.localtime().tm_hour == restart_time and time.time() - last_time > 3600:
            should_restart = list()
            for script in self.scripts.keys():
                if self.scripts[script]:
                    should_restart.append(script)
            SM.restart_scripts(should_restart)
            print('\n---------Restart---------\n')
            print('Restart scripts: ', should_restart)
            return True
        else:
            return False

    def issue_recorder(self):
        return


if __name__ == '__main__':
    # parameters required
    path = 'script_parm.csv'
    # loop time of main script
    loop_time = 5
    # 0~24h
    restart_time = 11

    # initialization
    last_restart = 0
    df = pd.read_csv(path, index_col=0)
    SM = ScriptManager()

    while True:
        # 读取新表格并更新至ScriptChecker中
        df = pd.read_csv(path, index_col=0)
        SC = ScriptChecker(df)
        # 检查是否需要重启
        if SC.restart_checker(restart_time, last_restart):
            last_restart = time.time()
        # 执行检查并输出
        print('current process:   ', SM.get_all_status())
        print('start scripts:     ', SC.run_checker())
        print('Terminate scripts: ', SC.stop_checker())

        time.sleep(loop_time)