import tkinter as tk
from PIL import ImageTk,Image
import time
from mss import mss
import win32api



#set sizescreen to change tkinker window size and final image size
sizescreen=480
#if you want it to follow your mouse set it to True
followmouse=False
#if you want to press'+' or '-' for not zooming turn it to False
zoomable=True
#change this up (to 20 or whatever) if you lag
waitnss=10  



#win32api.SetCursorPos((1920,1080))
xscreenresolution,yscreenresolution=win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)
leftx,topy=int(xscreenresolution/2-100),int(yscreenresolution/2-100)#;print(xscreenresolution,yscreenresolution)
centurx,century=int(xscreenresolution/2),int(yscreenresolution/2)
sizezoom=3




bounding_box = {'top': topy, 'left': leftx, 'width': 200, 'height': 200}# ;bounding_box = {'top': 440, 'left': 860, 'width': 200, 'height': 200}# I use this because my screen is 1980x1080
ratioset={-4:3,-3:2,-2:1.5,-1:1.25,0:1,1:1.25,2:1.5,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:10,11:12}
sizeset={0:480,1:384,2:320,3:240,4:160,5:120,6:96,7:80,8:60,9:48,'x':1,'y':1,99:192,-1:600,-2:720,-3:960,-4:1440}
#        1     1.25  1.5   2     3     4     5    6    7    8

def cal(size):
    half=int(size/2)
    bounding_box['top']=century-(half*sizeset['x'])
    bounding_box['left']=centurx-(half*sizeset['y'])
    bounding_box['width']=size*sizeset['x']
    bounding_box['height']=size*sizeset['y']

cal(sizeset[sizezoom])

def zoom_image(img,size):
    return img.resize([size*sizeset['x'],size*sizeset['y']], Image.CUBIC)

sct=mss()

button_zoomin=0xBB  #'+'
state_zoomin=win32api.GetKeyState(button_zoomin)

button_zoomout=0xBD  #'-"
state_zoomout=win32api.GetKeyState(button_zoomout)

root = tk.Tk()
root.attributes("-topmost", True)
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
def show_frame():
    global waitnss
    global centurx,century,sizezoom,followmouse,sizescreen
    global button_zoomin,button_zoomout
    global state_zoomin,state_zoomout
    root.lift()
    
    if followmouse:
        centurx,century=win32api.GetCursorPos()
        cal(sizeset[sizezoom])
    if zoomable:
        now_zoomin=win32api.GetKeyState(button_zoomin)
        now_zoomout=win32api.GetKeyState(button_zoomout)
        if now_zoomin<0 and now_zoomin!=state_zoomin and sizezoom<9:
            state_zoomin=now_zoomin
            sizezoom+=1
            cal(sizeset[sizezoom])
        elif now_zoomout<0 and now_zoomout!=state_zoomout and sizezoom>-4:
            state_zoomout=now_zoomout
            sizezoom-=1
            cal(sizeset[sizezoom])
    sct=mss()
    sct_img = sct.grab(bounding_box)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    img=zoom_image(img,sizescreen)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(waitnss, show_frame)
    
    
    
show_frame()
root.mainloop()

print('close in 5 seconds')
time.sleep(5)

#dont care what it is below this line
#------------------------------------------


# maxx=0
# minn=999
    # since it cant get a different below 0.014999999 sec so i will disable it
    # global maxx,minn
    # t=time.monotonic()-t
    # try:
    #     print('fps=',int(1/t))#,'time per image=',t,'max=',maxx)
    #     maxx=max(maxx,t)
    #     minn=min(minn,t)
    # except:
    #     print(f'error(t={t})')
# print('end\nmax time per image =',maxx,f'({int(1/maxx)}fps)','\nmin time per image =',minn,f'({int(1/minn)}fps)')

