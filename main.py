import sys
import os
import multiprocessing
import inspect
import importlib.util
import time
from datetime import datetime

from Schedule import Periodic

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        raise Exception("No location task specified")
    module_paths = []
    for p in args[1:]:
        if os.path.isdir(p):
            for m in os.listdir(p):
                if m.split('.')[-1] == "py":
                    module_paths.append(os.path.join(p, m))
    task_modules = []
    for m in module_paths:
        spec = importlib.util.spec_from_file_location("my_module", m)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        task_modules.append(module)
    jobs = list()
    for module in task_modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and obj.__dict__.get("__decorator_name__", None) == "job":
                schedule = Periodic(*obj.__dict__.get("__schedule__"))
                jobs.append({"task": obj, "schedule": schedule})
    while True:
        now = datetime.now()
        for job in jobs:
            schedule = job.get("schedule")
            task = job.get("task")
            next_time = job.get("next_time", schedule.get_next_time())
            if next_time < now:
                multiprocessing.Process(target=task).start()
                job["next_time"] = schedule.get_next_time()
            else:
                job["next_time"] = next_time
        time.sleep(1)
