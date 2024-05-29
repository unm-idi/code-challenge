import json

# Function to load prerequisites from json file
def load_prerequisites(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
# Function to check if a course can be taken given the completed courses and prerequisites
def can_take_course(course, completed_courses, prerequisites):
    # Helper function to recursively check if a prerequisite is met
    def check_prerequisite(prereq):
        if prereq["type"] == "course": # if prereq is a single course
            return prereq["code"] in completed_courses
        elif prereq["type"] == "and":
            return all(check_prerequisite(op) for op in prereq["operands"]) # recursively checks all sub-requirements
        elif prereq["type"] == "or":
            return any(check_prerequisite(op) for op in prereq["operands"])
        
    course_prereq = prerequisites.get(course)
    if not course_prereq:
        return True # No preerequisites for the course
        
    return check_prerequisite(course_prereq)
    
# Function to find the list of courses needed to satisfy the prerequisites for a given course
def courses_needed(course, completed_courses, prerequisites):
    needed_courses = []

    # Helper function to recursively find courses
    def find_needed_courses(prereq):
        if prereq["type"] == "course":
            if prereq["code"] not in completed_courses:
                needed_courses.append(prereq["code"]) # Add course if not already completed
        elif prereq["type"] == "and":
            for op in prereq["operands"]:
                find_needed_courses(op) # Recursively check all operands
        elif prereq["type"] == "or":
            for op in prereq["operands"]:
                # If one of the options is already satisfied we don't need to add more courses
                if (op["type"] == "course" and can_take_course(op["code"], completed_courses, prerequisites)) or \
                   (op["type"] in ["and", "or"] and can_take_course(course, completed_courses, prerequisites)):
                    return
            # Otherwise, add the first needed option
            find_needed_courses(prereq["operands"][0])

    course_prereq = prerequisites.get(course)
    if course_prereq:
        find_needed_courses(course_prereq)

    return needed_courses

# Function to process the test cases and generate the output file
def process_tests(tests_file, prerequisites_file, output_file):
    # Load prerequisites from file
    prerequisites = load_prerequisites(prerequisites_file)

    # Load test cases from file
    with open(tests_file, 'r') as file:
        tests = json.load(file)

    output = []

    # Iterate over each test case in the tests list
    for test in tests:
        course = test["course"]
        completed_courses = test["completedCourses"]
        # Determine if the course can be taken
        is_satisfied = can_take_course(course, completed_courses, prerequisites)
        # Determine the list of needed courses to satisfy prerequisites
        courses_needed_list = courses_needed(course, completed_courses, prerequisites)

        output.append({
            "course": course,
            "completedCourses": completed_courses,
            "isSatisfied": is_satisfied,
            "coursesNeeded": courses_needed_list
        })

    # Write the output to file
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=2)

# Process tests and generate output file
process_tests('data/tests.json', 'data/prerequisites.json', 'output.json')