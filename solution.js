const fs = require("fs")

const catalog = require("./data/prerequisites.json")
const tests = require("./data/tests.json")

// helper function to get prereqs for a given target course
const getPrereqs = (target) => {

}

const prereqsSatisfied = (takenCourses, targetPrereqs) => {

    switch (targetPrereqs['type']){
        // Base case:  if we reach the 'bottom' level of the prereqs, 
        // check if that class is in our taken courses array
        case 'course':
            return takenCourses.includes(targetPrereqs['code'])

        // Otherwise, use the appropriate logic on the next level
        case 'and':
            // begin true and then if any operands are false, return false
            return targetPrereqs['operands'].reduce((acc, curr) => acc && prereqsSatisfied(takenCourses, curr), true)
        
        case 'or':
            // begin false, then if any operands are true, return true
            return targetPrereqs['operands'].reduce((acc, curr) => acc || prereqsSatisfied(takenCourses, curr), false)
    }
}

// const i = 1
// const testTarget = tests[i]['course']
// const testTaken = tests[i]['completedCourses']
const testTarget = "ECON 300"
const testTaken = ["ECON 2110", "ECON 2120", "MATH 1512"]
const targetPrereqs = catalog[testTarget]

console.log(prereqsSatisfied(testTaken, targetPrereqs))

