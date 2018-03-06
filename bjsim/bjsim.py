import npyscreen
from bjsim import utest


class TestSuite:
    tx = None
    rx = None

    def __init__(self, args):
        self.t = ["Normal Operating / Response", "Late Reply", "Mid-Op Reset"]
        self.toRuni = []
        self.toRunt = []

    def listTest(self):
        tests = self.t
        return tests

    def makeList(self, sti):
        self.toRuni = sorted(sti)
        for i in self.toRuni:
            self.toRunt.append(self.t[i])

    def getList(self, rtype):
        if rtype == 'i':
            return self.toRuni
        elif rtype == 't':
            for i in self.toRuni:
                self.toRunt.append(self.t[i])
            return self.toRunt


class StatusForm(npyscreen.ActionFormV2):
    def create(self):
            # TitleSlider name refuses to update...
            self.max_width = 200
            self.sb = self.add(npyscreen.TitleFixedText, name='Progress:', 
                                value='0 / 0')
            self.rs = self.add(npyscreen.TitlePager, rely=5, name="History",
                               hidden=True, max_height=15)
            self.ui = self.add(npyscreen.FixedText, value="Press OK To Begin -->",
                               rely=-3)
    def on_cancel(self):
        self.parentApp.switchForm('MAIN')

    def on_ok(self):
        self.complete = 0
        self.rt = []
        self.ti = self.parentApp.ts.getList('i')
        self.tt = self.parentApp.ts.getList('t')
        self.outof = len(self.ti)
        self.sb.value= '0 / ' + str(self.outof)
        self.rs.hidden = False
        self.ui.value = "Running"
        self.display()
        self.r = utest.Utest(self.parentApp.ts.tx, self.parentApp.ts.rx)
        self.r.MakeLink()

        for self.test in self.ti:
            # Class/function to handle test
            self.complete += 1
            self.sb.value = str(self.complete) + ' / ' + str(self.outof)
            self.display()
            self.result = self.r.RunTest(self.test)
            self.rtn = self.tt.pop(0)
            if not self.result:
                self.result = ' Test Implementation Error'
            self.rtn = self.rtn + ':' + self.result
            self.rt.append(self.rtn)
            self.rs.values = self.rt
            self.display()
        self.ui.value = 'Complete'
        self.r.MakeLink(m='c')
        self.display()

        self.r.MakeLink(m='close')

class TestSelectionForm(npyscreen.ActionFormWithMenus):
    def create(self):
        self.menu = self.new_menu(name='Settings', shortcut="^S")
        self.menu.addItemsFromList([("Configure Serial Ports", self.cs)])
        self.values = self.parentApp.ts.listTest()
        self.selectedTest = self.add(npyscreen.TitleMultiSelect, name="Tests",
                                     values=self.values)

    def cs(self):
        self.parentApp.switchForm("SERIAL")

    def on_ok(self):
        if self.parentApp.ts.tx == 'stdout' or self.parentApp.ts.rx == 'empty':
            self.parentApp.switchForm('WARNING')
        else:
            self.parentApp.ts.makeList(self.selectedTest.value)
            self.parentApp.switchForm("STATUS")

    def on_cancel(self):
        self.parentApp.switchForm(None)


class DeviceWarning(npyscreen.ActionPopup):
    def create(self):
        self.warning = self.add(npyscreen.Textfield, editable=False,
         value='Please Configure Serial Device')

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class SerialConfig(npyscreen.ActionPopup):
    def create(self):
        self.rxp = self.add(npyscreen.TitleFilename, name='Receive:', value='/dev/ttyUSB')
        self.txp = self.add(npyscreen.TitleFilename, name='Transmit:', value='/dev/ttyUSB')
        self.rx_exist = self.rxp.value
        self.tx_exist = self.txp.value

    def on_cancel(self):
        self.parentApp.switchForm('MAIN')

    def on_ok(self):
        if self.txp.value != self.tx_exist:
            self.parentApp.ts.tx = self.txp.value
            self.tx_exist = self.txp.value
        if self.rxp.value != self.rx_exist:
            self.parentApp.ts.rx = self.rxp.value
            self.rx_exist = self.rxp.value
        self.parentApp.switchFormPrevious()


class BongjoviSimulator(npyscreen.NPSAppManaged):
    def __init__(self, args):
        self.args = args
        TestSuite.tx = self.args.tx
        TestSuite.rx = self.args.rx
        super().__init__()

    def onStart(self):
        self.ts = TestSuite(self.args)
        self.addForm('MAIN', TestSelectionForm, name="Bongjovi Simulator")
        self.addForm('STATUS', StatusForm, name='Testing Progress')
        self.addForm('SERIAL', SerialConfig, name='Serial Configuration')
        self.addForm('WARNING', DeviceWarning, name='Serial Device Warning')
