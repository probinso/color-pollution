from more_itertools import unique_everseen as unique

class Human(object):
    def __init__(self, called):
        self.__called = called

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__called)

    def __repr__(self):
        return "%s(%s)" % (self.__class__, self.__called)

    def called(self):
        return self.__called

class Parent(Human):
    def __init__(self, *args, **kwargs):
        Human.__init__(self, *args, **kwargs)

    def homeTask(self):
        return "Parenting"


class Professional(Human):
    def __init__(self, *args, **kwargs):
        Human.__init__(self, *args, **kwargs)

    def jobTask(self):
        return "Doing Stuff"

    def rankedJobSkills(self):
        attr   = 'jobTask'
        mro    = self.__class__.mro() # method resolutino order
        skills = (getattr(cls, attr)(self) for cls in mro if hasattr(cls, attr))
        return list(enumerate(unique(skills)))


class Scientist(Professional):
    def __init__(self, *args, **kwargs):
        Professional.__init__(self, *args, **kwargs)

    def jobTask(self):
        return "Sciencing"


class Developer(Professional):
    def __init__(self, *args, **kwargs):
        Professional.__init__(self, *args, **kwargs)

    def jobTask(self):
        return "Programming"


class Teacher(Professional):
    def __init__(self, *args, **kwargs):
        Professional.__init__(self, *args, **kwargs)

    def jobTask(self):
        return "Teaching"


class DataScientist(Parent, Scientist, Developer, Professional):
    def __init__(self, *args, **kwargs):
        Professional.__init__(self, *args, **kwargs)


class DataEngineer(Developer, Scientist, Professional):
    def __init__(self, *args, **kwargs):
        Professional.__init__(self, *args, **kwargs)


