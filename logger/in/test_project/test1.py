def foo():
    return beep()

def beep():
    wow = Wow()
    wow.cool()
    return 3

class Wow:
    def cool(self):
        return 10