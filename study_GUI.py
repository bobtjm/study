import study_interface
import study_data
import getfile
from Tkinter import *

gui = None

class GUI: #view
    updateCats = study_interface.updateCats
    save = None #defined in __init__
    prevQ = study_interface.prevQ
    nextQ = study_interface.nextQ
    updateWord = study_interface.updateWord
    answer = study_interface.answer
    updateQ = study_interface.updateQ
    
    def __init__(self):
        global gui
        gui = self
        self.root = Tk()
        self.q, self.a = StringVar(), StringVar()
        self.data = study_data.Data(getfile.getFile(self.root))
        self.save = self.data.save
        
        self.cats = self.Checkbar(self.root, [c for c in sorted(self.data.categories)], self.data.activeCategories, update = self.updateCats, maxColumns = 6)
        #cats.pack(side = TOP, fill = X)
        self.cats.grid(row = 0)
        self.cats.config(relief=GROOVE, bd=2)
        self.qb = self.QuestionBox(self.q, self.a, self.root)
        self.qb.grid(row = 1)

        self.opt = self.Options(self.root)
        #opt.pack(side = BOTTOM, fil = X)
        self.opt.config(relief=GROOVE, bd=2)
        self.opt.grid(row = 2)
        self.updateCats()
        
    def run(self):
        self.root.mainloop()

    class Checkbar(Frame):
        def __init__(self, parent=None, picks=[], active=[], side=LEFT, anchor=W, update = None, maxColumns = 10):
            Frame.__init__(self, parent)
            self.vars = []
            self.texts = []
            self.updatefunc = update
            r, c = 0, 0
            for pick in picks:
                var = BooleanVar(value = True if active and pick in active else False)
                chk = Checkbutton(self, text=pick, variable=var, command = self.update)
                #chk.pack(side=side, anchor=anchor, expand=NO)
                chk.grid(row = r, column = c)
                c += 1
                if (c >= maxColumns):
                    c = 0
                    r += 1
                self.vars.append(var)
                self.texts.append(pick)
                
        def update(self):
            if self.updatefunc:
                self.updatefunc()
                
        def state(self):
            return map((lambda var: var.get()), self.vars)
            
        def cats(self):
            return [self.texts[i] for i in range(len(self.vars)) if self.vars[i].get()]

    class Options(Frame):
        def __init__(self, parent=None, side = RIGHT, anchor = W):
            Frame.__init__(self, parent)
            Button(self, text='save', command = gui.save).pack(side=side)
            self.cb = gui.Checkbar(self, ["Shuffle", "Skip temporary marked", "Skip universal marked"], [gui.data.shuffle], update = gui.updateCats)
            self.cb.pack(side = side)
            
    class QuestionBox(Frame):
        def __init__(self, q, a, parent = None):
            Frame.__init__(self, parent)
            self.c = gui.Checkbar(self, ["Universal skip", "Temporary skip"], side = TOP, update = study_interface.updateWord, maxColumns = 1)
            self.c.grid(column=3, row = 0)#pack(side = LEFT)
            self.q = Label(self, textvariable = q, width = 71, wraplength = 500)
            self.q.grid(column = 1, row = 0, sticky = W)
            Button(self, text='prev', command = gui.prevQ).grid(row = 2, column=1, sticky = W)#.pack(side = BOTTOM)
            Button(self, text='next', command = gui.nextQ, width = 90).grid(row = 2, column=1, columnspan = 3, sticky = E)#.pack(side = BOTTOM)
            Button(self, text='show answer', command = gui.answer).grid(row = 1, column=2)#.pack(side = BOTTOM)
            Button(self, text='update Q/A', command = gui.updateQ).grid(row = 1, column=3)#.pack(side = BOTTOM)
            self.a = Label(self, textvariable = a, width = 71, wraplength = 500, anchor = CENTER)
            self.a.config(relief=GROOVE, bd=2)
            self.q.config(relief=GROOVE, bd=2)
            self.a.grid(column = 1, row = 1, sticky = W)
            
if __name__ == "__main__":
    GUI().run()
