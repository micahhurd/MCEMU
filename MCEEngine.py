# METCAL Emulator Engine
# By Micah Hurd
programName = "METCAL Emulator Engine"
version = 0.1

import os



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
        return command
    else:
        return -1

def askCommand(instructionLine):
    # print(instructionLine)

    # Clean up all the whitespace
    instructionList = ' '.join(instructionLine.split())
    # Split the line into a list
    instructionList = instructionList.split(" ")
    # print(line)

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


# Metcal environment setup variabls
askFlagListID =     ['a', 'b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z']
askFlagListValues = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
procedureLine = 0
instructionList = readMcFile(filename)
commandList = getCommandList(commandListFile)
end = False

instructionStartLine = findCommandStart(instructionList) + 1


# Main program loop
procedureLine = instructionStartLine
while end == False:
    if procedureLine > 100:
        end = True

    instructionLine = instructionList[procedureLine]
    print(instructionLine)

    command = parseInstruction(instructionLine)
    if command != -1:
        print(command)



    procedureLine += 1
