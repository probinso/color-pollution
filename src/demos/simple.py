from more_itertools import unique_everseen as unique

class Human:
    def __init__(self, called):
        self.called = called

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.called)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Professional(Human):
    def jobTask(self):
        return "Doing Stuff"

    def rankedJobSkills(self):
        attr   = 'jobTask'
        mro    = self.__class__.mro() # method resolutino order
        skills = (getattr(cls, attr)(self) for cls in mro if hasattr(cls, attr))
        return list(enumerate(unique(skills)))


class Scientist(Professional):
    def jobTask(self):
        return "Sciencing"


class Developer(Professional):
    def jobTask(self):
        return "Programming"


class Teacher(Professional):
    def jobTask(self):
        return "Teaching"


class DataScientist(Scientist, Developer):
    pass


class DataEngineer(Developer, Scientist):
    pass


class Professor(Teacher, DataScientist):
    pass

