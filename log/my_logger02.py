"""
RotatingFileHandler（按大小切割）
这个例子演示了当单个日志文件超过 1MB 时，就自动创建一个新的日志文件，最多保留 5 个备份文件。
创建循环文件处理器，基于日志文件的大小进行切割
    RotatingFileHandler
    参数:
        filename: 基础日志文件名 (e.g. 'app.log')
        maxBytes: 单个文件的最大字节数 (e.g. 1MB)
        backupCount: 保留的备份文件数量 (e.g. 5个)
        encoding: 推荐指定编码，避免中文乱码(e.g. 'utf-8')
"""
import logging
import logging.handlers


def init_logger(log_file='log02/app.log'):
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

    # 创建循环文件处理器，基于日志文件的大小进行切割
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=1 * 1024 * 1024,   # 1MB
        backupCount=5,
        encoding='utf-8'    # 推荐指定编码，避免中文乱码
    )
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(formatter)

    # 将handler添加到logger
    logger.addHandler(console_handler)
    logger.addHandler(rotating_file_handler)

    return logger


def main():
    log = init_logger()

    # 记录不同级别的日志
    log.debug('debug message, e.g.这是一条调试信息')
    log.info('info message, e.g.程序启动成功')
    log.warning('warning message, e.g.磁盘空间不足')
    log.error('error message, e.g.文件读取失败')
    log.critical('critical message, e.g.系统即将崩溃')

    # 测试日志输出
    user = 'admin'
    action = ['login', 'logout']
    for i in range(50000):
        if i % 2 == 0:
            log.info(f"用户[{user}]执行了[{action[0]}]操作")
        else:
            log.warning(f"用户[{user}]执行了[{action[1]}]操作")


if __name__ == '__main__':
    main()
