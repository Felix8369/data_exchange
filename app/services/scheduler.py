import os, fcntl, atexit
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler


def scheduler_init(app):
    """
    计划任务初始化
    使用文件锁保证在多进程下只有一个任务在运行
    :param app: Flask app
    :return:
    """

    base_dir = app.config.get('BASE_DIR')
    if base_dir is None:
        lock_file = '/tmp/scheduler.lock'
    else:
        lock_file = os.path.join(base_dir, 'logs', 'scheduler.lock')

    f = open(lock_file, 'wb')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)

        # 注册任务
        app.scheduler = BackgroundScheduler(timezone='Asia/Shanghai', executors=dict(default=ThreadPoolExecutor(10)))

        if app.config['VMM_TASK_SCHEDULER']:
            app.scheduler.add_job(func=do_task, trigger='cron', second='*/3', args=[app])

        app.scheduler.start()
    except BlockingIOError:
        pass
    except Exception as e:
        app.logger.error(e)

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

    atexit.register(unlock)


def do_task(app):
    """
    定时任务
    :param app:
    :return:
    """

    with app.app_context():
        pass
