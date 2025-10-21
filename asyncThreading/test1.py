import threading

class Counter(threading.Thread):
    def counter(self):
        c=0
        for i in range(100000000):
            c+=1
        print(c)

    def run(self):
        self.counter()

class Inputer(threading.Thread):
    def inputer(self):
        for i in range(10):
            x=input("Enter a number: ")
            print(x)

    def run(self):
        self.inputer()

def main():
    thread1=Counter()
    thread2=Inputer()
    thread1.start()
    thread2.start()
    

main()