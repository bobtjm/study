from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import askyesno, askokcancel
from shutil import copyfile
from os.path import isfile

def getFile(parent = None):
    file_opt = {"defaultextension": ".xlsx",
                "filetypes": [("Excel spreadsheet", ".xlsx;.xls")],
                "multiple": False,
                "title": "Choose a file"}
    if parent:
        file_opt["parent"] = parent
    filename = askopenfilename(**file_opt)
    while askyesno("Create backup?", "Create backup? (This is recommended when you use a new spreadsheet for the first time.)"):
        file_opt["initialfile"] = filename + ".backup.xlsx"
        if "multiple" in file_opt:
            del file_opt["multiple"]
        backup = asksaveasfilename(**file_opt)
        if (isfile(backup)):
            if not askokcancel("Create backup?", "This will overwrite the current file named " + backup + ". Do you still want to continue?"):
                continue
        copyfile(filename, backup)
        break
    return filename
