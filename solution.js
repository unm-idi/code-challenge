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

// recursive helper function to determine whether prereqs have been met, inputs are:
// completedCourses: the courses an individual has already completed
const prereqsSatisfied = (completedCourses, targetPrereqs) => {

    if(!targetPrereqs) return true

    const type = targetPrereqs['type']

    // Base case:  if we reach the 'bottom' level of the prereqs, 
    // check if that class is in our taken courses array
    if (type === 'course') {
        return completedCourses.includes(targetPrereqs['code'])

    // Otherwise, use the appropriate logic on the next level
    } else {
        const boolops = {
            'and': (a, b) => a && b,
            'or': (a, b) => a || b
        }

        // if we are using the "and" operator, then we begin true 
        // then if any operands are false, return false
        // if we are using the "or" operator, we do the opposite
        const start = (type === "and")

        return targetPrereqs['operands'].reduce((acc, curr) =>
            boolops[type](acc, prereqsSatisfied(completedCourses, curr)),
            start)
    }
}





const analysis = (target, completed) => {
    try {
        const targetPrereqs = getPrereqs(target)

        const result = prereqsSatisfied(completed, targetPrereqs)

        // console.log(result)
        return result

    } catch (e) {
        console.error(e)
    }

}


const testTarget = "ECON 300"
const testCompleted = ["ECON 2110", "ECON 2120", "MATH 1512", "MATH 1430"]

for(let i = 0; i < tests.length; i++){
    tests[i]['isSatisfied'] = analysis(tests[i]['course'], tests[i]['completedCourses'])
}

fs.writeFile(
    "output.json",
    JSON.stringify(tests),
    err => {
        if (err) throw err
        console.log("Done writing")
    }
)
console.log(tests)
// analysis(testTarget, testCompleted)

