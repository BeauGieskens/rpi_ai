import config
import os
import re

def saySomething(text):
    #os.system("espeak -ven+f3 -k5 -s150 '" + txt + "'")
    print "speaking..."
    print text
    sentences = ""
    text = re.sub('[!;]','.',text)
    for sentence in text.split('.'):
        if len(sentence) > 0:
            os.system("espeak '" + sentence + "' -v en/en-us")

