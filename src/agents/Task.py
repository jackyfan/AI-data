from collections import defaultdict, deque
from utility.logger_helper import LoggerHelper

logger = LoggerHelper.get_logger(__name__)


class SubTask(object):
    """
    定义子任务
    """

    def __init__(self, serial_id, name, dependencies, execute_function, step):
        self.serial_id = serial_id
        self.name = name
        self.step = step
        self.dependencies = dependencies
        self.execute_function = execute_function
        self.result = None

    def execute(self, dependencies):
        self.result = self.execute_function(self, dependencies)
        self.step["sql"] = self.result
        return self.result


class TaskScheduler:
    """
    任务调度与依赖管理
    """

    def __init__(self, tasks):
        self.tasks = tasks
        self.dependency_graph, self.indegrees = self.build_dependency_graph(self.tasks)

    def get_execution_order(self):
        """使用拓扑排序算法计算任务的执行顺序"""
        queue = deque([task_id for task_id in self.indegrees if self.indegrees[task_id] == 0])
        execution_order = []
        while queue:
            task_id = queue.popleft()
            execution_order.append(task_id)
            for dependent in self.dependency_graph[task_id]:
                self.indegrees[dependent] -= 1
                if self.indegrees[dependent] == 0:
                    queue.append(dependent)
        if len(execution_order) != len(self.tasks):
            raise ValueError("存在循环依赖，无法完成所有任务调度。")
        return execution_order

    def build_dependency_graph(self, tasks):
        """构建任务的依赖图，同时计算每个任务的入度"""
        graph = defaultdict(list)
        for task in tasks:
            logger.debug(f'{task.serial_id=}')
        indegrees = {index: 0 for index, _ in enumerate(tasks)}
        for task in tasks:
            for dependency in task.dependencies:
                graph[dependency].append(task.serial_id)
                logger.debug(f'before:{indegrees[task.serial_id]=}')
                indegrees[task.serial_id] += 1
                logger.debug(f'after:{indegrees[task.serial_id]=}')
        logger.debug(f'after:{indegrees=}')
        return graph, indegrees

    def execute_tasks(self):
        """
        按照依赖顺序执行所有任务
        :return:
        """
        execution_order = self.get_execution_order()
        results = {}
        for serial_id in execution_order:
            task = self.tasks[serial_id]
            dep_results = [self.tasks[dep].result for dep in task.dependencies]
            results = task.execute(dep_results)
        return results
