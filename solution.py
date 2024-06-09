from functools import reduce
from itertools import chain
import json
from pathlib import Path


def read_input():
    file_bytes = Path("data/tests.json").read_bytes()
    return json.loads(file_bytes)


def read_prerequisites():
    file_bytes = Path("data/prerequisites.json").read_bytes()
    return json.loads(file_bytes)


def handle_course(course_data, prereq):
    code = prereq["code"] if "code" in prereq else None
    complete = code in course_data["completedCourses"]
    return (complete, code)


def handle_and(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ors_ = filter(lambda obj_: obj_["type"] == "or", operands)
    courses = (handle_course(course_data, course) for course in courses_)
    ors = (handle_or(course_data, or_) for or_ in ors_)
    return list(chain(courses, ors))


def handle_or(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ands_ = filter(lambda obj_: obj_["type"] == "and", operands)
    courses = (handle_course(course_data, course) for course in courses_)
    ands = (handle_and(course_data, and_) for and_ in ands_)
    return list(chain(courses, ands))


def handle_prereqs(course, prereq):
    match prereq["type"]:
        case "course":
            return handle_course(course, prereq)
        case "and":
            return handle_and(course, prereq)
        case "or":
            return handle_or(course, prereq)


def check(obj, prereqs):
    course = obj["course"] if "course" in obj else None
    prereqs_ = prereqs[course]
    if prereqs_ is not None:
        return handle_prereqs(obj, prereqs_)
    return []


def course_rf(acc: list, val):
    if isinstance(val, tuple):
        (val_, code) = val
        if not val_:
            acc.append(code)
            return acc
    if isinstance(val, list):
        # check for the existence of a true value in a sub-list
        vals_ = any(map(lambda x: x[1], val))
        if vals_:
            return acc
        else:
            acc.append(vals_)
            return acc
    return acc


def create_output_course(course, result):
    if isinstance(result, list):
        result = reduce(course_rf, result, [])
    if isinstance(result, bool) and result:
        result = []
    elif isinstance(result, tuple):
        result = result[1] if not result[0] else None
    if result != []:
        course["coursesNeeded"] = result
    course["isSatisfied"] = False if result else True
    return course


def run_solution():
    prerequisites = read_prerequisites()
    tests = read_input()
    for obj_ in tests:
        result = check(obj_, prerequisites)
        create_output_course(obj_, result)
    with open("output.json", "w") as out:
        json.dump(tests, out, indent=4)


if __name__ == "__main__":
    run_solution()
