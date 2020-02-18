# METCAL Emulator Engine
# By Micah Hurd
programName = "METCAL Emulator Engine"
version = 0.1

import os

def readConfigFile(filename, searchTag, sFunc=""):
    searchTag = searchTag.lower()
    # print("Search Tag: ",searchTag)

    # Open the file
    with open(filename, "r") as filestream:
        # Loop through each line in the file

        for line in filestream:

            if line[0] != "#":

                currentLine = line
                equalIndex = currentLine.find('=')
                if equalIndex != -1:

                    tempLength = len(currentLine)
                    # print("{} {}".format(equalIndex,tempLength))
                    tempIndex = equalIndex
                    configTag = currentLine[0:(equalIndex)]
                    configTag = configTag.lower()
                    configTag = configTag.strip()
                    # print(configTag)

                    configField = currentLine[(equalIndex + 1):]
                    configField = configField.strip()
                    # print(configField)

                    # print("{} {}".format(configTag,searchTag))
                    if configTag == searchTag:

                        # Split each line into separated elements based upon comma delimiter
                        # configField = configField.split(",")

                        # Remove the newline symbol from the list, if present
                        lineLength = len(configField)
                        lastElement = lineLength - 1
                        if configField[lastElement] == "\n":
                            configField.remove("\n")
                        # Remove the final comma in the list, if present
                        lineLength = len(configField)
                        lastElement = lineLength - 1

                        if configField[lastElement] == ",":
                            configField = configField[0:lastElement]

                        lineLength = len(configField)
                        lastElement = lineLength - 1

                        # Apply string manipulation functions, if requested (optional argument)
                        if sFunc != "":
                            sFunc = sFunc.lower()

                            if sFunc == "listout":
                                configField = configField.split(",")

                            if sFunc == "stringout":
                                configField = configField.strip("\"")

                        filestream.close()
                        return configField

        filestream.close()
        return "Searched term could not be found"

def readMcFile(filename):
    # Place contents of procedure files into variable
    f = open(filename, 'r')
    x = f.readlines()
    f.close()
    return x

def getCommandList(filename):
    #Place contents of file into variable
    f = open(filename, 'r')
    x = f.readlines()
    f.close()

    # Strip newline characters from the file
    for index, i in enumerate(x):
        item = i
        item = item.strip()
        x[index] = item
    return x

def findCommandStart(instructionList):

    for index, line in enumerate(instructionList):

        # Clean up all the whitespace
        line = ' '.join(line.split())
        # Split the line into a list
        line = line.split(" ")

        firstItem = line[0]

        try:
            firstItem = firstItem.lower()
        except:
            firstItem = ""

        if firstItem == "step":
            return index

    return -1

def parseInstruction(instructionLine):

    # set ignore line flag to true by default
    ignoreLine = True

    # Clean up all the whitespace
    line = ' '.join(instructionLine.split())
    # Split the line into a list
    line = line.split(" ")
    # print(line)

    if line[0] != "":
        ignoreLine = False

    lineItemQuantity = len(line)

    firstItem = line[0]
    try:
        firstCharacter = firstItem[0]
    except:
        firstCharacter = "#"

    if firstCharacter[0] == "#":
        ignoreLine = True

    if lineItemQuantity < 2:
        ignoreLine = True

    if ignoreLine == False:
        # print(line)
        command = line[1]
        command = command.lower()
        return command
    else:
        return -1

def extractProcedureTitle(instructionLine):
    # Clean up all the whitespace
    line = ' '.join(instructionLine.split())
    # Split the line into a list
    line = line.split(" ")
    # print(line)

    length = len(line)

    firstElement = line[0]
    try:
        firstElement = firstElement.lower()
    except:
        firstElement = "-1"

    procedureTitle = ""
    if firstElement == "instrument:":

        for i in range(1,length):
            if procedureTitle == "":
                procedureTitle  = procedureTitle + line[i]
            else:
                procedureTitle = procedureTitle + " " + line[i]
    else:
        procedureTitle = "-1"

    return procedureTitle

def buildProcDir(directory):
    import os

    # Create a list of all .mc files in the specified directory
    fileList = []
    for file in os.listdir(directory):
        if file.endswith(".mc"):
            fileList.append((os.path.join(directory, file)))


    procedureTitleList = []
    procedureTitleFilename = []
    # Open each file and extract the title(s) from the procedure
    for index, filePath in enumerate(fileList):
        fileContents = readMcFile(filePath)
        #print(contents)

        for index, i in enumerate(fileContents):
            title = extractProcedureTitle(i)
            #print(command)
            if title != "-1":
                procedureTitleList.append(title)
                procedureTitleFilename.append(filePath)


    # print(procedureTitleList)
    # print(procedureTitleFilename)

    file1 = open("Proc.dir", "w")
    for index, title in enumerate(procedureTitleList):
        procedureNumber = index + 1
        filePath = procedureTitleFilename[index]
        toFile = "{},{},{}\n".format(procedureNumber, title, filePath)
        file1.write(toFile)
    file1.close()

def askCommand(instructionLine):

    # Clean up all the whitespace
    instructionList = ' '.join(instructionLine.split())
    # Split the line into a list
    instructionList = instructionList.split(" ")

    # Find the number of elements in the instruction line
    length = len(instructionList)
    # A valid command must contain at least three elements
    if length < 3:
        return -1

    # Calculate qty of ask parameters
    qtyParameters = length - 2

    # Determine if the command is setting ask parameters to on or off
    askFlag = instructionList[1]
    askFlag = askFlag.lower()
    if askFlag == "ask+":
        set = "+"
    else:
        set = "-"

    # Loop through the elements in the instruction line list, starting right after the ask element
    # Sets the ask flag values to on or off as specified
    for i in range(2,length):

        # Obtain the index'd valued from the instruction list
        flag = instructionList[i]
        # set it to lower case character
        flag = flag.lower()
        # Index the current flag in the askFlagListID
        flagIndex = askFlagListID.index(flag)
        # Set the appropriate flag in the flag values variable to the currect value (on or off)
        if set == "+":
            askFlagListValues[flagIndex] = True
        else:
            askFlagListValues[flagIndex] = False

    return 1




# Program setup variabls
cwd = os.getcwd()
filename = cwd + "/" + "test.mc"
commandListFile = cwd + "/" + "supportedCommands.txt"
configFile = "mcemu.cfg"

# Import configuration file values
procDirectory = readConfigFile(configFile, "procDirectory", "stringout")
print(procDirectory)

# Scan procedure folder and create a procedure list
buildProcDir(procDirectory)

# Create METCAL environment variables
askFlagListID =     ['a', 'b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z']
askFlagListValues = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
procedureLine = 0
endFlag = False

# Procedure parameter lists
# These lists facilitate calling and returning from subroutines by storing the parameters of each routie
# to a list. In this way, when a subprocedure ends, the primary procedure may be returned to
procedureLineList = []
activeProcedureList = []
procedureLineQtyList = []
instructionListList = []

commandList = getCommandList(commandListFile)
currentActiveProcedureName = "Test METCAL Emu Procedure"
activeProcedureList.append(currentActiveProcedureName)

# Read the METCAL procedure file into a variable
instructionList = readMcFile(filename)
instructionListList.append(instructionList)

procedureLineQty = len(instructionList)
procedureLineQtyList.append(procedureLineQty)

instructionStartLine = findCommandStart(instructionList) + 1
procedureLineList.append(instructionStartLine)

# Main program loop
procedureLine = instructionStartLine
while endFlag == False:
    if procedureLine > 100:
        endFlag = True

    # This code facilitates returning from called subs; allows infinite nested subs
    if procedureLine == procedureLineQty:
        tempListLength = len(activeProcedureList)
        if tempListLength > 1:
            try:
                tempIndex = activeProcedureList.index(currentActiveProcedureName)
                returnIndex = tempIndex - 1

                # Delete the current subProcedure information from each procedure parameter list
                del activeProcedureList[tempIndex]
                del activeProcedureList[tempIndex]
                del procedureLineQtyList[tempIndex]
                del procedureLineList[tempIndex]

                # Load the return sub procedure parameters from the each procedure parameter list
                currentActiveProcedureName = activeProcedureList[returnIndex]
                instructionList = activeProcedureList[returnIndex].copy()
                procedureLineQty = procedureLineQtyList[returnIndex]
                procedureLine = procedureLineList[returnIndex]
            except:
                endFlag = True

        print()
    else:
        currentInstruction = instructionList[procedureLine]
        print(currentInstruction)

        command = parseInstruction(currentInstruction)
        if command != -1:
            print(command)

    tempIndex = activeProcedureList.index(currentActiveProcedureName)
    procedureLine += 1
    procedureLineList[tempIndex] = procedureLine



# To-Do List:
## Update currentActiveProcedureName to automatically populate based on the current running procedure