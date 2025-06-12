from agents.Task import SubTask, TaskScheduler
from models.model_gensql import sql_generate
from utility.logger_helper import LoggerHelper

logger = LoggerHelper.get_logger(__name__)


def invoke(steps):
    tasks = {}
    for step in steps["step"]:
        deps = step["dependence"]
        if deps == 0 or deps is None:
            deps = []
        dependencies = []
        for dep in deps:
            dependencies.append(dep)
        tasks[step["serial_id"]]=(SubTask(name=step["id"], dependencies=dependencies, execute_function=sql_generate, serial_id=step["serial_id"], step=step))
    logger.debug(f'2.1 任务：{tasks=}')
    scheduler = TaskScheduler(tasks)
    result = scheduler.execute_tasks()
    return result
