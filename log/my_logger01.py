import logging
import logging.handlers
# from logging.handlers import RotatingFileHandler
# import os


def init_logger(log_file='app.log'):
    """
    初始化日志
    :param log_file: 日志文件,默认为app.log
    :return:
    """
    # 创建一个日志实例
    # logger = logging.getLogger(__name__)    # __name__ 是一个内置变量，它的值就是当前模块的完整名称
    logger = logging.getLogger('my_log')
    logger.setLevel(logging.DEBUG)  # 设置日志级别： DEBUG

    # 创建Formatter：格式化器，定义日志的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

    # 创建控制台handler并设置级别为INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 创建文件handler并设置级别为DEBUG
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 将handler添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def main():
    """主函数演示日志使用"""
    log = init_logger()

    # 记录不同级别的日志
    log.debug('debug message, e.g.这是一条调试信息')
    log.info('info message, e.g.程序启动成功')
    log.warning('warning message, e.g.磁盘空间不足')
    log.error('error message, e.g.文件读取失败')
    log.critical('critical message, e.g.系统即将崩溃')

    # 演示异常记录
    try:
        result = 10 / 0
    except Exception as e:
        log.exception(f"发生除零错误：除数不能为0, {e}")

    # 带参数的日志
    user = 'admin'
    action = 'login'
    log.info(f"用户[{user}]执行了[{action}]操作")

    # 测试日志输出
    for i in range(10000):
        log.debug(f"This is a test log message number {i}")


if __name__ == '__main__':
    main()
