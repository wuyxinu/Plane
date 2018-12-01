#image.py

def load_image(tkinter):
	return \
		tkinter.PhotoImage(file = "../image/background.png")\
		,tkinter.PhotoImage(file = "../image/bee.gif")\
		,tkinter.PhotoImage(file = "../image/bullet.gif")\
		,tkinter.PhotoImage(file = "../image/hero.gif")\
		,tkinter.PhotoImage(file = "../image/hero0.gif")\
		,tkinter.PhotoImage(file = "../image/smallplane.gif")\
		,tkinter.PhotoImage(file = "../image/张学友1.png")\
		,tkinter.PhotoImage(file = "../image/爆炸.png")\
		,tkinter.PhotoImage(file = "../image/protection.png")\
		,tkinter.PhotoImage(file="../image/bigplane.gif")
def load_state_image(tkinter):
	return \
		tkinter.PhotoImage(file = "../image/start.png")\
		,tkinter.PhotoImage(file = "../image/stop.png")\
		,tkinter.PhotoImage(file = "../image/pause.png")

def load_smallPlane_image(tkinter):
	return \
		tkinter.PhotoImage(file = "../image/smllplane_bomb1.png")\
		,tkinter.PhotoImage(file = "../image/smllplane_bomb2.png")\
		,tkinter.PhotoImage(file = "../image/smllplane_bomb3.png")

def load_MidPlane_image(tkinter):
	return \
		tkinter.PhotoImage(file = "../image/plane_bomb1.png")\
		,tkinter.PhotoImage(file = "../image/plane_bomb2.png")\
		,tkinter.PhotoImage(file = "../image/plane_bomb3.png")\
		,tkinter.PhotoImage(file = "../image/plane_bomb4.png")