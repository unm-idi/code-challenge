# Programmer Analyst 2 Interview Problem

## Problem Definition
Before students can take a course at UNM, they must meet that courses prerequisite requirements. As a simple example, in order to take MATH 1250, a student must have completed MATH 1220. However, some prerequisite requirements are more complicated than simply requiring a single course. They can be a logical combination of multiple courses, or even other logical combinations. For example, the prerequisite requirement for MATH 1512 looks like `(MATH 1230 and MATH 1240) or MATH 1250`.

This problem consists of two parts:
1. Write code that determines if a given course can be taken provided a list of courses that have already been completed. A course's prerequisite requirements can be read from the file `data/prerequisites.json`. See the section _Course Prerequisite Data_ for details on how the data is formatted. Below is an example of the inputs and expected output for one scenario:
```
INPUTS:
  COURSE: 'MATH 1512'
  COMPLETED_COURSES: ['MATH 1215']
OUTPUT:
  false
```

2. Working off of your solution from part 1, modify your code to return a list of courses that the student will need to complete in order to satisfy the given course's prerequisite requirements. Note - while there could be multiple correct solutions, be careful not to include more courses than necessary. Below is an example of the inputs and expected output for one scenario:
```
INPUTS:
  COURSE: 'MATH 1512'
  COMPLETED_COURSES: ['MATH 1215']
OUTPUT:
  ['MATH 1220', 'MATH 1250']
  # In order to take MATH 1512, the student could complete MATH 1250 which requires MATH 1220, which requires MATH 1215.
```

## Instructions
1. Fork this repository.
2. Write your code to solve the two challenges listed above.
3. Using your code, create an output file that produces solutions for the scenarios listed in the `data/tests.json` file. Details can be found in the _Testing & Output File_ below.
4. Create a file named INSTRUCTIONS that detail how to run your code.
5. Commit and push your code.
6. Create a pull request.


### Considerations
- You may use any programming language you'd like, though python or ruby are preferred.
- Refrain from using any external libraries or code.
- As cool as ChatGPT is, please don't use it to write code for you.
- If you have any questions about the problem definition or the data, feel free to contact us at idi@unm.edu


## Course Prerequisite Data
In order to complete the above tasks, this repository includes a file,`data/prerequisites.json` that contain prerequisite requirements for several courses. The root object contains keys that represent a course code, and the value is an object specifying that course's prerequisite requirements.
```json
{
  "MATH 1512": { ...requirementObject },
  "MATH 1240": { ...requirementObject },
  "MATH 100": null
  ...  
}
```

Requirement objects come in three types:
- course: A course requirement indicates that a specific course (specified by the key *code*) must be completed in order to satisfy the requirement.
- and: An "and" requirement indicates that all sub requirements (specified by the key *operands*) must also be satisfied.
- or: An "or" requirement indicates that at least one sub-requirement (specified by the key *operands*) must be satisfied.

A course with null indicates that the course has no requirements and can always be taken.

Examples of the three requirement json objects can be seen below.
```json
{
  "type": "course",
  "code": "MATH 1240"
}

{
  "type": "and",
  "operands": [ ... ] // Contains multiple requirement objects
}

{
  "type": "or",
  "operands": [ ... ] // Contains multiple requirement objects
}
```

### Example
Putting this all together, the prerequisite requirements of `(MATH 1230 and MATH 1240) or MATH 1250` for the course MATH 1512 would look like:
```json
{
  "MATH 1512": {
    "type": "or",
    "operands": [
      {
        "type": "and",
        "operands": [
          {
            "type": "course",
            "code": "MATH 1230"
          },
          {
            "type": "course",
            "code": "MATH 1240"
          }
        ]
      },
      {
        "type": "course",
        "code": "MATH 1250"
      }
    ]
  },
  ...
}
```

## Testing & Output File
#### Test Data Format
The file `data/tests.json` contains a list of json objects that represent a scenario to evaluate. They also contain the expected solution to part 1. The objects look like:
```json
[
  {
    "course": "MATH 1512",                // The course to evaluate
    "completedCourses": ["MATH 1250"],    // Course that have already been completed
    "isSatisfied": true                   // Some cases contain the expected solution to part 1 to serve as a guide
  },
  ...
]
```

#### Output File Format
In order for us to evaluate the solutions your code produces, create a file called `output.json` that contains your code's output for each test case formatted as follows:
```json
[
  {
    "course": "MATH 1512",                  // The course that was evaluated - copied from the test data
    "completedCourses": ["MATH 1215"],      // The list of courses already completed - copied from the test data
    "isSatisfied": true,                    // The output your code produced from part 1.
    "coursesNeeded": [ ... ]                // The output your code produced from part 2.
  },
  ...
]
```
