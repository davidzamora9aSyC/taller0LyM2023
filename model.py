# Lista de comandos aceptados por el robot
commands = [
    'assingTo',
    'goto',
    'move',
    'turn',
    'face',
    'put',
    'pick',
    'moveToThe',
    'moveInDir',
    'jumpToThe',
    'jumpInDir',
    'nop',
]
#Lista de comandos para la instrucción Look
lookCommands = {
    'N' : True,
    'E' : True,
    'W' : True,
    'S' : True
}
#Lista de condiciones

conditions=[
    'facing',
    'canPut',
    'canPick',
    'canMoveDir',
    'canJumpInDir',
    'canMoveToThe',
    'canJumpToThe',
    'not'
]
#Lista de comandos para la instrucción Check
checkCommands = {
    'C' : True,
    'B' : True
}

#Variables definidas durante la ejecución del programa
definedVariables = {

}

#Caracteres especiales
specialChars = {
    "(" : 0,
    ")" : 0,
    "[" : 0,
    "]" : 0,
    ":" : 0
}



def wordInCommands(word):
    """Verifica si una instrucción se encuentra dentro de la lista de comandos."""
    if word in commands.keys():
        return True
    else:
        return False


def verifyProgram():
    verificado=True
    """Verifica que las instrucciones ingresadas sean correctas"""
    programString = "" #String que contiene todas las instrucciones leídas en el archivo de texto
    filename = "programaPrueba.txt"
    with open(filename,"r") as file: #Lectura el archivo de texto
        for line in file:
            #line = line.strip('\n') + ' '
            line = line.lstrip()

        
            programString += line #Se añade cada línea leída al String que contiene todo

    programList = programString.split('\n')
    i=0
    while i < len(programList):

        if programList[0] != 'ROBOT_R' and (i==0):
            verificado=False
            
        elif programList[1][0:4]!= "VARS" and (i==1):
            verificado=False 
            
        elif programList[1].strip("")

        i+=1

    print(programString)
    if verificado == True:
        return "Correcto"

    return 'ESCRIBA BIEN'
   

print(verifyProgram())