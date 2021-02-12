"""
PERSONAL PLANNER "PlanApp"
DEMO DESKTOP APPLICATION
using Python Tkinter

Author: Marcus Lowndes


"""
import tkinter as tk
from tkinter import messagebox
import calendar
import datetime


notes = []
lists = []
allMonths = {}  # allocate each month's name to it's number
for i in range(1, 13): allMonths[calendar.month_name[i]] = i


class Note:
    """A note that can be saved and attributed to a particular day."""
    def __init__(self, title, text):
        self.title = title
        self.text = text
    def setDate(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


class List:
    """A note that can be saved and attributed to a particular day."""
    def __init__(self, title, textList):
        self.title = title
        self.listBody = []
        for text in textList:
            self.listBody.append(text)
    def setDate(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


class MakeNote(tk.Frame):
    """An app allowing the user to make a new note"""
    def __init__(self, parent, day, month, year, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        self.window = parent
        self.day = day
        self.month = month
        self.year = year

        self.noteTitle = tk.StringVar(self.window)
        self.noteTitle.set("")
        self.selectedDay = tk.IntVar(self.window)
        self.selectedDay.set(self.day)
        self.selectedMonth = tk.StringVar(self.window)
        self.selectedMonth.set(calendar.month_name[self.month])
        self.selectedYear = tk.IntVar(self.window)
        self.selectedYear.set(self.year)

        self.topFrame = self.topFrame()
        self.noteFrame = self.noteFrame()
        self.botFrame = self.botFrame()

    def topFrame(self):
        """Title entry box for note"""
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(side='top', pady=10)

        self.titleLabel = tk.Label(self.window, text=" Title:  ")
        self.titleLabel.pack(in_=self.topFrame, side=tk.LEFT)

        self.title = tk.Entry(self.window, width=31, font='Helvetica', bd=2,
                              textvariable=self.noteTitle, relief=tk.SUNKEN)
        self.title.pack(in_=self.topFrame, side=tk.RIGHT, ipady=5, ipadx=3)

    def noteFrame(self):
        """Note itself goes here, with scrollbar"""
        self.noteFrame = tk.Frame(self.window, bd=5, relief=tk.SUNKEN,)
        self.noteFrame.pack(side='top', padx=10)

        self.noteBox = tk.Text(self.window, font='Helvetica', padx=7,
                               pady=5, wrap=tk.WORD, width=33, height=20,)
        self.noteBox.pack(in_=self.noteFrame, side=tk.LEFT, fill=tk.BOTH)

        self.noteScroll = tk.Scrollbar(self.window, orient=tk.VERTICAL,
                                       command=self.noteBox.yview)
        self.noteScroll.pack(in_=self.noteFrame, side=tk.RIGHT, fill=tk.Y)
        self.noteBox.config(yscrollcommand=self.noteScroll.set,)

    def botFrame(self):
        """Submit Button"""
        self.botFrame = tk.Frame(self.window)
        self.botFrame.pack(side=tk.BOTTOM, pady=10)

        self.daySelection = tk.OptionMenu(
            self.window, self.selectedDay, *range(1, 32)
        )
        self.daySelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.daySelection.config(width=5, pady=7)

        self.monthSelection = tk.OptionMenu(
            self.window, self.selectedMonth, *allMonths.keys()
        )
        self.monthSelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.monthSelection.config(width=10, pady=7)

        self.yearSelection = tk.OptionMenu(
            self.window, self.selectedYear, *range(2005, 2030)
        )
        self.yearSelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.yearSelection.config(width=5, pady=7)

        self.newNoteBut = tk.Button(
            self.window, text="Save", width=10, pady=5, bg='pink',
            overrelief=tk.GROOVE, command=lambda: self.submit(
                self.noteTitle.get(), self.noteBox.get('1.0', 'end'),
                self.selectedDay.get(), allMonths[self.selectedMonth.get()],
                self.selectedYear.get()
            )
        )
        self.newNoteBut.pack(side=tk.RIGHT, in_=self.botFrame)

    def submit(self, title, text, day, month, year):
        """Save the note from the text box and attribute it to a particular day"""
        if messagebox.askyesno("Are you sure?", (
                "This will save your note, however it cannot " +
                "be edited in this version of the application."
        )) is True:
            if day in list(calendar.Calendar().itermonthdays(year, month)):
                newNote = Note(title, text)
                newNote.setDate(day, month, year)
                notes.append(newNote)
                self.window.destroy()
            else: messagebox.showerror("Error", (
                "That day is not in {month} {year}.\n" +
                "Please select a different day to submit this note to."
            ))


class SmartEntry(tk.Entry):
    """Stolen from https://stackoverflow.com/a/34953716 """
    def __init__(self, master, side, in_, ipadx, ipady, content='', name=None):
        self.text = tk.StringVar(master, content, name)
        tk.Entry.__init__(self, master, textvariable=self.text, bd=2,
                          width=33, font='Helvetica', relief=tk.SUNKEN)
        self.pack(side=side, in_=in_, ipadx=ipadx, ipady=ipady)
    def get(self): return self.text.get()
    def set(self, text): return self.text.set(text)
    def disable(self): self.config(state=tk.DISABLED)


class MakeList(tk.Frame):
    """An app allowing the user to make a new list"""
    def __init__(self, parent, day, month, year, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)
        self.window = parent
        self.numItems = 0
        self.day = day
        self.month = month
        self.year = year
        self.i = 0
        self.listItems = []

        self.listTitle = tk.StringVar(self.window)
        self.listTitle.set("")
        self.listItemText = tk.StringVar(self.window)
        self.listItemText.set("")
        self.selectedDay = tk.IntVar(self.window)
        self.selectedDay.set(self.day)
        self.selectedMonth = tk.StringVar(self.window)
        self.selectedMonth.set(calendar.month_name[self.month])
        self.selectedYear = tk.IntVar(self.window)
        self.selectedYear.set(self.year)

        self.topFrame = self.topFrame()

        self.listFrame = tk.Frame(self.window, bd=5, relief=tk.SUNKEN)
        self.listFrame.pack(side=tk.TOP, padx=10)
        self.addListItemBut = tk.Button(
            self.window, padx=3, bg='lightgreen', overrelief=tk.GROOVE,
            command=self.newListItem, text="Save Current Item & Add New Item"
        )
        self.addListItemBut.pack(side=tk.BOTTOM, in_=self.listFrame, fill=tk.X)
        self.listItem1 = self.listItem()

        self.botFrame = self.botFrame()

    def topFrame(self):
        """Title entry box for note"""
        self.topFrame = tk.Frame(self.window)
        self.topFrame.pack(side=tk.TOP, pady=10)

        self.titleLabel = tk.Label(self.window, text=" Title:  ")
        self.titleLabel.pack(in_=self.topFrame, side=tk.LEFT)

        self.title = tk.Entry(self.window, width=31, font='Helvetica', bd=2,
                              textvariable=self.listTitle, relief=tk.SUNKEN)
        self.title.pack(in_=self.topFrame, side=tk.RIGHT, ipady=5, ipadx=3)

    def newListItem(self):
        self.listItems.append(self.itemText.get())
        self.itemText.disable()
        self.newItem = self.listItem()

    def listItem(self):
        self.i += 1
        self.itemFrame = tk.Frame(self.window)
        self.itemFrame.pack(side=tk.TOP, pady=5, in_=self.listFrame)

        self.itemNum = tk.Label(self.window, text=("  " + str(self.i) + ".  "))
        self.itemNum.pack(in_=self.itemFrame, side=tk.LEFT)
        self.itemText = SmartEntry(self.window, tk.RIGHT, self.itemFrame, 3, 3)
        self.itemText.pack(in_=self.itemFrame, side=tk.RIGHT, ipady=3, ipadx=3)

    def botFrame(self):
        """Submit Button"""
        self.botFrame = tk.Frame(self.window)
        self.botFrame.pack(side=tk.BOTTOM, pady=10)

        self.daySelection = tk.OptionMenu(
            self.window, self.selectedDay, *range(1, 32)
        )
        self.daySelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.daySelection.config(width=5, pady=7)

        self.monthSelection = tk.OptionMenu(
            self.window, self.selectedMonth, *allMonths.keys()
        )
        self.monthSelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.monthSelection.config(width=10, pady=7)

        self.yearSelection = tk.OptionMenu(
            self.window, self.selectedYear, *range(2005, 2030)
        )
        self.yearSelection.pack(side=tk.LEFT, in_=self.botFrame)
        self.yearSelection.config(width=5, pady=7)

        self.newNoteBut = tk.Button(
            self.window, text="Save", width=10, pady=5, bg='pink',
            overrelief=tk.GROOVE, command=lambda: self.submit(
                self.listTitle.get(), self.listItems, self.itemText.get(),
                self.selectedDay.get(), allMonths[self.selectedMonth.get()],
                self.selectedYear.get()
            )
        )
        self.newNoteBut.pack(side=tk.RIGHT, in_=self.botFrame)

    def submit(self, title, listBody, finalItem, day, month, year):
        """Save the note from the text box and attribute it to a particular day"""
        listBody.append(finalItem)
        if messagebox.askyesno("Are you sure?", (
                "This will save your list, however it cannot " +
                "be edited in this version of the application."
        )) is True:
            if day in list(calendar.Calendar().itermonthdays(year, month)):
                newList = List(title, listBody)
                newList.setDate(day, month, year)
                lists.append(newList)
                self.window.destroy()
            else: messagebox.showerror("Error", (
                "That day is not in {month} {year}.\n" +
                "Please select a different day to submit this list to."
            ))


class PlanApp(tk.Frame):
    """Tkinter application to view and edit the calendar."""
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        self.window = parent
        self.cal = calendar.Calendar()
        self.today = str(datetime.date.today())
        self.month = int(self.today[5:7])
        self.year = int(self.today[:4])
        self.day = int(self.today[8:])
        self.monthName = calendar.month_name[self.month]

        # initialize user input variables
        self.selectedMonth = tk.StringVar(self.window)
        self.selectedMonth.set(self.monthName)
        self.selectedYear = tk.IntVar(self.window)
        self.selectedYear.set(self.year)

        # initialize top frame with option menus
        self.calendarMenu1 = self.calendarMenu()

        # initialize calendar with individual buttons for each day
        self.calendarFrame = tk.LabelFrame(
            self.window, bd=5, relief=tk.SUNKEN, labelanchor=tk.N,
            text=(" " + self.monthName + "  " + str(self.year) + " ")
        )
        self.calendarFrame.grid(padx=10, columnspan=7, rowspan=5)
        self.calendarButs = self.calendar()

        # initialize bottom frame with buttons to create new notes/lists
        self.botButs = self.bottomButs()

    def calendarMenu(self):
        """Create OptionMenus to select the calendar"""
        self.topFrame = tk.Frame(self.window)
        self.topFrame.grid(padx=5, pady=10)

        self.monthSelection = tk.OptionMenu(
            self.window, self.selectedMonth, *allMonths.keys()
        )
        self.monthSelection.grid(row=0, column=0, padx=10, in_=self.topFrame)
        self.monthSelection.config(width=10, pady=7)

        self.yearSelection = tk.OptionMenu(
            self.window, self.selectedYear, *range(2005, 2030)
        )
        self.yearSelection.grid(row=0, column=1, in_=self.topFrame)
        self.yearSelection.config(width=5, pady=7)

        self.filler = tk.Frame(self.window)
        self.filler.grid(row=0, column=3, padx=30, in_=self.topFrame)

        self.updateBut = tk.Button(
            text='Update Calendar', width=15, pady=5, bd=3,
            command=lambda: self.updateCalendar(
                self.selectedYear.get(), self.selectedMonth.get()
            ), overrelief=tk.GROOVE, bg='lightyellow'
        )
        self.updateBut.grid(row=0, column=4, in_=self.topFrame)

    def calendar(self):
        """Create buttons in calendarFrame, current day appears green."""
        j = 0
        k = 1
        for i in self.cal.itermonthdays(self.year, self.month):
            j += 1
            if (i == 0) or ():
                self.dayBut = tk.Button(
                    self.window, width=5, bd=3, pady=13,
                    bg='lightblue', overrelief=tk.GROOVE,
                    command=lambda i=i: self.openDay(i)
                )
                self.dayBut.grid(row=k, column=j, columnspan=1,
                                 pady=3, padx=3, in_=self.calendarFrame)
            elif (i == self.day) and ((int(self.today[5:7]) == self.month)
                                      and (int(self.today[:4]) == self.year)):
                self.dayBut = tk.Button(
                    self.window, text=i, width=5, pady=13, bd=3,
                    bg='lightgreen', overrelief=tk.GROOVE,
                    command=lambda i=i: self.openDay(i)
                )
                self.dayBut.grid(row=k, column=j, columnspan=1,
                                 pady=3, padx=3, in_=self.calendarFrame)
            else:
                self.dayBut = tk.Button(
                    self.window, text=i, width=5, pady=13, bd=3,
                    bg='lightblue', overrelief=tk.GROOVE,
                    command=lambda i=i: self.openDay(i)
                )
                self.dayBut.grid(row=k, column=j, columnspan=1,
                                 pady=3, padx=3, in_=self.calendarFrame)
            if j == 7:
                j = 0
                k += 1

    def updateCalendar(self, year, month):
        """Take selected year and month from OptionMenu and reset calendarFrame"""
        self.year = year
        self.month = allMonths[month]
        self.monthName = month
        self.calendarFrame.destroy()
        self.calendarFrame = tk.LabelFrame(
            self.window, bd=5, relief=tk.SUNKEN, labelanchor=tk.N,
            text=(" " + self.monthName + "  " + str(self.year) + " ")
        )
        self.calendarFrame.grid(padx=10, columnspan=7, rowspan=5, row=1)
        self.calendarButs = self.calendar()

    def listDisplayables(self, i):
        """Reads through all the currently saved notes and if the
        date matches the chosen day, add them to list of displayables"""
        displayables = [[],[]]
        for eachNote in notes:
            if ((eachNote.day == i)
                    and (eachNote.month == self.month)
                    and (eachNote.year == self.year)):
                displayables[0].append(eachNote)
        for eachList in lists:
            if ((eachList.day == i)
                    and (eachList.month == self.month)
                    and (eachList.year == self.year)):
                displayables[1].append(eachList)
        return displayables

    def makeDisplayables(self, l):
        """Coverts list of displayables into readable strings"""
        s1 = ''
        s2 = ''
        if (len(l[0]) == 0): s1 += "No notes for this day."
        if (len(l[1]) == 0): s2 += "No lists for this day."
        for i in l[0]:
            if isinstance(i, Note):
                s1 += (i.title + '\n\n' + i.text + '\n')
            s1 += "------------------------------------\n"
        for i in l[1]:
            if isinstance(i, List):
                s2 += (i.title + '\n')
                k = 0
                for j in i.listBody:
                    k += 1
                    s2 += ('\n' + str(k) + ':  ' + j)
                s2 += '\n\n------------------------------------\n'
        return [s1, s2]

    def infoFrame(self, top, title, s, column, text):
        """Frame for displaying either all notes or all lists for that day"""
        label = tk.Label(top, text=title, font="Helvetica")
        label.grid(row=1, column=column, padx=20, pady=7)

        frame = tk.Frame(top, bd=5, relief=tk.SUNKEN,)
        frame.grid(row=2, column=column, padx=10)

        info = tk.Text(top, font='Helvetica', padx=7, pady=5,
                       wrap=tk.WORD, width=20, height=20,)
        info.grid(in_=frame, row=1, column=0)

        scroll = tk.Scrollbar(top, orient=tk.VERTICAL, command=info.yview)
        scroll.grid(in_=frame, row=1, rowspan=1, column=1, sticky=tk.NS)
        info.insert(tk.INSERT, text + s)
        info.config(yscrollcommand=scroll.set, state=tk.DISABLED, bg='lightgrey')

    def dayWindow(self, i, s, text):
        """New window displaying all notes and lists for that day"""
        top = tk.Toplevel(self)
        top.resizable(0,0)
        top.wm_title(str(i) + " " + self.monthName + " " + str(self.year))
        self.topF = tk.Frame(top)
        self.topF.grid(row=0, columnspan=2, pady=2)
        self.infoFrame(top, "Notes", s[0], 0, text)
        self.infoFrame(top, "Lists", s[1], 1, '')
        self.botF = tk.Frame(top)
        self.botF.grid(row=3, columnspan=2, pady=5)

    def openDay(self, i):
        """When a day is clicked, a messagebox will
         appear showing information about that day"""
        l = self.listDisplayables(i)
        s = self.makeDisplayables(l)
        if i == 0: return messagebox.showwarning(
            "Cannot show info", (
                    "That day is not in " + self.monthName +
                    " " + str(self.year) + "."
            ), parent=self.window
        )
        elif int(self.today[8:]) == i: return self.dayWindow(
            i, s, ("This is the current day!\n\n------" +
                   "------------------------------\n")
        )
        else: return self.dayWindow(i, s, '')

    def bottomButs(self):
        """Buttons to create new notes or lists."""
        self.botFrame = tk.Frame(self.window)
        self.botFrame.grid(padx=5, pady=10)

        self.newNoteBut = tk.Button(
            self.window, text="Make a new Note",
            width=15, pady=7, bg='pink', overrelief=tk.GROOVE,
            command=lambda: self.makeNewNote()
        )
        self.newNoteBut.grid(column=0, row=0, padx=5, in_=self.botFrame)

        self.newListBut = tk.Button(
            self.window, text="Make a new List",
            width=15, pady=7, bg='pink', overrelief=tk.GROOVE,
            command=lambda: self.makeNewList()
        )
        self.newListBut.grid(column=1, row=0, padx=5, in_=self.botFrame)

    def makeNewNote(self):
        """Initialize a new window to create a new note"""
        if __name__ == "__main__":
            noteApp(self.day, self.month, self.year)

    def makeNewList(self):
        """Initialize a new window to create a new list"""
        if __name__ == "__main__":
            listApp(self.day, self.month, self.year)


def noteApp(day, month, year):
    """Run note creator app"""
    root = tk.Tk()
    MakeNote(root, day, month, year).pack()
    root.resizable(0, 0)
    root.title("New Note")


def listApp(day, month, year):
    """Run list creator app"""
    root = tk.Tk()
    MakeList(root, day, month, year).pack()
    root.resizable(0, 0)
    root.title("New List")


def mainApp():
    """Run main app"""
    root = tk.Tk()
    PlanApp(root).grid()
    root.resizable(0, 0)
    root.title("PlanApp - Your Personal Planner")
    root.mainloop()


# Run main application
if __name__ == '__main__':
    mainApp()

