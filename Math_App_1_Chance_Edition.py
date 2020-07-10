import random
import datetime

import operator
operations = {" + ": operator.add, " - ": operator.sub, " * ": operator.mul, " ÷ ": operator.div}

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
        global wrong_question_id
        self.result = self.oper_func(self.n1, self.n2)
        python_question = str(self.n1) + self.func_symbol + str(self.n2) + " = "
        user_answer = input(python_question)
        if str(user_answer) == str(self.result):
            print("You are correct!")
            python_equation = str(python_question) + str(user_answer) + "    ✓"
            complete_insert_into_history = (python_question, python_equation, 1, datetime.date.today(), datetime.datetime.now().strftime("%H:%M:%S"))
            insert_into_history = "INSERT INTO history (question, equation, is_answer_correct, date_completed, time_completed) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(insert_into_history, complete_insert_into_history)
            mydb.commit()
            Operation.score += 1
        else:
            print("Sorry, your answer is wrong")
            python_equation = str(python_question) + str(user_answer) + "    ✕"
            complete_insert_into_history = (python_question, python_equation, 0, datetime.date.today(), datetime.datetime.now().strftime("%H:%M:%S"))
            insert_into_history = "INSERT INTO history (question, equation, is_answer_correct, date_completed, time_completed) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(insert_into_history, complete_insert_into_history)
            # mycursor.execute("INSERT INTO wrong_questions SELECT question_id FROM history")
            mycursor.execute("SELECT MAX(question_id) FROM history")
            for wrong_question_id_tuple in mycursor:
                for individual_wrong_question_id in wrong_question_id_tuple:
                    wrong_question_id = individual_wrong_question_id
            complete_insert_into_wrong_questions = (wrong_question_id, python_question, self.n1, self.func_symbol, self.n2)
            insert_into_wrong_questions = "INSERT INTO wrong_questions (question_id, question, number_1, operator, number_2) VALUES (%s, %s, %s, %s, %s)"
            # mycursor.execute("INSERT INTO wrong_questions (question_id) SELECT MAX(question_id) FROM history")
            mycursor.execute(insert_into_wrong_questions, complete_insert_into_wrong_questions)
            mydb.commit()

for element in range(number_of_questions):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    add = Operation(num1, num2, " + ", operations[" + "])
    subtract = Operation(num1, num2, " - ", operations[" - "])
    multiply = Operation(num1, num2, " * ", operations[" * "])
    divide = Operation(num1, num2, " ÷ ", operations[" ÷ "])

    operation_list = [add.function, subtract.function, multiply.function, divide.function]
    random.choice(operation_list)()

for element in Operation.history:
    print(element)

mycursor.execute("SELECT * FROM history")
for i in mycursor:
    print(i)

print()
score_frame = "{} / {}"
overall_score = score_frame.format(Operation.score, number_of_questions)

print(overall_score)

mycursor.execute("SELECT COUNT(*) FROM wrong_questions")

global amount_of_rows
for total_counts in mycursor:
    for individual_total_count in total_counts:
        amount_of_rows = individual_total_count

if amount_of_rows != 0:
    redo = input("Would you like to redo the wrong questions? (Yes/No): ")

    while True:
        if redo == "Yes" or redo == "No":
            break
        else:

            redo = input("Please answer Yes or No: ")

    if redo == "No":
        quit()
else:
    quit()

list_of_wrong_questions = []

mycursor.execute("SELECT question FROM wrong_questions")
for questions in mycursor:
    for individual_question in questions:
        list_of_wrong_questions.append(individual_question)

print()
print("Wrong Questions: ")
for each_question in list_of_wrong_questions:
    print(each_question)

list_of_wrong_question_ids = []

mycursor.execute("SELECT question_id FROM wrong_questions")
for question_ids in mycursor:
    for individual_number_1 in question_ids:
        list_of_wrong_question_ids.append(individual_number_1)

print()
print("Question IDs: " + str(list_of_wrong_question_ids))

list_of_number_1s = []

mycursor.execute("SELECT number_1 FROM wrong_questions")
for number_1s in mycursor:
    for individual_number_1 in number_1s:
        list_of_number_1s.append(individual_number_1)

print()
print("Number 1s: " + str(list_of_number_1s))

list_of_operators = []

mycursor.execute("SELECT operator FROM wrong_questions")
for operators in mycursor:
    for individual_operator in operators:
        list_of_operators.append(individual_operator)

print()
print("Operators: " + str(list_of_operators))

list_of_number_2s = []

mycursor.execute("SELECT number_2 FROM wrong_questions")
for number_2s in mycursor:
    for individual_number_2 in number_2s:
        list_of_number_2s.append(individual_number_2)

print()
print("Number 2s: " + str(list_of_number_2s))
print()

number_of_wrong_questions = len(list_of_number_1s)
question_number = 0

def redo_wrong_questions(question_number):
    print("Beginning your retrial: ")
    redo_result = operations[list_of_operators[question_number]](list_of_number_1s[question_number], list_of_number_2s[question_number])
    python_redo_question = str(list_of_number_1s[question_number]) + str(list_of_operators[question_number]) + str(list_of_number_2s[question_number]) + " = "
    user_redo_answer = input(python_redo_question)
    if str(user_redo_answer) == str(redo_result):
        print("You are correct!")
        complete_delete_wrong_question_from_history = list_of_wrong_question_ids[question_number]
        delete_wrong_question_from_history = "DELETE FROM wrong_questions WHERE (question_id = %s)"
        mycursor.execute(delete_wrong_question_from_history, (complete_delete_wrong_question_from_history,))
        mydb.commit()
        # complete_delete_wrong_question_from_wrong_questions = list_of_question_ids[question_number]
        # delete_wrong_question_from_wrong_questions = "DELETE FROM wrong_questions WHERE (question_id = %s)"
        # mycursor.execute(delete_wrong_question_from_wrong_questions, (complete_delete_wrong_question_from_wrong_questions,))
        # mydb.commit()
        # DELETE FROM `math_app`. `history` WHERE(`question_id` = '181')
    else:
        print("Sorry, your answer is wrong")

while question_number < number_of_wrong_questions:
    redo_wrong_questions(question_number)
    question_number += 1