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


const findFewestAdditionalCourses = (targetPrereqs, completed, memo) => {
    
    if(!targetPrereqs) return []

    const type = targetPrereqs['type']

    if(type === 'course') {
        let subProblem = targetPrereqs['code']

        if(completed.includes(subProblem)) 
            return []

        let subPrereqs = getPrereqs(subProblem)

        let subSolution = findFewestAdditionalCourses(subPrereqs, completed, memo)
        subSolution.push(subProblem)

        return subSolution
    }

    let operands = targetPrereqs['operands']

    if(type === 'or') {
        let minLength = Infinity
        let bestSubSolution

        for(let i = 0; i < operands.length; i++){

            let subPrereqs = operands[i]
            let subSolution = findFewestAdditionalCourses(subPrereqs, completed, memo)

            if(subSolution.length < minLength){
                minLength = subSolution.length
                bestSubSolution = subSolution.slice()
            }

        }

        return bestSubSolution
    }

    if(type === 'and') {
        let totalSubSolution = []
        for(let i = 0; i < operands.length; i++){

            let subPrereqs = operands[i]
            let subSolution = findFewestAdditionalCourses(subPrereqs, completed, memo)

            for(let course of subSolution){
                if(totalSubSolution.includes(course)) continue
                totalSubSolution.push(course)
            }
        }

        return totalSubSolution
    }

}


const solve = (target, completed) => {
    try {
        const targetPrereqs = getPrereqs(target)

        const result = findFewestAdditionalCourses( targetPrereqs, completed, {})

        return result

    } catch (e) {
        console.error(e)
    }

}

for(let i = 0; i < tests.length; i++){
    let fewestAdditionalCoursesNeeded = solve(tests[i]['course'], tests[i]['completedCourses'])
    tests[i]['isSatisfied'] = (fewestAdditionalCoursesNeeded.length === 0)
    tests[i]['coursesNeeded'] = fewestAdditionalCoursesNeeded
}


fs.writeFile(
    "output.json",
    JSON.stringify(tests),
    err => {
        if (err) throw err
        console.log("Done writing")
    }
)

