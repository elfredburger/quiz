import requests
import json
import timeit
import sys

session = requests.Session()
pull=session.get('') #enter questions link
if pull.status_code!=200:
    print('Network error status code: '+ str(pull.status_code))
    sys.exit()
listOfQuestions=pull.json() 


numberOfQuestions=(len(listOfQuestions))
listOfMarkedQuestions=[]


class Quiz:
    def __init__(self,user):
        self.user=user
        self.correctAnswers=0
        self.report=[]
    def report_add(self,question,answer,correctAnswer,timeSpent):
        
        self.report.append({'question':question,'userAnswer':answer,'correctAnswer':correctAnswer,'timeSpent':timeSpent})
    def end_quiz(self):
        print(self.user+', your results are: \n')
        for questionResult in self.report:
            print('Question: '+questionResult.get('question')+'\n'+'You answered: '+ questionResult.get('userAnswer')+'\n'
                +'Correct answer: '+questionResult.get('correctAnswer')+'\nTime spent on this question '+str(round(questionResult.get('timeSpent')))+' seconds\n')
        print('\nCorrect answers: '+ str(self.correctAnswers)+'\n')
        print('Your score is: '+ str((self.correctAnswers/numberOfQuestions)*100)+' % !')
    
        


        


def check_answer(answer,question,quiz,timeSpent):
    
    answers= ['A','B','C','D','E','A,B','A,C','A,D','A,E',
              'B,A','B,C','B,D','B,E','C,A','C,B','C,D',
              'C,E','D,A','D,B','D,C','D,E','E,A','E,B',
              'E,C','E,D']
    if answer in answers:                                  
        if answer == question.get('CorrectAnswers'):
            quiz.correctAnswers+=1
        quiz.report_add(question.get('Question'),answer,question.get('CorrectAnswers'),timeSpent)

    if answer=='M' and question in listOfMarkedQuestions:
        answer=input('Incorrect answer, try again ').upper()
        check_answer(answer,question,quiz,timeSpent)

    if answer=='M' and question not in listOfMarkedQuestions:
        listOfMarkedQuestions.append(question)
        print('Question added for review')
                    
    
    if answer not in answers and answer!='M' :
        
        answer=input('Incorrect answer, try again').upper()
        check_answer(answer,question,quiz,timeSpent)
    

 

def ask_question(listOfQuestions,quiz):
        for question in listOfQuestions:
            print('\nQuestion : '+ question.get('Question')+'\n')

            print ('To mark question type "M"')
            if question.get('RequiredAnswers')==1:
                print('Choose one answer a,b,c,d'+'\n')
                print('A) '+question.get('AnswerA'))
                print('B) '+question.get('AnswerB'))
                print('C) '+question.get('AnswerC'))
                print('D) '+question.get('AnswerD'))

            else:
                print('choose two answers separated by coma')
                print('A) '+question.get('AnswerA'))
                print('B) '+question.get('AnswerB'))
                print('C) '+question.get('AnswerC'))
                print('D) '+question.get('AnswerD'))
                if question.get('AnswerE')!='':
                    print('E) '+question.get('AnswerE'))
            
            
            question_timer_start=timeit.default_timer()
            answer = input('your answer is: ').upper()
            question_timer_end=timeit.default_timer()
            check_answer(answer,question,quiz,question_timer_end-question_timer_start)
                
          
       


def run():
    
    name = input('Enter your name ')
    #lang=input('enter 'eng' for english version or 'de' for german version')
    start = timeit.default_timer()
    quiz=Quiz(name)
    

    ask_question(listOfQuestions,quiz)
    
    if len(listOfMarkedQuestions)>0:
        print('-------------------------You are now answering questions you marked for review-------------------------')
        ask_question(listOfMarkedQuestions,quiz)
    quiz.end_quiz()
    end=timeit.default_timer()
    print ('Time spent on the quiz is '+ str(round(end-start))+' seconds. Average time per question is '+str(round((end-start)/len(listOfQuestions))))
run()