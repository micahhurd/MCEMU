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




procedureLine = 0

cwd = os.getcwd()
filename = cwd + "/" + "test.mc"
commandListFile = cwd + "/" + "supportedCommands.txt"


instructionList = readMcFile(filename)
commandList = getCommandList(commandListFile)
end = False

instructionStartLine = findCommandStart(instructionList) + 1

procedureLine = instructionStartLine
while end == False:
    if procedureLine > 100:
        end = True

    instructionLine = instructionList[procedureLine]

    command = parseInstruction(instructionLine)
    if command != -1:
        print(command)



    procedureLine += 1
