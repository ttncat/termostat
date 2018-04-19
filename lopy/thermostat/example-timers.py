from machine import Timer

t = Timer.Alarm(lambda f:print("hello"), 1, periodic=True)
