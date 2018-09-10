
class Keycalls:
    def __init__(self):
        self.ESTOP = 'on_keycall_ESTOP'
        self.POWER = 'on_keycall_POWER'
        self.ABORT = 'on_keycall_ABORT'
        self.XPOS = 'on_keycall_XPOS'
        self.XNEG = 'on_keycall_XNEG'
        self.YPOS = 'on_keycall_YPOS'
        self.YNEG = 'on_keycall_YNEG'
        self.ZPOS = 'on_keycall_ZPOS'
        self.ZNEG = 'on_keycall_ZNEG'
        self.APOS = 'on_keycall_APOS'
        self.ANEG = 'on_keycall_ANEG'
        self.BPOS = 'on_keycall_BPOS'
        self.BNEG = 'on_keycall_BNEG'       
        self.INCREMENTS = 'on_keycall_INCREMENTS'
        self.TEST = 'on_keycall_INCREMENTS'

    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)
      
class Keybinding:
    def __init__(self):
        self.F1 = 'ESTOP'
        self.F2 = 'POWER'
        self.Escape = 'ABORT'
        self.Up = 'YPOS'
        self.Down = 'YNEG'
        self.Right = 'XPOS'
        self.Left = 'XNEG'
        self.Page_Up = 'ZPOS'
        self.Page_Down = 'ZNEG'
        self.Home = 'APOS'
        self.End = 'ANEG'
        self.Insert = 'BPOS'
        self.Delete = 'BNEG'
        self.i = 'INCREMENTS'
        self.I = 'INCREMENTS'

    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

class Keylookup:
    def __init__(self):
        self.keycall = Keycalls()
        self.keybinding = Keybinding()

    def get_call(self,binding):
        try:
            return self.keycall[binding]
        except:
            print "No key function call"
            return None

    def get_binding(self,key):
        try:
            return self.keybinding[key]
        except:
            print "No key binding"
            return None

    def convert(self,key):
        try:
            b = self.keybinding[key]
            return self.keycall[b]
        except:
            return None

    def add_binding(self,key,binding):
        try:
            self.keybinding[key] = binding
        except:
            print "Binding for key %s could not be added"% key

    def add_call(self,binding,function):
        try:
            self.keycall[binding] = function
        except:
            print "Binding %s could not be added"% binding

    def add_conversion(self,key,binding,function):
        self.add_binding(key,binding)
        self.add_call(binding,function)
