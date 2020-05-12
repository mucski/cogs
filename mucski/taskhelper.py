class TaskHelper:
    def __init__(self):
        self.tasks = []
        
    def cog_unload(self):
        for task in list(self.tasks):
            task.cancel()
            
    def schedule_task(self, coro):
        task = asyncio.create_task(coro)
        task.add_done_callback(lambda t: self.tasks.remove(task))
        self.tasks.append(task)