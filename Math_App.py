import random

import operator
operations = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.div}

import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "tri1plepho9tonsin5gle", database = "math_app")

mycursor = mydb.cursor()

while True:
    try:
        number_of_questions = int(input("How many questions would you like to do? Number: "))
        break
    except ValueError:
        print("Sorry please enter an integer")

class Operation:

    history = []
    score = 0

    def __init__(self, n1, n2, func_symbol, oper_func):
        self.n1 = n1
        self.n2 = n2
        self.func_symbol = func_symbol
        self.oper_func = oper_func

    def function(self):
        self.result = self.oper_func(self.n1, self.n2)
        python_question = str(self.n1) + self.func_symbol + str(self.n2) + " = "
        user_answer = input(python_question)
        while True:
            if str(user_answer) == str(self.result):
                print("You are correct!")
                python_equation = str(python_question) + str(user_answer) + "    ✓"
                complete = (python_question, python_equation)
                sentence = "INSERT INTO history (question, equation) VALUES (%s, %s)"
                mycursor.execute(sentence, complete)
                mydb.commit()
                Operation.score += 1
                break
            else:
                print("Sorry, your answer is wrong, please try again:")
                user_answer = input(str(self.n1) + self.func_symbol + str(self.n2) + " = ")
                python_equation = str(python_question) + str(user_answer) + "    ✕"
                complete = (python_question, python_equation)
                sentence = "INSERT INTO history (question, equation) VALUES (%s, %s)"
                mycursor.execute(sentence, complete)
                mydb.commit()
                Operation.score -= 1

for element in range(number_of_questions):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    add = Operation(num1, num2, " + ", operations["+"])
    subtract = Operation(num1, num2, " - ", operations["-"])
    multiply = Operation(num1, num2, " * ", operations["*"])
    divide = Operation(num1, num2, " ÷ ", operations["/"])

    operation_list = [add.function, subtract.function, multiply.function, divide.function]
    random.choice(operation_list)()

for element in Operation.history:
    print(element)

mycursor.execute("SELECT * FROM history")
for i in mycursor:
    print(i)

print()
print(str(Operation.score) + " / " + str(number_of_questions))