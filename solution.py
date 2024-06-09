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
    # get the course code
    code = prereq["code"] if "code" in prereq else None
    # check if code is in the completedCourses array
    return code in course_data["completedCourses"]


def handle_course_2(course_data, prereq):
    code = prereq["code"] if "code" in prereq else None
    complete = code in course_data["completedCourses"]
    return (complete, code)


def handle_and(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ors_ = filter(lambda obj_: obj_["type"] == "or", operands)
    courses = (handle_course(course_data, course) for course in courses_)
    ors = (handle_or(course_data, or_) for or_ in ors_)
    return chain(courses, ors)


def handle_and_2(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ors_ = filter(lambda obj_: obj_["type"] == "or", operands)
    courses = (handle_course_2(course_data, course) for course in courses_)
    ors = (handle_or_2(course_data, or_) for or_ in ors_)
    return list(chain(courses, ors))


def handle_or(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ands_ = filter(lambda obj_: obj_["type"] == "and", operands)
    courses = (handle_course(course_data, course) for course in courses_)
    ands = (handle_and(course_data, and_) for and_ in ands_)
    return chain(courses, ands)


def handle_or_2(course_data, prereq):
    operands = prereq["operands"]
    courses_ = filter(lambda obj_: obj_["type"] == "course", operands)
    ands_ = filter(lambda obj_: obj_["type"] == "and", operands)
    courses = (handle_course_2(course_data, course) for course in courses_)
    ands = (handle_and_2(course_data, and_) for and_ in ands_)
    return list(chain(courses, ands))


def handle_prereqs(course, prereq):
    match prereq["type"]:
        case "course":
            return handle_course(course, prereq)
        case "and":
            return handle_and(course, prereq)
        case "or":
            return handle_or(course, prereq)


def handle_prereqs_2(course, prereq):
    match prereq["type"]:
        case "course":
            return handle_course_2(course, prereq)
        case "and":
            return handle_and_2(course, prereq)
        case "or":
            return handle_or_2(course, prereq)


def create_output_course(course, result):
    course["isSatisfied"] = True if result else False
    return course


def check(obj, prereqs):
    course = obj["course"] if "course" in obj else None
    prereqs_ = prereqs[course]
    if prereqs_ is not None:
        return handle_prereqs(obj, prereqs_)
    return True


def check2(obj, prereqs):
    course = obj["course"] if "course" in obj else None
    prereqs_ = prereqs[course]
    if prereqs_ is not None:
        return handle_prereqs_2(obj, prereqs_)
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


def create_output_course_2(course, result):
    if isinstance(result, list):
        result = reduce(course_rf, result, [])
    if isinstance(result, bool) and result:
        result = []
    elif isinstance(result, tuple):
        result = result[1] if not result[0] else None
    course["coursesNeeded"] = result if result != [] else None
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


def run_solution_2():
    prerequisites = read_prerequisites()
    tests = read_input()
    for obj_ in tests:
        result = check2(obj_, prerequisites)
        create_output_course_2(obj_, result)
    with open("output.json", "w") as out:
        json.dump(tests, out, indent=4)


if __name__ == "__main__":
    run_solution_2()
