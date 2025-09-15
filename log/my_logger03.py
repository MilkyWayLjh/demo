"""
TimedRotatingFileHandler（按时间切割）
这个例子演示了每天午夜（服务器时间）切割一次日志文件，并保留最近 7 天的备份。
TimedRotatingFileHandler
参数:
    filename: 基础日志文件名
    when: 时间间隔单位 ('S'-秒, 'M'-分, 'H'-小时, 'D'-天, 'W0'-W6-周, 'midnight'-午夜)
        when 参数的常用值：
            'S'：秒; 'M'：分钟; 'H'：小时; 'D'：天; 'W0' - 'W6'：每周（0 代表周一，6 代表周日）
            'midnight'：每天午夜（等同于 'D' 但时间点更明确）
    interval: 间隔数 (e.g., when='D', interval=1 -> 每天)
    backupCount: 保留的备份文件数量
    utc: 是否使用 UTC 时间 (默认 False，使用本地时间)
    atTime: 如果 when='midnight'，可以用这个指定“午夜”的具体时间
    # atTime=datetime.time(hour=0, minute=0, second=0) # 明确指定午夜时间，默认就是00:00:00
"""
import logging
import logging.handlers


def init_logger(log_file='log03/app.log'):
    """
    初始化日志
    :param log_file: 日志文件,默认为 app.log
    :return:
    """
    # 创建一个日志实例
    logger = logging.getLogger(__name__)    # __name__ 是一个内置变量，它的值就是当前模块的完整名称
    logger.setLevel(logging.DEBUG)

    # 创建Formatter：格式化器，定义日志的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

    # 创建控制台handler并设置级别为INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 定时循环文件处理器，基于日志文件的时间进行切割
    time_rotating_file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',    # 午夜时间，默认就是00:00:00
        # when='S',    # 秒
        interval=1,     # 间隔1天
        backupCount=7,  # 保留7个备份
        encoding='utf-8'
    )
    time_rotating_file_handler.setLevel(logging.DEBUG)
    time_rotating_file_handler.setFormatter(formatter)

    # 将handler添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(time_rotating_file_handler)

    return logger


def main():
    log = init_logger()

    # 记录不同级别的日志
    # log.debug('debug message, e.g.这是一条调试信息')
    # log.info('info message, e.g.程序启动成功')
    # log.warning('warning message, e.g.磁盘空间不足')
    # log.error('error message, e.g.文件读取失败')
    # log.critical('critical message, e.g.系统即将崩溃')

    # 测试日志输出
    robot = 'REAL_ROBOT_MK6'
    action = ['没有分配的充电桩!', '传感器异常!']
    for i in range(50000):
        if i % 2 == 0:
            log.error(f"机器人[{robot}]存在[{action[0]}]")
        else:
            log.critical(f"机器人[{robot}]存在[{action[1]}]")


if __name__ == '__main__':
    main()
