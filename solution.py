import json


# Load prerequisites from a JSON file
def load_prerequisites(file_path):
    with open(file_path, 'r') as prerequisites_file:
        prerequisites = json.load(prerequisites_file)
    return prerequisites


# Helper function to check if prerequisites are satisfied
def helper(operand, completed_courses, prerequisites):
    req_type = operand['type']

    # If the requirement is a single course, check if it's completed
    if req_type == 'course':
        return operand['code'] in completed_courses

    operands = operand.get('operands', [])

    # If the requirement is an 'and' type, all sub-requirements must be satisfied
    if req_type == 'and':
        return all(helper(op, completed_courses, prerequisites) for op in operands)
    # If the requirement is an 'or' type, at least one sub-requirement must be satisfied
    elif req_type == 'or':
        return any(helper(op, completed_courses, prerequisites) for op in operands)


# Function to determine if a course can be taken given completed courses and prerequisites
def can_take_course(course, completed_courses, prerequisites):
    req = prerequisites.get(course)
    if req is None:
        return True
    return helper(req, completed_courses, prerequisites)


# Helper function to find which courses are needed to satisfy a prerequisite
def courses_needed_helper(operand, completed_courses, prerequisites):
    req_type_helper = operand['type']

    if req_type_helper == 'course':
        if operand['code'] not in completed_courses:
            needed = courses_needed(operand['code'], completed_courses, prerequisites)
            needed.append(operand['code'])
            return needed
        return []

    operands = operand.get('operands', [])

    # If the requirement is an 'and' type, accumulate all needed courses for sub-requirements
    if req_type_helper == 'and':
        needed_courses = []
        for op in operands:
            needed_courses.extend(courses_needed_helper(op, completed_courses, prerequisites))
        return needed_courses
    # If the requirement is an 'or' type, find the shortest path of needed courses
    elif req_type_helper == 'or':
        shortest_path = None
        for op in operands:
            path = courses_needed_helper(op, completed_courses, prerequisites)
            if shortest_path is None or len(path) < len(shortest_path):
                shortest_path = path
        return shortest_path or []


# Function to find all courses needed to take a specific course
def courses_needed(course, completed_courses, prerequisites):
    req = prerequisites.get(course)
    if req is None:
        return []

    req_type = req['type']
    if req_type == 'course':
        if req['code'] not in completed_courses:
            needed = courses_needed(req['code'], completed_courses, prerequisites)
            needed.append(req['code'])
            return needed
        return []

    operands = req.get('operands', [])
    needed_courses = []

    # If the requirement is an 'and' type, accumulate all needed courses for sub-requirements
    if req_type == 'and':
        for op in operands:
            needed_courses.extend(courses_needed_helper(op, completed_courses, prerequisites))
    # If the requirement is an 'or' type, find the shortest path of needed courses
    elif req_type == 'or':
        shortest_path = None
        for op in operands:
            path = courses_needed_helper(op, completed_courses, prerequisites)
            if shortest_path is None or len(path) < len(shortest_path):
                shortest_path = path
        needed_courses.extend(shortest_path)

    return needed_courses


# Main function to process tests and generate output
def main():
    prerequisites = load_prerequisites('prerequisites.json')
    with open('tests.json', 'r') as file:
        tests = json.load(file)
    output = []
    for test in tests:
        course = test['course']
        completed_courses = test.get('completedCourses', [])
        is_satisfied = can_take_course(course, completed_courses, prerequisites)
        if is_satisfied:
            unique_course_needed_list = []
        else:
            courses_needed_list = courses_needed(course, completed_courses, prerequisites)
            unique_course_needed_list = list(set(courses_needed_list))

        output_item = {
            'course': course,
            'completedCourses': completed_courses,
            'isSatisfied': is_satisfied,
            'coursesNeeded': unique_course_needed_list
        }
        output.append(output_item)

    with open('output.json', 'w') as f:
        json.dump(output, f, indent=2)


# Entry point of the script
if __name__ == '__main__':
    main()
