# importing modules
from math import *
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import askyesno
from pygame import *

# initialize pygame and mixer settings
mixer.pre_init(44100, -16, 2, 2048)
init()

# removing tkinter window when quit
root = Tk()
root.withdraw()

# setting window size
WIDTH, HEIGHT = 1200, 800
# creating surfaces
screen = display.set_mode((WIDTH, HEIGHT))

# displaying window icon
icon = image.load("assets/icon.png")
display.set_icon(icon)
# setting window caption
display.set_caption("AOT Paint")

# setting colour rgb values
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# creating tool names and getting file names
toolNames = ["stamp0", "stamp1", "stamp2", "stamp3", "stamp4", "stamp5", "pencil",
             "eraser", "line", "fill", "rect", "ellipse", "brush", "clear", "text"]
toolImg = ["assets/pencil.png", "assets/eraser.png", "assets/line.png",
           "assets/paintbucket.png", "assets/rect.png", "assets/circle.png",
           "assets/brush.png", "assets/clear.png", "assets/text.png"]

# creating stamp names and loading files with transparency
stampNames = ["stamp0", "stamp1", "stamp2", "stamp3", "stamp4"]
stamps = [image.load("assets/stamp0.png").convert_alpha(),
          image.load("assets/stamp1.png").convert_alpha(),
          image.load("assets/stamp2.png").convert_alpha(),
          image.load("assets/stamp3.png").convert_alpha(),
          image.load("assets/stamp4.png").convert_alpha()]

# creating rect list for tools and stamps for collisions and other interactions
toolRects = [(280, 93, 65, 65), (363, 93, 65, 65), (440, 93, 65, 65), (516, 93, 65, 65),
             (588, 93, 65, 65), (685, 93, 60, 60)]
stampRects = []

# loading and blitting background & other theme images
bg = image.load("assets/bg.jpg").convert()
screen.blit(bg, (0, 0))
logo = transform.scale(image.load("assets/aotlogo.png").convert_alpha(), (270, 100))
screen.blit(logo, (5, 60))

# loading and blitting colour palette w/ colour preview
colourPicker = image.load("assets/colourpicker.jpg").convert()
paletteRect = colourPicker.get_rect(topleft=(897, 40))
screen.blit(colourPicker, (897, 40))
currColRect = Rect(840, 40, 55, 55)
currColRect2 = Rect(840, 40, 55, 55)
draw.rect(screen, WHITE, paletteRect, 2)  # drawing colour rect

# loading and blitting text "color" w/ font "Minecraft.ttf"
fontSmall = font.Font("assets/Minecraft.ttf", 15)
fontMed = font.Font("assets/Minecraft.ttf", 17)
colourText = fontSmall.render("COLOR", True, WHITE)
screen.blit(colourText, (840, 100))

# creating & drawing canvas with menu
canvasRect = Rect(275, 195, 900, 585)
canvasOutlineRect = Rect(270, 190, 910, 595)
draw.rect(screen, WHITE, canvasRect)
draw.rect(screen, BLACK, canvasOutlineRect, 5)

menuRect = Rect(0, 0, 1200, 33)
draw.rect(screen, (70, 10, 10), menuRect)

# creating and drawing stamp background
stampRect = Rect(275, 90, 500, 70)
draw.rect(screen, BLACK, stampRect, 0)
stampRect2 = Rect(275, 90, 500, 70)
draw.rect(screen, WHITE, stampRect2, 2)

# creating stamp adder rect and img
stampSize = 80
isUserStamp = False
stampAdderImg = image.load("assets/addstamp.png").convert_alpha()
screen.blit(stampAdderImg, (785, 110))
addStampRect = Rect(785, 105, 40, 40)
colourText = fontSmall.render("NEW", True, WHITE)
screen.blit(colourText, (695, 113))
colourText = fontSmall.render("STAMP", True, WHITE)
screen.blit(colourText, (689, 128))

# creating slider rects
sliderRect = Rect(25, 440, 216, 30)
sliderRect2 = Rect(25, 440, 230, 30)
thicknessText = fontSmall.render("TOOL THICKNESS", True, WHITE)
redRect = Rect(25, 490, 216, 30)
redRect2 = Rect(25, 490, 230, 30)
greenRect = Rect(25, 530, 216, 30)
greenRect2 = Rect(25, 530, 230, 30)
blueRect = Rect(25, 570, 216, 30)
blueRect2 = Rect(25, 570, 230, 30)

# creating menu buttons for save/load/undo/redo/fill/music
# volume/pauseplay/eyedropper/zoom/playlist
saveRect = Rect(10, 0, 40, 30)
saveimg = image.load("assets/save.png").convert_alpha()
screen.blit(saveimg, (10, 3))
loadRect = Rect(60, 0, 40, 30)
loadimg = image.load("assets/load.png").convert_alpha()
screen.blit(loadimg, (60, 3))
undoRect = Rect(110, 0, 40, 30)
undoimg = image.load("assets/undo.png").convert_alpha()
screen.blit(undoimg, (110, 4))
redoRect = Rect(160, 0, 40, 30)
redoimg = image.load("assets/redo.png").convert_alpha()
screen.blit(redoimg, (160, 4))
fillRect = Rect(210, 0, 40, 30)
fillimg = image.load("assets/fill.png").convert_alpha()
fillimg = transform.scale(fillimg, (35, 35))
screen.blit(fillimg, (210, -5))
musicRect = Rect(360, 0, 40, 30)
musicimg = image.load("assets/music.png").convert_alpha()
musicimg = transform.scale(musicimg, (33, 33))
screen.blit(musicimg, (360, 0))
voldownRect = Rect(415, 0, 30, 30)
voldownimg = image.load("assets/volumedown.png").convert_alpha()
voldownimg = transform.scale(voldownimg, (33, 33))
screen.blit(voldownimg, (415, 0))
volupRect = Rect(455, 0, 40, 30)
volupimg = image.load("assets/volumeup.png").convert_alpha()
volupimg = transform.scale(volupimg, (33, 33))
screen.blit(volupimg, (455, 0))
pauseplayRect = Rect(755, 4, 30, 30)
pauseplayimg = image.load("assets/pauseplay.png").convert_alpha()
pauseplayimg = transform.scale(pauseplayimg, (25, 25))
helpRect = Rect(1165, 2, 30, 30)
eyedropperimg = image.load("assets/eyedropper.png")
screen.blit(eyedropperimg, (265, 0))
eyedropperRect = Rect(265, 0, 40, 30)
zoomimg = image.load("assets/zoom.png")
screen.blit(zoomimg, (315, 0))
zoomRect = Rect(315, 0, 35, 30)
playlistRect = Rect(805, 0, 40, 30)
playlistimg = image.load("assets/playlist.png").convert_alpha()
playlistimg = transform.scale(playlistimg, (33, 33))
screen.blit(playlistimg, (805, 0))

# help button
helpimg = image.load("assets/help.png").convert_alpha()
helpimg = transform.scale(helpimg, (30, 30))
screen.blit(helpimg, (1167, 2))
helpmenuimg = image.load("assets/helpmenu.jpg").convert_alpha()
# help menu
isHelp = False
oneCap = False

# setting tool to "", none selected
tool = ""

# default colour black
colour = BLACK

# initialize startx and starty for line, rect, ellipse
startx, starty = 0, 0

# initialize oldmx and oldmy for prev mouse pos
oldmx, oldmy = 0, 0

# initialize fix mouse coords for draw tool
fixdrawx, fixdrawy = 0, 0

# tool thickness
thk = 5

# undo/redo variables - check if action performed and count amount
action = False
undoList, redoList = [], []

# initialize boolean for if draw should be filled
toolFill = False

# initialize variable for which stamp is chosen
currStamp = -1

# loading and blitting tools and stamps, basic UI elements
loadCount = 0
loadCount2 = 0

# initialize music text movement variables
musicTextMove = 0
musicMoveLimit = 0
musicVol = 0.3
released = False
isPlaying = False
musicText = ""
# creating music player rects and blitting
musicPlayerRect = Rect(500, 2, 250, 30)
musicSurface = Surface((250, 30))
# preset playlist
musicTrackNames = ["assets/Three Dimensional Maneuver - Attack on Titan.ogg",
                   "assets/The Reluctant Heroes - Attack on Titan.ogg",
                   "assets/Bird in a Cage - Attack on Titan.ogg"]
musicTracks = []
# tells pygame to keep track of when a track ends
MUSICEND = USEREVENT+1
mixer.music.set_endevent(MUSICEND)
playlistStart = False
# loading slightly longer .ogg files takes a bit of time apparently
loadTime = 0

# create pos surface
posRect = Rect(840, 120, 55, 43)
posSurface = Surface((56, 45))

# text
userText = ""

# rgb values
redValue = 0
greenValue = 0
blueValue = 0
# rgb values in list for changing colour tuple
colourStatusList = [0, 0, 0]

# volume viewer
volumeRect = Rect(275, 33, 110, 50)
draw.rect(screen, BLACK, volumeRect)
volumeRect2 = Rect(275, 60, 110, 20)
draw.rect(screen, BLACK, volumeRect2)
draw.rect(screen, WHITE, volumeRect2, 2)
draw.rect(screen, WHITE, Rect(275, 60, 30, 20))
volumeText = fontSmall.render("MUSIC VOLUME", True, WHITE)
screen.blit(volumeText, (275, 40))

# status bar surface
statbarSurface = Surface((438, 40))
statbarSurface.fill(BLACK)
screen.blit(statbarSurface, (400, 40))
statbarRect = (400, 40, 438, 40)
draw.rect(screen, WHITE, statbarRect, 2)

# eyedropper
isEyedropper = False

# zoom
isZoom = False

# coords
posxText, posyText = fontSmall.render("X:", True, WHITE), fontSmall.render("Y:", True, WHITE)

# typing
textTool = False

# cursors for different tools
cursorList = []
# loading cursors
for i in range(len(toolImg)):
    newCursorImg = image.load(toolImg[i])
    newCursor = cursors.Cursor((0, 38), newCursorImg)
    cursorList.append(newCursor)
# load default cursor
defaultCursorImg = image.load("assets/cursordefault.png")
defaultCursor = cursors.Cursor((0, 0), defaultCursorImg)
mouse.set_cursor(defaultCursor)  # set starting cursor to default

for i in range(190, 361, 80):  # "i" represents y-coord of img
    for j in range(25, 186, 80):  # "j" represents x-coord of img
        draw.rect(screen, GREY, (j, i, 70, 70))  # produce imgs in rows
        toolRects.append((j, i, 70, 70))

for i in range(206, 380, 80):
    for j in range(40, 200, 79):
        toolPics = image.load(toolImg[loadCount]).convert_alpha()
        screen.blit(toolPics, (j, i))  # blitting tool pictures in rects
        loadCount += 1

# loading all stamps
for j in range(280, 600, 75):
    stampbg = image.load("assets/stampbg.png")
    trnstampbg = stampbg.convert_alpha().copy()
    trnstampbg.fill((255, 255, 255, 70), None, BLEND_RGBA_MULT)
    screen.blit(trnstampbg, (j, 90))
    stampRects.append((j, 93, 65, 65))

# blitting all stamps
for j in range(280, 600, 77):
    s = transform.scale(stamps[loadCount2], (65, 65))
    screen.blit(s, (j, 93))
    loadCount2 += 1

# loading backgrounds
bgs = ["assets/bg1.png", "assets/bg2.png", "assets/bg3.png", "assets/bg4.png"]
previewLoc = [(20, 710), (145, 710), (20, 625), (145, 625)]
bgRects = [(20, 710, 115, 75), (145, 710, 115, 75), (20, 625, 115, 75), (145, 625, 115, 75)]
currBg = -1
bgList = []
bgPreviews = []
# blitting backgrounds and adding them to background list
for bg in range(len(bgs)):
    bgimg = image.load(bgs[bg])
    bgList.append(bgimg)
    preview = transform.scale(bgimg, (115, 75))
    bgPreviews.append(preview)
    screen.blit(preview, previewLoc[bg])
    draw.rect(screen, BLACK, Rect(bgRects[bg]), 3)


# function for volume
def volumeView():
    draw.rect(screen, BLACK, volumeRect2)
    draw.rect(screen, WHITE, volumeRect2, 2)
    draw.rect(screen, WHITE, Rect(275, 60, musicVol * 100, 20))


# function for thickness slider
def slider():
    global thk  # thickness and undo/redo need to be accessed
    # drawing slider rects, need 2 so the slider doesn't show outside of rect
    draw.rect(screen, BLACK, sliderRect, 0)
    draw.rect(screen, WHITE, sliderRect, 2)
    draw.rect(screen, BLACK, sliderRect2, 0)
    draw.rect(screen, WHITE, sliderRect2, 2)
    screen.blit(thicknessText, (72, 448))
    if sliderRect.collidepoint(mx, my) and mb[0]:  # check for user moving slider
        thk = mx - 25  # chancing thickness based on position of slider
        draw.rect(screen, RED, Rect(thk + 25, 440, 15, 30))  # updating new pos
    draw.rect(screen, RED, Rect(thk + 25, 440, 15, 30))  # drawing slider when not clicked


# red value slider
def redSlider():
    global redValue, colour
    draw.rect(screen, RED, redRect, 0)
    draw.rect(screen, WHITE, redRect, 2)
    draw.rect(screen, RED, redRect2, 0)
    draw.rect(screen, WHITE, redRect2, 2)
    if redRect.collidepoint(mx, my) and mb[0]:  # check for user moving slider
        redValue = mx - 25
        draw.rect(screen, WHITE, Rect(redValue + 25, 490, 15, 30))  # draw slider at new pos
        colourList = list(colour)
        colourList[0] = redValue * 1.187  # scaling x pos to rgb value
        colour = tuple(colourList)  # changing colour variable to new value
    draw.rect(screen, WHITE, Rect(redValue + 25, 490, 15, 30))  # slider resting pos


# green value slider
def greenSlider():
    global greenValue, colour
    draw.rect(screen, GREEN, greenRect, 0)
    draw.rect(screen, WHITE, greenRect, 2)
    draw.rect(screen, GREEN, greenRect2, 0)
    draw.rect(screen, WHITE, greenRect2, 2)
    if greenRect.collidepoint(mx, my) and mb[0]:
        greenValue = mx - 25
        draw.rect(screen, WHITE, Rect(greenValue + 25, 530, 15, 30))
        colourList = list(colour)
        colourList[1] = greenValue * 1.187
        colour = tuple(colourList)
    draw.rect(screen, WHITE, Rect(greenValue + 25, 530, 15, 30))


# blue value slider
def blueSlider():
    global blueValue, colour
    # drawing slider rects, need 2 so the slider doesn't show outside of rect
    draw.rect(screen, BLUE, blueRect, 0)
    draw.rect(screen, WHITE, blueRect, 2)
    draw.rect(screen, BLUE, blueRect2, 0)
    draw.rect(screen, WHITE, blueRect2, 2)
    if blueRect.collidepoint(mx, my) and mb[0]:  # check for user moving slider
        blueValue = mx - 25  # chancing value based on position of slider
        draw.rect(screen, WHITE, Rect(blueValue + 25, 570, 15, 30))
        colourList = list(colour)
        colourList[2] = blueValue * 1.187
        colour = tuple(colourList)
    draw.rect(screen, WHITE, Rect(blueValue + 25, 570, 15, 30))


# function for picking colour
def palette():
    global colour, redValue, greenValue, blueValue  # need to access colour var
    if paletteRect.collidepoint(mx, my) and mb[0]:  # checking for click on colours
        colour = screen.get_at((mx, my))  # getting colour at click pos
        # converting rgb values to pixel value for sliders
        redValue = colour[0] / 1.186
        greenValue = colour[1] / 1.186
        blueValue = colour[2] / 1.186
    # drawing colour preview
    draw.rect(screen, colour, currColRect, 0)
    draw.rect(screen, WHITE, currColRect2, 2)


# function for pencil tool - thickness of 1
def pencil():
    draw.line(screen, colour, (oldmx, oldmy), (mx, my), 1)  # draw from prev mouse pos to current
    draw.circle(screen, colour, (mx, my), 1)  # draw circle to make line look nicer


# function for brush tool - thickness changes
def brush(thickness):
    # drawn when difference in oldpos and newpos not enough for fix to be used
    draw.line(screen, colour, (oldmx, oldmy), (mx, my), thickness)
    draw.circle(screen, colour, (mx, my), thickness)


# function for eraser tool
def eraser(x):
    # replacing canvas with subsurface of background to not erase bg
    if currBg != -1 and 275 + x // 2 < mx < 1175 - x // 2 and 195 + x // 2 < my < 780 - x // 2:
        screen.blit(bgList[currBg].subsurface(Rect(mx-275-x//2, my-195-x//2, x, x)).copy(), (mx-x//2, my-x//2))
    # drawing white line and circle to "erase" contents of screen when no bg applied
    elif currBg == -1:
        draw.line(screen, WHITE, (oldmx, oldmy), (mx, my), x)
        draw.circle(screen, WHITE, (mx, my), x // 2)


# function for line tool
def line(sx, sy, thickness):
    screen.blit(screenCap, (275, 195))  # blitting screen capture on canvas
    draw.line(screen, colour, (sx, sy), (mx, my), thickness)  # drawing line from mb down pos to current


# function for fill tool
def fill():
    screen.subsurface(canvasRect).fill(colour)  # fill canvas with selected colour


# function for rect tool
def rect(sx, sy, thickness, isFilled):
    rectKeys = key.get_pressed()
    screen.blit(screenCap, (275, 195))  # blitting screen capture on canvas
    if rectKeys[K_LSHIFT]:
        rectRect = Rect(sx, sy, (mx - sx), (mx - sx))  # blitting rect at new mouse pos
    else:
        rectRect = Rect(sx, sy, (mx - sx), (my - sy))  # blitting rect at new mouse pos
    rectRect.normalize()  # normalize rect to get rid of negative values
    draw.rect(screen, colour, rectRect, 0 if isFilled else thickness)  # blitting rect


# function for ellipse tool
def ellipse(sx, sy, isFilled, thickness):
    ellipseKey = key.get_pressed()
    screen.blit(screenCap, (275, 195))  # blitting screen capture on canvas
    if ellipseKey[K_LSHIFT]:
        circleRect = Rect(sx, sy, mx - sx, mx - sx)  # creating rect for ellipse tool
    else:
        circleRect = Rect(sx, sy, mx - sx, my - sy)  # creating rect for ellipse tool
    circleRect.normalize()  # normalizing rect
    draw.ellipse(screen, colour, circleRect, 0 if isFilled else thickness)  # draw ellipse


# function for saving canvas
def saveTool():
    fileName = filedialog.asksaveasfilename(defaultextension=".png")  # getting filename of img
    if not fileName:  # ensuring user actually typed filename
        return 0
    else:
        image.save(screen.subsurface(canvasRect), fileName)  # saving file


# function for loading image to canvas
def loadTool():
    fileName = filedialog.askopenfilename()  # asking for file select
    if fileName:  # ensuring file isn't none
        loadedimg = image.load(fileName)  # loading img
        imgx, imgy = loadedimg.get_width(), loadedimg.get_height()  # grabbing dimensions
        aspectRatio = loadedimg.get_width() / loadedimg.get_height()  # finding aspect ratio
        if imgx > 900:  # resize if length too big
            imgx, imgy = 900, 900 / aspectRatio
            loadedimg = transform.scale(loadedimg, (imgx, imgy))
        if imgy > 585:  # resize if width too big
            loadedimg = transform.scale(loadedimg, (585 * aspectRatio, 585))
        screen.blit(loadedimg, (275, 195))  # blit final image after resizing


# function to draw stamps
def createStamp(num):
    global currStamp, stampSize  # access current stamp and size of stamp
    screen.blit(screenCap, (275, 195))  # ensure stamp doesn't blit all over screen
    screen.set_clip(canvasRect)  # only allow stamps in canvas
    if currStamp == 5 and canvasRect.collidepoint(mx, my):  # checking for stamp being users stamp
        scaledUserStamp = transform.scale(userStamp, (stampSize, stampSize))  # scaling it in case too big
        screen.blit(scaledUserStamp, (mx - 40, my - 40))  # blit where cursor is
    elif canvasRect.collidepoint(mx, my):  # normal preset stamp
        scaledStamp = transform.scale(stamps[num], (stampSize, stampSize))
        screen.blit(scaledStamp, (mx - 40, my - 40))  # blitting on cursor


# function for music player
def musicPlayer():
    # accessing music text info, clicks, and other music info
    global musicTextMove, musicText, musicMoveLimit, released,\
        isPlaying, musicVol, playlistStart, loadTime
    # drawing music player
    screen.blit(musicSurface, (500, 2))
    screen.blit(pauseplayimg, (755, 4))
    draw.rect(screen, WHITE, musicPlayerRect, 2)
    musicSurface.blit(musicCap, (0, 0))

    if musicRect.collidepoint(mx, my) and released:  # user wants to open music file
        musicName = filedialog.askopenfilename()
        released = False
        if musicName:  # if user gives file, do the following:
            isPlaying = True
            # loading and playing imported music
            mixer.music.load(musicName)
            mixer.music.set_volume(musicVol)
            mixer.music.play()
            # find title and use av. pixels/character to find amount needed to scroll through
            fileCutoff = musicName.rindex("/")
            musicName = musicName[fileCutoff + 1:len(musicName) - 4]
            musicMoveLimit = int(20 + len(musicName) * 8.7 - 250)
            musicText = fontSmall.render(musicName, True, WHITE)
    elif musicText != "":
        # blitting text onto music display surface
        musicSurface.blit(musicText, (15 - musicTextMove, 7))
        if isPlaying and playlistStart == False:
            musicTextMove += 0.04  # always moving when music is playing and not paused
        elif playlistStart:
            musicTextMove = 0
        if musicTextMove > musicMoveLimit:  # reset movement when reach end of text
            musicTextMove = 0

    if playlistRect.collidepoint(mx, my) and mb[0]:  # playing from aot playlist
        released = False
        playlistStart = True
        for k in range(len(musicTrackNames)):  # loading all songs and playing first song
            musicTracks.append(mixer.music.load(musicTrackNames[k]))
            mixer.music.play()
            isPlaying = True
            loadTime = 0
    elif playlistStart:  # loading and playlist text
        if loadTime < 2500:
            musicText = fontSmall.render("LOADING...", True, WHITE)
            loadTime += 1
        else:
            musicText = fontSmall.render("Attack on Titan - Playlist", True, WHITE)


# displaying coordinates of cursor relative to canvas
def displayCoords():
    global posxText, posyText  # accessing the coordinate text
    screen.blit(posSurface, (840, 120))  # blitting coordinate display surface
    draw.rect(screen, WHITE, posRect, 1)
    # update coords when on canvas
    if canvasRect.collidepoint(mx, my):
        posxText = fontSmall.render("X: " + str(mx-275), True, WHITE)
        posyText = fontSmall.render("Y: " + str(my-195), True, WHITE)
    screen.blit(posxText, (844, 124))
    screen.blit(posyText, (844, 144))


# function for text tool
def typeText(text):
    global textTool  # access boolean for if text tool is selected; input not taken when tool not selected
    screen.blit(screenCap, (275, 195))
    screen.set_clip(canvasRect)
    textTool = True
    # blitting text with colour and at cursor pos
    if text != "":
        screen.set_clip(canvasRect)
        uText = fontMed.render(text, True, colour)
        screen.blit(uText, (mx + 40, my - 20))


# distance between prev coords and current coords (fix for pencil tool)
def distance(prevX, prevY, currX, currY):  # take old and new pos
    return sqrt((prevX - currX) ** 2 + (prevY - currY) ** 2)  # return dist between pos


# functions for confirmation when clearing canvas and exiting
def confirmClear():
    ans = askyesno(title="Clear Canvas", message="Confirm Clear?")  # using askyesno module
    if ans:  # if answer is True, function returns true to signify user confirmation
        return True


def confirmQuit():
    ans = askyesno(title="Quit AOT Paint", message="Confirm Quit?")  # giving title and msg
    if ans:  # if answer is True, function returns true to signify user confirmation
        return True


# function for status bar that displays basic program info
def statusBar(currTool):
    global colourStatusList  # accessing list that stores colour values and replaces unmutable tuple
    # blit status bar surface and divider lines
    screen.blit(statbarSurface, (400, 40))
    draw.rect(screen, WHITE, statbarRect, 2)
    draw.line(screen, WHITE, (491, 40), (491, 78))
    draw.line(screen, WHITE, (605, 40), (605, 78))
    draw.line(screen, WHITE, (765, 40), (765, 78))
    # making tool name of any stamp (stamp1, stamp2, stamp3, etc) equal to "stamp"
    if "stamp" in currTool:
        currTool = "stamp"
    # blitting text: current tool, thickness, rgb values, and if tools are filled
    currToolText = fontSmall.render("Tool: " + str(currTool), True, WHITE)
    screen.blit(currToolText, (404, 53))
    currThkText = fontSmall.render("Thickness: " + str(thk), True, WHITE)
    screen.blit(currThkText, (496, 53))
    for rgb in range(3):
        colourStatusList[rgb] = int(colour[rgb])
    currRGBText = fontSmall.render("RGB: " + str(colourStatusList), True, WHITE)
    screen.blit(currRGBText, (612, 53))
    if toolFill:
        toolFillTemp = "ON"
    else:
        toolFillTemp = "OFF"
    currIsFill = fontSmall.render("Fill: " + str(toolFillTemp), True, WHITE)
    screen.blit(currIsFill, (775, 53))


def eyedropper():
    global colour, redValue, greenValue, blueValue  # need to access colour var
    if canvasRect.collidepoint(mx, my) and mb[0]:  # checking for click on colours
        colour = screen.get_at((mx, my))  # getting colour at click pos
        # adjusting rgb values according to pixels vs rgb values (210 vs 250)
        redValue = colour[0] / 1.186
        greenValue = colour[1] / 1.186
        blueValue = colour[2] / 1.186
        return True
    # drawing colour preview
    draw.rect(screen, colour, currColRect, 0)
    draw.rect(screen, WHITE, currColRect2, 2)


# zoom in tool
def zoomTool():
    global actionCap  # access actionCap for undo purposes
    # zoom in on mx my
    if mb[0] and canvasRect.collidepoint(mx, my):
        # don't allow bigger canvas to get onto entire screen
        screen.set_clip(canvasRect)
        zoomedCanvas = transform.scale(screen.subsurface(canvasRect), (1800, 1350))  # transform 1.5x original size
        screen.blit(zoomedCanvas, (550-mx, 350-my))  # blitting in relation to mx, my
        actionCap = screen.subsurface(canvasRect).copy()
        undoList.append(actionCap)
        return True


screenCap = screen.subsurface(canvasRect).copy()  # taking first screen capture for tools
musicCap = musicSurface.copy()  # music text capture

# screencapture of blank screen for undo/redo
actionCap = screen.subsurface(canvasRect).copy()
undoList.append(actionCap)

running = True
while running:
    mx, my = mouse.get_pos()  # getting the current mx and my
    displayCoords()  # displaying coords based on curr mx my
    mb = mouse.get_pressed()  # mouse button pressed
    for evt in event.get():  # handling events
        if evt.type == QUIT:  # handling quit
            if confirmQuit():
                running = False

        # handling when a music track ends and in playlist
        if evt.type == MUSICEND and playlistStart:
            if len(musicTracks) > 0:  # making sure there are songs in list
                mixer.music.queue(musicTracks.pop())  # queueing last song in list with pop()

        # recieving text when textTool is true
        if evt.type == KEYDOWN and textTool:
            if evt.key == K_BACKSPACE:  # slicing string is backspace
                userText = userText[:-1]
            elif evt.key == K_RETURN:  # saving string on screen
                actionCap = screen.subsurface(canvasRect).copy()
                undoList.append(actionCap)
                userText = ""
                tool = ""
                mouse.set_cursor(defaultCursor)
            elif evt.key == K_ESCAPE:  # resetting string
                userText = ""
            elif evt.key == K_TAB:  # manual tab because input doesnt support
                userText += "   "
            else:  # take normal keyboard input
                userText += evt.unicode

        # handling mouse button down events
        if evt.type == MOUSEBUTTONDOWN:
            startx, starty = evt.pos  # taking start coords of moues button down for tools like line

            # checking for stamp selected, preset or user
            for i in range(5):
                if Rect(stampRects[i]).collidepoint(mx, my):
                    currStamp = i
            if Rect(685, 95, 60, 60).collidepoint(mx, my) and isUserStamp:
                currStamp = 5

        # handling mouse button up events
        if evt.type == MOUSEBUTTONUP:

            # for use outside of event loop
            released = True

            # checking for eyedropper tool selection; if selected, signify with tool and boolean
            if eyedropperRect.collidepoint(mx, my):
                isEyedropper = True
                tool = "col sel"

            # checking for zoom tool selection; if selected, signify with tool and boolean
            if zoomRect.collidepoint(mx, my):
                isZoom = True
                tool = "zoom"

            # checking for help menu selection; if selected, signify with boolean
            # if already seelcted, deselect and blit screen before help menu
            if isHelp:
                screen.blit(prevHelp, (0, 0))
                isHelp = False
            if helpRect.collidepoint(mx, my) and isHelp == False:
                isHelp = True
                oneCap = True
                tool = ""

            # backgrounds; checking for selection
            for i in range(len(bgs)):
                if Rect(bgRects[i]).collidepoint(mx, my):
                    currBg = i
                    screen.blit(bgList[i], (275, 195))  # if selected, blit onto canvas
                    action = True

            # checking for pausing or playing of music; also must be playing a track
            if pauseplayRect.collidepoint(mx, my) and musicText != "":
                # checking for whether music is paused or playing and reverting states
                if not isPlaying:
                    mixer.music.unpause()
                    isPlaying = True
                else:
                    mixer.music.pause()
                    isPlaying = False

            # checking for user clicking volume up
            if volupRect.collidepoint(mx, my) and (musicVol <= 1):
                musicVol += 0.1  # raising music volume
                mixer.music.set_volume(musicVol)  # setting new volume
                volumeView()  # updating volume viewer

            # checking for user clicking volume down
            if voldownRect.collidepoint(mx, my) and (musicVol >= 0):
                musicVol -= 0.1  # decrease music volume
                mixer.music.set_volume(musicVol)  # setting new volume
                volumeView()  # updating volume viewer

            # checking for user importing stamp
            if addStampRect.collidepoint(mx, my):
                stampName = filedialog.askopenfilename()  # opening file explorer
                if stampName:  # make sure filename not empty
                    isUserStamp = True
                    # load and blit preview stamp
                    userStamp = image.load(stampName)
                    userStampIcon = transform.scale(userStamp, (60, 60))
                    draw.rect(screen, BLACK, Rect(680, 95, 60, 60))
                    screen.blit(userStampIcon, (680, 95))

            # checking for saving canvas
            if saveRect.collidepoint(mx, my):
                saveTool()

            # checking for loading image
            if loadRect.collidepoint(mx, my):
                loadTool()

            # checking for fill selection/deselection
            if fillRect.collidepoint(mx, my):
                # set fill to true if false and vice versa
                if toolFill:
                    toolFill = False
                else:
                    toolFill = True

            # checking for undo
            if undoRect.collidepoint(mx, my):
                # make sure there are still captures left to undo
                if len(undoList) > 1:
                    # taking last captured action, deleting from list and appending to redo side
                    undoCap = undoList.pop()
                    redoList.append(undoCap)
                    # blitting undo capture
                    screen.blit(undoList[-1], (275, 195))
                else:
                    # fill white when at last capture
                    screen.subsurface(canvasRect).fill(WHITE)
                tool = ""  # reset tool
            # checking for redo
            if redoRect.collidepoint(mx, my):
                # make sure still items in redo list
                if len(redoList) > 0:
                    # same process as undo but appending to undolist and popping from redolist
                    redoCap = redoList.pop()
                    undoList.append(redoCap)
                    screen.blit(undoList[-1], (275, 195))
                tool = ""
            # resetting redolist when action performed
            if len(redoList) > 0 and canvasRect.collidepoint(mx, my) and mb[0]:
                redoList = []
            # checking if canvas capture is needed and resetting action to false
            if action and tool != "":
                actionCap = screen.subsurface(canvasRect).copy()
                undoList.append(actionCap)
                action = False

            # taking capture
            screenCap = screen.subsurface(canvasRect).copy()

        # cycling and checking if tool is selected
        for i in range(len(toolNames)):
            # update rect colour if hovering or tool selected
            if Rect(toolRects[i]).collidepoint(mx, my) or tool == toolNames[i]:
                if "stamp" not in toolNames[i]:  # stamps not "part" of tools so excluded from highlighting
                    draw.rect(screen, RED, toolRects[i], 2)
                    # checking for tool selection
                    if canvasRect.collidepoint(mx, my):
                        # setting cursor upon entering canvas with certain tool
                        if toolNames[i] == "rect" or toolNames[i] == "ellipse":
                            mouse.set_cursor(defaultCursor)
                        else:
                            mouse.set_cursor(cursorList[i-6])
                    else:
                        mouse.set_cursor(defaultCursor)
                # setting tool to selected tool or unselecting tool
                if evt.type == MOUSEBUTTONUP and Rect(toolRects[i]).collidepoint(mx, my):
                    if tool == toolNames[i]:
                        tool = ""  # unselect tool
                    else:
                        if isEyedropper:  # eyedropper not included in traditional tools
                            isEyedropper = False
                        tool = toolNames[i]  # select tool
            # drawing default unselected colour for tools
            elif "stamp" not in toolNames[i]:
                draw.rect(screen, GREEN, toolRects[i], 2)

    # thickness slider
    slider()
    # rgb value sliders
    redSlider()
    greenSlider()
    blueSlider()
    # colour selection palette
    palette()
    # music player
    musicPlayer()
    # view program info
    statusBar(tool)

    # creating stamps
    if "stamp" in tool:
        createStamp(currStamp)

    # help menu when user select help
    if isHelp:
        if oneCap:
            prevHelp = screen.copy()  # taking cap of screen before help menu
        screen.blit(helpmenuimg, (0, 0))  # blit help menu
        oneCap = False

    if isEyedropper:  # checking for eyedropper tool active
        if eyedropper():  # until eyedropper returns true continue having tool as eyedropper
            isEyedropper = False
            tool = ""

    if isZoom:  # similar strucutre to eyedropper, but with zoom tool
        if zoomTool():  # the following happens upon clicking, which has isZoom returns true
            isZoom = False
            tool = ""

    # checking for user clear canvas, and ask for confirmation
    if evt.type == MOUSEBUTTONUP and tool == "clear" and canvasRect.collidepoint(mx, my):
        if confirmClear():
            screen.subsurface(canvasRect).fill(WHITE)
            currBg = -1  # resetting bg to none
        released = False

    # use tools
    if canvasRect.collidepoint(mx, my):
        screen.set_clip(canvasRect)  # only allow changes in canvas
        if mb[0]:
            if tool == "pencil":  # pencil drawing
                pencil()
                # fix to fill in undrawn parts
                dx = mx - oldmx
                dy = my - oldmy
                apartDist = int(distance(oldmx, oldmy, mx, my))

                # iterating through all points that need to be drawn
                for i in range(1, apartDist):
                    # coords of next fix coords
                    fixdrawx = dx * i / apartDist + oldmx
                    fixdrawy = dy * i / apartDist + oldmy
                    draw.circle(screen, colour, (int(fixdrawx), int(fixdrawy)), 1)  # drawing circle
            if tool == "brush":
                # same fix as pencil tool, except accounting to thickness
                brush(thk)
                dx = mx - oldmx
                dy = my - oldmy
                apartDist = int(distance(oldmx, oldmy, mx, my))

                for i in range(1, apartDist):
                    fixdrawx = dx * i / apartDist + oldmx
                    fixdrawy = dy * i / apartDist + oldmy
                    draw.circle(screen, colour, (int(fixdrawx), int(fixdrawy)), thk)
            if tool == "eraser":
                eraser(thk)  # using eraser function
            if tool == "line":
                line(startx, starty, thk)  # drawing line with starting pos and thickness
            if tool == "fill":
                fill()  # fill screen function
            if tool == "rect":
                rect(startx, starty, thk, toolFill)  # drawing rect
            if tool == "ellipse":
                ellipse(startx, starty, toolFill, thk)  # drawing ellipse
        if tool == "text":
            typeText(userText)  # typing text
        if tool != "":
            action = True  # action occured when tool is selected

    # oldmx my for drawing fix
    oldmx, oldmy = mx, my

    # updating display
    display.flip()

    # setting pixel editing area back to entire screen
    screen.set_clip(None)

    # resetting released (clicked) variable
    released = False

quit()
