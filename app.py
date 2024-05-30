import json
 
 

 
# function to check if prerequisite is satisifed
def checkPreq(course_code, prereq, completed_courses):
  # iterating through each input in the prereq file
    course_prereq = prereq.get(course_code)
    needed_courses = set()
 
    # inner function to check for the prereq and generate the result
    def evaluate_requirement(requirement):
      # if no prereqs, return true(as they cn directly enroll into the course)
        if requirement is None:
            return True
      # if directly course is mentioned, check if is completed already
        if requirement['type'] == 'course':
            if requirement['code'] not in completed_courses:
                needed_courses.add(requirement['code'])
                return False
            return True
      # handling operands
        elif requirement['type'] == 'and':
            result = True
            for sub_req in requirement['operands']:
                if not evaluate_requirement(sub_req):
                    result = False
            return result
        elif requirement['type'] == 'or':
            result = False
            for sub_req in requirement['operands']:
                if evaluate_requirement(sub_req):
                    return True
            for sub_req in requirement['operands']:
                evaluate_requirement(sub_req)  
            return result
        return False
 
    is_satisfied = evaluate_requirement(course_prereq)
 
    # generating json output of the fuction in the required output format
    result = {
            "course": course_code,  # The course that was evaluated - copied from the test data
            "completedCourses": completed_courses,  # The list of courses already completed - copied from the test data
            "isSatisfied": is_satisfied,  # The output your code produced from part 1.
            "coursesNeeded": list(needed_courses) # The output your code produced from part 2
        }
    return result
 
if __name__ == "__main__":

    # reading the prerequisite file and storing it for input 
    f = open('data/prerequisites.json') 
    prereq_data = json.load(f)

    # reading test data
    f = open('data/tests.json') 
    test_data = json.load(f)
    
    final_res = []
    # iterating through each test case and generating result for it
    for test in test_data:
        final_res.append(checkPreq(test['course'], prereq_data, test['completedCourses']))
    
    # writing the concatenated output into the output file
    with open('output.json', 'w') as file:
        json.dump(final_res, file, indent=2)