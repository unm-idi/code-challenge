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


    switch (targetPrereqs['type']) {
        case 'course':



        case 'and':
            return targetPrereqs['operands'].reduce((acc, curr) => acc && prereqsSatisfied(completedCourses, curr), true)

        case 'or':
            // begin false, then if any operands are true, return true
            return targetPrereqs['operands'].reduce((acc, curr) => acc || prereqsSatisfied(completedCourses, curr), false)
    }
}





const testTarget = "ECON 300"
const testCompleted = ["ECON 2110", "ECON 2120", "MATH 1512", "MATH 1430"]

const analysis = (target, completed) => {
    try {
        const targetPrereqs = getPrereqs(target)

        const result = prereqsSatisfied(completed, targetPrereqs)

        console.log(result)

    } catch (e) {
        console.error(e)
    }

}

analysis(testTarget, testCompleted)

