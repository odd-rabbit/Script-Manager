import time
import pandas

if __name__ == '__main__':
    # 10秒来模拟脚本运行
    for i in range(5):
        print(i)
        time.sleep(2)
    # 模拟输出csv
    pandas.DataFrame({'1':'a'}, index=[0]).to_csv('out2.csv')