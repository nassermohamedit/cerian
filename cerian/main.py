import sys
import os
import inspect
import importlib.util
import time
from multiprocessing import Process


def time_loop(jobs):
    while True:
        for job in jobs:
            if job[1].tick():
                Process(target=job[0]).start()
        time.sleep(0.1)


def find_jobs(locations: list[str]) -> list[callable]:
    locations = filter(lambda loc: os.path.isdir(loc), locations)
    py_modules = list()
    for loc in locations:
        loc_py_modules = filter(lambda file: file.split('.')[-1] == "py", os.listdir(loc))
        loc_py_modules = map(lambda file: os.path.join(loc, file), loc_py_modules)
        py_modules.extend(list(loc_py_modules))
    module_objects = []
    for m in py_modules:
        spec = importlib.util.spec_from_file_location("py_module", m)
        module_obj = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_obj)
        module_objects.append(module_obj)
    jobs = list()
    for module in module_objects:
        jobs_objects = filter(lambda mem: inspect.isfunction(mem[1]), inspect.getmembers(module))
        jobs_objects = filter(lambda mem: mem[1].__dict__.get("is_job", False), jobs_objects)
        jobs_objects = map(lambda mem: (mem[1], mem[1].__dict__.get('schedule')), jobs_objects)
        jobs.extend(list(jobs_objects))
    return jobs


if __name__ == "__main__":
    print("cerian")
    args = sys.argv
    if len(args) < 2:
        raise Exception("No location task specified")
    jobs = find_jobs(sys.argv[1:])
    time_loop(jobs)
