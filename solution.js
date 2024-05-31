const fs = require("fs")

const catalog = require("./data/prerequisites.json")
const tests = require("./data/tests.json")

// helper function to get prereqs for a given target course
const getPrereqs = (target) => {
    if (!Object.keys(catalog).includes(target)) {
        throw new Error('Target course not found')
    }
    return catalog[target]
}

// recursive function to find the shortest list of prereqs needed in order to take a course
const findFewestAdditionalCourses = (targetPrereqs, completed) => {
    
    // if there are no prereqs for a given course, return an empty array (no courses are needed)
    if(!targetPrereqs) return []

    const type = targetPrereqs['type']

    if(type === 'course') {
        let subProblem = targetPrereqs['code']

        // if the prerequisite course has already been completed, no additional courses are needed
        if(completed.includes(subProblem)) return []

        let subPrereqs = getPrereqs(subProblem)

        // otherwise, find the shortest list of courses needed to take the current prereq
        let subSolution = findFewestAdditionalCourses(subPrereqs, completed)

        // add the current course to the running total, then return
        subSolution.push(subProblem)

        return subSolution
    }


    let operands = targetPrereqs['operands']
    
    // if the type is OR, then find the shortest subpath of each option
    if(type === 'or') {
        let minLength = Infinity
        let bestSubSolution

        for(let i = 0; i < operands.length; i++){

            let subPrereqs = operands[i]
            let subSolution = findFewestAdditionalCourses(subPrereqs, completed)

            // update the best sub solution only if it has a shorter length than one previously found
            if(subSolution.length < minLength){
                minLength = subSolution.length
                bestSubSolution = subSolution.slice()
            }

        }

        return bestSubSolution
    }

    // if the type is AND, then add all missing courses and all of shortest paths to them
    if(type === 'and') {
        let totalSubSolution = []
        for(let i = 0; i < operands.length; i++){

            let subPrereqs = operands[i]
            let subSolution = findFewestAdditionalCourses(subPrereqs, completed)

            for(let course of subSolution){
                // do not add courses that have already been added
                if(totalSubSolution.includes(course)) continue
                totalSubSolution.push(course)
            }
        }

        return totalSubSolution
    }

}

// helper function that checks to make sure data being passed in is good before calculating shortest path to target
const solve = (target, completed) => {
    try {
        const targetPrereqs = getPrereqs(target)

        const result = findFewestAdditionalCourses( targetPrereqs, completed)

        return result

    } catch (e) {
        console.error(e)
    }

}

// Run tests
for(let i = 0; i < tests.length; i++){
    let fewestAdditionalCoursesNeeded = solve(tests[i]['course'], tests[i]['completedCourses'])
    
    // if the shortest path to the target course is empty, that means the prereqs have been satisfied
    tests[i]['isSatisfied'] = (fewestAdditionalCoursesNeeded.length === 0)

    // return shortest path to the target course
    tests[i]['coursesNeeded'] = fewestAdditionalCoursesNeeded
}

// Write output.json file
fs.writeFile(
    "output.json",
    JSON.stringify(tests),
    err => {
        if (err) throw err
        console.log("Done writing")
    }
)