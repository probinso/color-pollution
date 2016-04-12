class Human(object):
    def __init__(self, called):
        self.__called = called

    def getCalled(self):
        return self.__called

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.getCalled())

    def __repr__(self):
        return '%s(%s)' % (self.__class__, self.getCalled())

class Parent(Human):
    def __init__(self, *args, **kwargs):
       Human.__init__(self, *args, **kwargs)

    def homeTask(self):
       return 'Parenting'


