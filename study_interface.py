import random
currentIndex = 0
allQs = []
skipu = False
skipt = False
    
#prerequisites:
#self has:
#  q - StringVar()
#  a - StringVar()
#  data - Data
#  cats - Checkbar
#  opt - Options

def nextQ(self):
    global currentIndex, allQs
    currentIndex += 1
    if currentIndex >= len(allQs):
        currentIndex = 0
    if (len(allQs) != 0):
        self.q.set(allQs[currentIndex].question)
        self.qb.c.vars[0].set(allQs[currentIndex].uskip)
        self.qb.c.vars[1].set(allQs[currentIndex].tskip)
    else:
        self.q.set("")
        self.qb.c.vars[0].set(False)
        self.qb.c.vars[1].set(False)
    self.a.set("")

def prevQ(self):
    global currentIndex, allQs
    currentIndex -= 1
    if currentIndex < 0:
        currentIndex = len(allQs) - 1
    if (len(allQs) != 0):
        self.q.set(allQs[currentIndex].question)
        self.qb.c.vars[0].set(allQs[currentIndex].uskip)
        self.qb.c.vars[1].set(allQs[currentIndex].tskip)
    else:
        self.q.set("")
        self.qb.c.vars[0].set(False)
        self.qb.c.vars[1].set(False)
    self.a.set("")
    
def answer(self):
    global currentIndex, allQs
    if (len(allQs) != 0):
        self.a.set("\n".join(allQs[currentIndex].answers))
        
def updateWord(self):
    allQs[currentIndex].uskip = self.qb.c.state()[0]
    allQs[currentIndex].tskip = self.qb.c.state()[1]
    self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].uskip = allQs[currentIndex].uskip
    self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].tskip = allQs[currentIndex].tskip

def updateCats(self):
    global activeCategories, skipt, skipu, allQs, currentIndex
    currentIndex = -1
    self.data.activeCategories = self.cats.cats()
    allQs = []
    self.data.shuffle = self.opt.cb.state()[0]
    skipt = self.opt.cb.state()[1]
    skipu = self.opt.cb.state()[2]
    for c in self.data.activeCategories:
        for item in self.data.categories[c]:
            if not (skipu and item.uskip) and not (skipt and item.tskip):
                allQs.append(item)
    if self.data.shuffle:
        random.shuffle(allQs)
    nextQ(self)

def updateQ(self):
    global currentIndex, allQs
    newQ = raw_input("New question: (leave blank to keep) ")
    newA = raw_input("New answer: (leave blank to keep) ")
    oldQ = self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].question
    oldA = "; ".join(self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].answers)
    if not newQ: newQ = oldQ
    if not newA: newA = oldA
    if raw_input("\n\nOld question: %s\nNew question: %s\n\nOld answer: %s\nNew answer: %s\nOkay to switch? (y or n) "%(oldQ, newQ, oldA, newA)) == 'y':
        self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].question = newQ
        self.data.categories[allQs[currentIndex].category][allQs[currentIndex].index - 1].answers = [txt.strip() for txt in newA.split(';')]
        allQs[currentIndex].question = newQ
        allQs[currentIndex].answers = [txt.strip() for txt in newA.split(';')]
        self.q.set(newQ)
        if self.a.get():
            self.a.set("\n".join([txt.strip() for txt in newA.split(';')]))
        print "Saved new question."
    else:
        print "Didn't save question."
