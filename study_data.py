from openpyxl import *

class Data: #Model
    class Question:
        def __init__(self, sheet, cat, answers, question, uskip, tskip, catindex, overallindex):
            self.category = sheet[cat].internal_value
            self.answers = [s.strip() for s in str(sheet[answers].internal_value).split(';')]
            self.question = sheet[question].internal_value#.strip()
            self.uskip = sheet[uskip].internal_value
            self.tskip = sheet[tskip].internal_value
            self.index = sheet[catindex].internal_value
            self.index2 = overallindex

        def __str__(self):
            return str(self.uskip)+str(self.tskip)+str(self.question)

    def __init__(self, filename):
        self.wb = load_workbook(filename, data_only = True)
        self.filename = filename
        self.datasheet = self.wb.get_sheet_by_name('Data')
        self.settingsheet = settingsheet = self.wb.get_sheet_by_name('Settings')
        self.ccat = settingsheet["C2"].value
        self.qcat = settingsheet["D2"].value
        self.acat = settingsheet["E2"].value
        self.icat = settingsheet["F2"].value
        self.ucat = settingsheet["G2"].value
        self.tcat = settingsheet["H2"].value
        self.shuffle = settingsheet["A2"].value
        self.activeCategories = settingsheet["B2"].value
        if self.activeCategories:
            self.activeCategories = self.activeCategories.split(";")
        self.row = 2
        self.categories = {}
        while self.datasheet['%s%d' % (self.ccat, self.row)].value != None:
            c = self.datasheet['%s%d' % (self.ccat, self.row)].value
            if c not in self.categories:
                self.categories[c] = []
            self.categories[c].append(self.Question(self.datasheet, "%s%d" % (self.ccat, self.row), #category
                                                    "%s%d" % (self.acat, self.row), #answer
                                                    "%s%d" % (self.qcat, self.row), #question
                                                    "%s%d" % (self.ucat, self.row), #universal skip
                                                    "%s%d" % (self.tcat, self.row), #temporary skip
                                                    "%s%d" % (self.icat, self.row), self.row - 1)) #indices
            self.row += 1
        print "Loaded %d questions." % (self.row - 2)

    def save(self):
        print "writing to spreadsheet..."
        for c in self.categories:
            for item in self.categories[c]:
                #if c == "Chapter 17": print item
                row = int(item.index2) + 1
                self.datasheet["%s%d" % (self.qcat, row)].value = item.question
                self.datasheet["%s%d" % (self.acat, row)].value = ';'.join(item.answers)
                self.datasheet["%s%d" % (self.tcat, row)].value = item.tskip
                self.datasheet["%s%d" % (self.ucat, row)].value = item.uskip
        self.settingsheet['B2'].value = ';'.join(self.activeCategories)
        if self.shuffle:
            self.settingsheet['A2'].value = 'Shuffle'
        else:
            self.settingsheet['A2'].value = ''
        print "saving file..."
        self.wb.save(self.filename)
        print "Saved!"
