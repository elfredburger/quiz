import requests
import json
import timeit


listOfQuestions=requests.get('https://7xzprnkulf.execute-api.eu-west-1.amazonaws.com/Prod/questions/all').json()
numberOfQuestions=(len(listOfQuestions))
listOfMarkedQuestions=[]


class Quiz:
    def __init__(self,user,lang):
        self.user=user
        self.lang=lang
        self.correctAnswers=0
        self.report=[]
    def reportAdd(self,question,answer,correctAnswer,timeSpent):
        
        self.report.append({'question':question,'userAnswer':answer,'correctAnswer':correctAnswer,'timeSpent':timeSpent})
    def endQuiz(self):
        
        for i in self.report:
            print("question: "+i.get("question")+"\n"+"you answered: "+ i.get("userAnswer")+"\n"+"correct answer: "+i.get('correctAnswer')+"\ntime spent on this question "+str(round(i.get('timeSpent')))+' seconds\n')
        print('\ncorrect answers: '+ str(self.correctAnswers)+'\n')
        print('your score is: '+ str((self.correctAnswers/numberOfQuestions)*100)+' % !')
    
        


        


def checkAnswer(answer,question,quiz,timeSpent):
    
    answers= ['A','B','C','D','E','A,B','A,C','A,D','A,E', 'B,A','B,C','B,D','B,E','C,A','C,B','C,D','C,E','D,A','D,B','D,C','D,E','E,A','E,B','E,C','E,D']
    if answer in answers:                                  
        if answer == question.get('CorrectAnswers'):
            quiz.correctAnswers+=1
        quiz.reportAdd(question.get('Question'),answer,question.get('CorrectAnswers'),timeSpent)

    if answer=='M' and question in listOfMarkedQuestions:
        answer=input('incorrect answer, try again').upper()
        checkAnswer(answer,question,quiz,timeSpent)

    if answer=='M' and question not in listOfMarkedQuestions:
        listOfMarkedQuestions.append(question)
        print('question added for review')
                    
    
    if answer not in answers and answer!='M' :
        
        answer=input('incorrect answer, try again').upper()
        checkAnswer(answer,question,quiz,timeSpent)
    

 

def askQuestion(listOfQuestions,a):
        for i in listOfQuestions:
            print("\nquestion : "+ i.get("Question")+'\n')

            print ('to mark question type "M"')
            if i.get("RequiredAnswers")==1:
                print('choose one answer a,b,c,d'+'\n')
                print("A) "+i.get('AnswerA'))
                print("B) "+i.get('AnswerB'))
                print("C) "+i.get('AnswerC'))
                print("D) "+i.get('AnswerD'))

            else:
                print('choose two answers separated by coma')
                print("A) "+i.get('AnswerA'))
                print("B) "+i.get('AnswerB'))
                print("C) "+i.get('AnswerC'))
                print("D) "+i.get('AnswerD'))
                if i.get('AnswerE')!='':
                    print("E) "+i.get('AnswerE'))
            
            
            question_timer_start=timeit.default_timer()
            answer = input('your answer is: ').upper()
            question_timer_end=timeit.default_timer()
            checkAnswer(answer,i,a,question_timer_end-question_timer_start)
                
        a.endQuiz()   
       


def run():
    
    name = input('enter your name')
    #lang=input('enter "eng" for english version or "de" for german version')
    start = timeit.default_timer()
    a=Quiz(name,'eng')
    

    askQuestion(listOfQuestions,a)
    print('-------------------------You are now answering questions you marked for review-------------------------')
    askQuestion(listOfMarkedQuestions,a)

    end=timeit.default_timer()
    print ('time spent on the quiz is '+ str(round(end-start))+' seconds. Average time per question is '+str(round((end-start)/len(listOfQuestions))))
run()