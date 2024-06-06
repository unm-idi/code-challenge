require 'json'

jsonFile = File.open('./data/tests.json')
prereqsFile = File.open('./data/prerequisites.json')
parsedFileData = JSON.load jsonFile
$parsedPrereqsData = JSON.load prereqsFile

$firstArray = []
$lastArray = []

$data = ""

def sortCase(prereqs)

    prereqs["operands"].each do |process|

        if process["type"] == "course"
            $firstArray.push(process["code"])
        else
            process["operands"].each do |insert|
                $lastArray.push(insert["code"])
            end
        end
    end

end

def objectiveProcessor(course,completed)

    objOne = ""
    objTwo = []
    $firstArray = []
    $lastArray = []

    if $parsedPrereqsData[course] == "" || $parsedPrereqsData[course] == nil

        objOne = "true"
        objTwo = []
    elsif $parsedPrereqsData[course]["type"] == "course"

        if completed.include?($parsedPrereqsData[course]["code"])
            objOne = "true"
            objTwo = []
        else
            objOne = "false"
            objTwo = ["#{$parsedPrereqsData[course]["code"]}"]
        end
    elsif $parsedPrereqsData[course]["type"] == "or"

        sortCase($parsedPrereqsData[course])
        
        if $firstArray & completed != nil
            objOne = "true"
            objTwo = []
        elsif ($lastArray - completed).empty?
            objOne = "true"
            objTwo = []
        else
            objOne = "false"
            if ($lastArray - completed).length < fistArray.length
                objTwo = $lastArray - completed
            else
                objTwo = $firstArray
            end
        end

    elsif $parsedPrereqsData[course]["type"] == "and"

        sortCase($parsedPrereqsData[course])
        
        if $lastArray & completed != nil && ($firstArray - completed).empty?
            objOne = "true"
            objTwo = []
        else
            objOne = "false"
            objTwo = ($firstArray + $lastArray) - completed
        end

    end
    return $data = "\n\t{\t\n\t\"course\": \"#{course}\",\n\t\"completedCourses\": #{completed},\n\t\"isSatisfied\": #{objOne},\n\t\"coursesNeeded\": #{objTwo}\n\t}"
end

File.write("output.json", "[")

parsedFileData.each do |look|

    objectiveProcessor(look["course"],look["completedCourses"])

    unless look == parsedFileData[10]
        File.write("output.json", "#{$data},", mode: "a")
    else
        File.write("output.json", "#{$data}", mode: "a")
    end
end

File.write("output.json", "\n]", mode: "a")