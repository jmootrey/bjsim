import npyscreen
import time

class TestSuite(object):

    def __init__(self):
        self.t = ["Normal Operating / Response", "Late Reply", "Mid-Op Reset"]
        self.toRuni = None
        self.toRunt = None
        self.toRunz = None

    def listTest(self, ):
        tests = self.t
        return tests

    def makeList(self, sti, stt):
        self.toRuni, self.toRunt = sti, stt
        self.toRunz = zip(sti, stt)
        self.toRunz = sorted(self.toRunz)
        self.toRuni, self.toRunt = [], []
        for i in self.toRunz:
            self.toRuni.append(i[0])
            self.toRunt.append(i[1])

    def getList(self, rtype):
        if rtype == 'i':
            tr = self.toRuni
            return tr
        elif rtype == 't':
            tr = self.toRunt
            return tr
        else:
            tr = self.toRunz
            return tr


class StatusForm(npyscreen.ActionFormV2):
    def create(self):
            # TitleSlider name refuses to update...
            self.max_width = 200
            self.sb = self.add(npyscreen.TitleSlider, name='Progress:', step=0,
                               out_of=100, max_width=50)
            self.rs = self.add(npyscreen.TitlePager, rely=5, name="History",
                               hidden=True, max_height=15)
            self.ui = self.add(npyscreen.FixedText, value="Press OK To Begin",
                               rely=-3)

    def on_ok(self):
        self.rt = []
        self.ti = self.parentApp.ts.getList('i')
        self.tt = self.parentApp.ts.getList('t')
        self.sb.out_of = len(self.ti)
        self.rs.hidden = False
        self.ui.value = "Running"
        self.display()
        self.r = RunTest()
        for test in self.ti:
            # Class/function to handle test
            self.result = self.r.t(0)
            self.rtn = self.tt.pop(0)
            self.rtn = self.rtn + self.result
            self.rt.append(self.rtn)
            self.rs.values = self.rt
            self.sb.value += 1
            self.display()


# debug
class RunTest:

    def t(self, id):
        time.sleep(1)
        if id == 0:
            return ': Ok'
        elif id == 1:
            return ' Ok'
        elif id == 2:
            return ' Ok'


class TestSelectionForm(npyscreen.ActionFormV2):
    def create(self):
        self.values = self.parentApp.ts.listTest()
        self.selectedTest = self.add(npyscreen.TitleMultiSelect, name="Tests",
                                     values=self.values)

    def on_ok(self):
        self.parentApp.ts.makeList(self.selectedTest.value,
                                   self.selectedTest.values)
        self.parentApp.switchForm("STATUS")


class BongjoviSimulator(npyscreen.NPSAppManaged):
    def onStart(self):
        self.ts = TestSuite()
        self.addForm('MAIN', TestSelectionForm, name="Bongjovi Simulator")
        self.addForm('STATUS', StatusForm, name='Testing Progress')
