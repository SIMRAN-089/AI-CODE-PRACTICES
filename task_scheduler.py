import heapq

class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.dependencies = []
        self.dependents = []  # Track tasks that depend on this one

    def add_dependency(self, task):
        self.dependencies.append(task)
        task.dependents.append(self)

class TaskGraph:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, duration):
        self.tasks[name] = Task(name, duration)

    def add_dependency(self, task_name, dependency_name):
        if task_name in self.tasks and dependency_name in self.tasks:
            self.tasks[task_name].add_dependency(self.tasks[dependency_name])

    def heuristic(self, task):
        """ Heuristic: Compute longest path to completion """
        memo = {}

        def dfs(t):
            if t in memo:
                return memo[t]
            if not t.dependents:
                return t.duration
            memo[t] = t.duration + max(dfs(dep) for dep in t.dependents)
            return memo[t]

        return dfs(task)

    def a_star_scheduling(self):
        """ A* Scheduling using longest path estimation """
        pq = []
        in_degree = {task: len(task.dependencies) for task in self.tasks.values()}

        for task in self.tasks.values():
            if in_degree[task] == 0:
                heapq.heappush(pq, (self.heuristic(task), task.duration, task.name, task))

        execution_order = []
        while pq:
            _, _, _, current = heapq.heappop(pq)
            execution_order.append(current.name)

            for dependent in current.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    heapq.heappush(pq, (self.heuristic(dependent), dependent.duration, dependent.name, dependent))

        return execution_order

    def greedy_scheduling(self):
        """ Greedy algorithm: Pick shortest available task first while ensuring dependencies are met """
        in_degree = {task: len(task.dependencies) for task in self.tasks.values()}
        ready_tasks = [task for task in self.tasks.values() if in_degree[task] == 0]
        ready_tasks.sort(key=lambda x: x.duration)  # Sort by shortest duration

        execution_order = []
        while ready_tasks:
            current = ready_tasks.pop(0)
            execution_order.append(current.name)

            for dependent in current.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    ready_tasks.append(dependent)
                    ready_tasks.sort(key=lambda x: x.duration)  # Keep sorting by shortest duration

        return execution_order


# Example Usage:
task_graph = TaskGraph()
task_graph.add_task("A", 3)
task_graph.add_task("B", 2)
task_graph.add_task("C", 4)
task_graph.add_task("D", 6)

task_graph.add_dependency("C", "A")
task_graph.add_dependency("C", "B")
task_graph.add_dependency("D", "C")

print("A* Scheduling Order:", task_graph.a_star_scheduling())
print("Greedy Scheduling Order:", task_graph.greedy_scheduling())
