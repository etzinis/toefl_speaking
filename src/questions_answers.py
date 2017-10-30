import os, sys, time, signal
import Tkinter as tk
import tkFont
import random


background_color = "dodgerblue"
class Timer(tk.Tk):
    def __init__(self, textos, qora):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="TOEFL Questions - thymios", bg="blue")
        self.title("TOEFL Questions - thymios")
        self.configure(bg = background_color)
        self.geometry('1200x1200+600+600')
        self.label.pack()
        self.remaining = 0
        self.textos = textos
        if (qora == "q"):
            self.countdownq(20)
        else:
            self.countdowna(45)


    def countdownq(self, remaining = None):

        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="Now Start Speaking")
            time.sleep(1)
            self.destroy()
            return
        else:            
            self.label.configure(text=self.textos+"\nPrepare your answer:"+" %d" % self.remaining, font=("Helvetica 16 bold"), fg="white", bg = background_color)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdownq)
            

    def countdowna(self, remaining = None):

        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="Time's up! Ready for the next question")
            time.sleep(1)
            self.destroy()
            return
        else:
            self.label.configure(text=self.textos+"\n Recording: %d" % self.remaining, font=("Helvetica 16 bold"), fg="white", bg = background_color)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdowna)



def make_one_list(lines, q):
    for i in range(len(lines)):
        num = lines[i].split("\n")[0].split(".")[0]
        try:
            int(num)
            q[num] = ""
        except Exception, e:
            continue


        j = i+1
        while (1):
            try:
                int(lines[j].split("\n")[0].split(".")[0])
            except Exception, e:
                if (j >= len(lines)):
                    break
                q[num] += " " + lines[j].split("\n")[0]
                j += 1
                continue

            break


    return q

def make_the_questions_list(lines1, lines2, q1, q2):
    q1 = make_one_list(lines1,q1)
    q2 = make_one_list(lines2,q2)
    return (q1,q2)

def do_one_question(num,q,qs):
    print "NOW DOING " + num
    textos = q[num]
    t = textos.split(".")
    textos = "\n".join(t)
    t = textos.split(",")
    textos = "\n".join(t)
    t = textos.split("?")
    textos = "\n".join(t)
    timer = Timer(textos,"q")
    timer.mainloop()
    pid = os.fork()
    if (pid == 0):
        os.system("arecord -d 46 "+ "../" + qs + "/" + num + ".wav")
        exit(0)
    else:
        timer = Timer(textos,"a")
        timer.mainloop()
        os.kill(pid,signal.SIGINT)
        os.system("killall arecord")
    return num
    

def main():
    q1 = {}
    q2 = {}
    f1 = open("possible_questions_q1","r")
    f2 = open("possible_questions_q2","r")
   
    (q1,q2)=make_the_questions_list(f1.readlines(),f2.readlines(),q1,q2)
    f1.close()
    f2.close()

    # check for the questions which were checked from previous examination
    exlist1 = os.listdir("../q1")
    exlist2 = os.listdir("../q2")
    
    for el in exlist1:
        try:
            del q1[el.split(".wav")[0]]
        except Exception, e:
            continue

    for el in exlist2:
        try:
            del q2[int(el.split(".wav")[0])]
        except Exception, e:
            continue


    #Ready to proceed in questions 
    q = q1
    qs = ""
    while (1):
     
        inp = input("Which question do you prefer?\n")
        inp = str(inp)
        print inp
        if (inp=="1"):
            q = q1
            qs = "q1"
            break
        elif (inp == "2"):
            q = q2
            qs = "q2"
            break

    while (1):
        inp = input("Listen to a recording?\n")
        try:
            if (os.path.exists("../"+qs+"/"+str(inp)+".wav")):
                os.system("play "+"../"+qs+"/"+str(inp)+".wav")
                continue
        except Exception, e:
            continue

        s = do_one_question(random.choice(q.keys()),q, qs)
        del q[s]

main()