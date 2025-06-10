from agents.Task import SubTask, TaskScheduler
from models.model_gensql import sql_generate


def invoke(steps):
    tasks = []
    for step in steps["step"]:
        deps = step["dependence"]
        if deps == 0 or deps == None:
            deps = []
        dependencies = []
        for dep in deps:
            dependencies.append(dep)
        tasks.append(SubTask(name=step["id"], dependencies=dependencies,execute_function=sql_generate, serial_id=step["serial_id"], step=step))

    scheduler=TaskScheduler(tasks)
    result = scheduler.execute_tasks()
    return result

