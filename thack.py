from pathlib import Path
import time
# from tkinter import *
# Explicit imports to satisfy Flake8
from cmu_112_graphics import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hugom\Documents\School Work\THack\build\assets\frame0")

class Bet: #The actual like big question thing for everyone
    def __init__(self, title, op1, op2, expires, tags, result = None):
        self.title = title #question
        self.options = (op1, op2) #two options
        self.expires = expires #end date
        self.tags = tags # list of related tags
        self.op1 = op1
        self.op2 = op2
        self.bets1 = [] #option 1 
        self.numb1 = 0
        self.bets2 = [] #option 2 bets
        self.numb2 = 0
        self.numBets = len(self.bets1) + len(self.bets2) # fix
        self.result = result
    

    def closeBet(self, outcome):
        pot = self.numBets * 0.1
        if outcome == 1:
            winners = self.bets1
            losers = self.bets2
        else:
            winners = self.bets2
            losers = self.bets1
        winnings = pot / (len(winners)) #fix
        for wager in winners: #1 is profile 2 is wager
            wager[1].balance += winnings
            wager[1].netEarnings += winnings
            wager[2].result = True
        for wager in losers:
            wager[2].result = False

class Wager: #individual bets placed by players
    def __init__(self, title, vote, quantity, bet):
        self.title = title
        self.vote = vote
        self.quantity = quantity
        self.bet = bet

class Profile: #person's account
    def __init__(self, username):
        self.username = username
        self.balance = 0
        self.posts = []
        self.current = []
        self.history = []
        self.wins = []
        self.losses = []
        self.accuracy = 0
        self.netEarnings = 0
    
    def makeNewBet(self, title, op1, op2, expires, tags, app):
        bet = Bet(title, op1, op2, expires, tags)
        self.posts.append(bet)
        app.allBets.append(bet)

    def makeWager(self, bet, quantity, vote, app): 
        #Place (quantity) wagers, returns T if wager goes through F otherwise
        wager = Wager(bet.title, quantity, vote, bet)
        app.hugom.current.append(wager)
        cost = 0.1 * quantity
        if cost > self.balance:
            return False
        self.current.append(wager)
        for x in range(quantity):
            if vote == 1:
                bet.bets1.append((self, wager))
            else:
                bet.bets2.append((self, wager))
        return True

    def updtBalance(self, amount):
        self.balance += amount
        print(self.balance)

    def updtCurrWagers(self):
        for wager in self.current:
            if wager.bet.result != None:
                if wager.vote == wager.bet.result:
                    self.wins.append(wager)
                    self.netEarnings += 1
                else:
                    self.losses.append(wager)
                self.current.remove(wager)
                self.history.append(wager.bet)

    def updtAccuracy(self):
        self.accuracy = (len(self.wins)/len(self.history))*100 if len(self.history)!=0 else 0

def appStarted(app):
    app.hugom = Profile("Hugo.martinezzz")
    app.mode = 'home'
    app.home_setting = 'FYP'
    app.isqclicked = False
    app.isop1clicked = False
    app.isop2clicked = False
    app.ishrclicked = False
    app.isminclicked = False
    app.previewQ = ''
    app.previewOp1 = ''
    app.previewOp2 = ''
    app.previewHr = ''
    app.previewMin = ''
    app.allBets = []
    app.betIndex = 0
    bet1 = Bet('Who will win the Superbowl?', 'Chiefs', 'Eagles', 100, None)
    bet2 = Bet('Will we win the Hackathon?', 'Yes', 'No :(', 100, None)
    bet3 = Bet('When will Eric wake up today?', 'Before 10 AM', 'After 10 AM', 0, None, True)
    app.allBets.append(bet1)
    app.allBets.append(bet2)
    app.allBets.append(bet3)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\hugom\Documents\School Work\THack\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

##helper
def clickIn(cx, cy, x1, y1, x2, y2):
    if cx > x1 and cx < x2:
        if cy > y1 and cy < y2:
            return True
    return False

#hi hugo
# #Home screen
def home_mousePressed(app, event):
    x = event.x
    y = event.y
    if clickIn(x, y, 297.0, 18.0, 380.0, 61.0,):
        app.hugom.balance += 1
    if clickIn(x, y, 117.0, 18.0, 273.0, 61.0,):
        if app.home_setting == 'FYP':
            app.home_setting = 'Friends'
        else:
            app.home_setting = 'FYP'

    if clickIn(x, y, 0, 745, 77, 800): #home
        app.mode = 'home'
    if clickIn(x, y, 78, 745, 156, 800): #current bets
        app.mode = 'currBets'
    if clickIn(x, y, 157, 745, 226, 800): #post
        app.mode = 'makePost'
    if clickIn(x, y, 227, 745, 305, 800): #leaderboard
        app.mode = 'leaderb'
    if clickIn(x, y, 306, 745, 390, 800): #profile
        app.mode = 'profPage'

def home_keyPressed(app, event):
    if len(app.allBets) != 0:
        if event.key == "Up":
            app.betIndex -= 1
            if app.betIndex < 0:
                app.betIndex = len(app.allBets) - 1
        if event.key == "Down":
            app.betIndex += 1
            if app.betIndex >= len(app.allBets):
                app.betIndex = 0
        if event.key == "Left":
            app.hugom.makeWager(app.allBets[app.betIndex], 1, 1, app)
            app.allBets.pop(app.betIndex)
            app.betIndex += 1
            if app.betIndex >= len(app.allBets):
                app.betIndex = 0
        if event.key == "Right":
            app.hugom.makeWager(app.allBets[app.betIndex], 1, 2, app)
            app.allBets.pop(app.betIndex)
            app.betIndex += 1
            if app.betIndex >= len(app.allBets):
                app.betIndex = 0
def home_redrawAll(app, canvas):
    canvas.create_rectangle(
        0.0,
        711.0,
        390.0,
        798.0,
        fill="#B6B6B6",
        outline="")

    canvas.create_rectangle(
        0.0,
        79.0,
        390.0,
        711.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_image(117, 18, image = ImageTk.PhotoImage(
        file=relative_to_assets("button_1.png")), anchor='nw')

    canvas.create_image(297, 18, image = ImageTk.PhotoImage(
        file=relative_to_assets("button_2.png")), anchor='nw')
    
    canvas.create_image(10, 18, image = ImageTk.PhotoImage(
        file=relative_to_assets("button_3.png")), anchor='nw')

    if len(app.allBets) == 0:
        question = 'No Bets Available'
        options = ':('
    else:
        question = app.allBets[app.betIndex].title
        options = f'{app.allBets[app.betIndex].op1}                 {app.allBets[app.betIndex].op2}'
    #Current Bet Info:
    canvas.create_text(
        390/2,
        158.0,
        anchor="c",
        text= question,
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text( #options
        390/2,
        400.0,
        anchor="c",
        text= options,
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        28.0,
        745.0,
        anchor="nw",
        text="Home",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        745.0,
        anchor="nw",
        text="Current Bets",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        319.0,
        745.0,
        anchor="nw",
        text="Profile",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        182.0,
        745.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        227.0,
        745.0,
        anchor="nw",
        text="Leaderboard",
        fill="#000000",
        font=("Inter", 12 * -1)
    )
#Current Bets Screen
def currBets_mousePressed(app, event):
    x = event.x
    y = event.y
    if clickIn(x, y, 0, 745, 77, 800): #home
        app.mode = 'home'
    if clickIn(x, y, 78, 745, 156, 800): #current bets
        app.mode = 'currBets'
    if clickIn(x, y, 157, 745, 226, 800): #post
        app.mode = 'makePost'
    if clickIn(x, y, 227, 745, 305, 800): #leaderboard
        app.mode = 'leaderb'
    if clickIn(x, y, 306, 745, 390, 800): #profile
        app.mode = 'profPage'
    if clickIn(x, y, 250.0, 240.0, 370.0, 267.0):
        app.hugom.updtCurrWagers()
        app.hugom.updtAccuracy()

def currBets_redrawAll(app, canvas):
    canvas.create_rectangle(
        0.0,
        217.0,
        390.0,
        711.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        37.0,
        37.0,
        80.0,
        80.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        10.0,
        104.0,
        66.0,
        199.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        65.0,
        104.0,
        121.0,
        199.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        140.0,
        104.0,
        196.0,
        199.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        215.0,
        104.0,
        271.0,
        199.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        290.0,
        104.0,
        346.0,
        199.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        19.0,
        291.0,
        369.0,
        393.0,
        fill="#FFFFFF",
        outline="")
    if len(app.hugom.current) > 0:
        canvas.create_text(19, 292, anchor = 'nw', text = app.hugom.current[0].title,
                                    font = ("Inter", 12 * -1))
        canvas.create_text(19, 322, anchor = 'nw', text = f'Expires in {app.hugom.current[0].bet.expires} minutes',
                                    font = ("Inter", 12 * -1))
        if app.hugom.current[0].vote == 1:
            backing = app.hugom.current[0].bet.op1
        else:
            backing = app.hugom.current[0].bet.op2
        canvas.create_text(19, 352, anchor = 'nw', text = f"You're betting on: {backing}",
                                    font = ("Inter", 12 * -1))
    canvas.create_rectangle(
        250.0,
        240.0,
        370.0,
        267.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        20.0,
        240.0,
        240.0,
        267.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle(
        19.0,
        409.0,
        369.0,
        511.0,
        fill="#FFFFFF",
        outline="")
    if len(app.hugom.current) > 1:
        canvas.create_text(19, 409, anchor = 'nw', text = app.hugom.current[1].title,
                                    font = ("Inter", 12 * -1))
        canvas.create_text(19, 440, anchor = 'nw', text = f'Expires in {app.hugom.current[1].bet.expires} minutes',
                                    font = ("Inter", 12 * -1))
        if app.hugom.current[1].vote == 1:
            backing = app.hugom.current[1].bet.op1
        else:
            backing = app.hugom.current[1].bet.op2
        canvas.create_text(19, 470, anchor = 'nw', text = f"You're betting on: {backing}",
                                    font = ("Inter", 12 * -1))
    canvas.create_rectangle(
        19.0,
        527.0,
        369.0,
        629.0,
        fill="#FFFFFF",
        outline="")
    if len(app.hugom.current) > 2:
        canvas.create_text(19, 527, anchor = 'nw', text = app.hugom.current[2].title,
                                    font = ("Inter", 12 * -1))
        canvas.create_text(19, 560, anchor = 'nw', text = f'Expires in {app.hugom.current[2].bet.expires} minutes',
                                    font = ("Inter", 12 * -1))
        if app.hugom.current[2].vote == 1:
            backing = app.hugom.current[2].bet.op1
        else:
            backing = app.hugom.current[2].bet.op2
        canvas.create_text(19, 590, anchor = 'nw', text = f"You're betting on: {backing}",
                                    font = ("Inter", 12 * -1))
    canvas.create_rectangle(
        20.0,
        645.0,
        370.0,
        711.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        264.0,
        50.0,
        anchor="nw",
        text="January 20 2073",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        285.0,
        246.0,
        anchor="nw",
        text="Claim All",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        83.0,
        246.0,
        anchor="nw",
        text="View Preference",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle(
        219.0,
        246.0,
        234.0,
        261.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        0.0,
        711.0,
        390.0,
        798.0,
        fill="#B6B6B6",
        outline="")

    canvas.create_text(
        28.0,
        745.0,
        anchor="nw",
        text="Home",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        745.0,
        anchor="nw",
        text="Current Bets",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        319.0,
        745.0,
        anchor="nw",
        text="Profile",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        182.0,
        745.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        227.0,
        745.0,
        anchor="nw",
        text="Leaderboard",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

#Main Post Screen
def makePost_mousePressed(app, event):
    x = event.x
    y = event.y
    if clickIn(x, y, 48.0, 515.0, 341.0, 556.0):
        app.isqclicked = True
        app.isop1clicked = False
        app.isop2clicked = False
        app.ishrclicked = False
        app.isminclicked = False
    if clickIn(x, y, 48.0, 583.0, 341.0, 624.0):
        app.isop1clicked = True
        app.isqclicked = False
        app.isop2clicked = False
        app.ishrclicked = False
        app.isminclicked = False
    if clickIn(x, y, 48.0, 657.0, 341.0, 698.0):
        app.isop2clicked = True
        app.isqclicked = False
        app.isop1clicked = False
        app.ishrclicked = False
        app.isminclicked = False
    if clickIn(x, y, 48.0, 731.0, 182.0, 772.0):
        app.ishrclicked = True
        app.isqclicked = False
        app.isop1clicked = False
        app.isop2clicked = False
        app.isminclicked = False
    if clickIn(x, y, 207.0, 731.0, 341.0, 772.0):
        app.isminclicked = True
        app.isqclicked = False
        app.isop1clicked = False
        app.isop2clicked = False
        app.ishrclicked = False
    if clickIn(x, y, 293.0, 43.0, 330, 55):
        expires = int(app.previewHr)*60 + int(app.previewMin)
        print(app.hugom.posts)
        app.hugom.makeNewBet(app.previewQ, app.previewOp1, app.previewOp2, expires, None, app)
        print(app.hugom.posts)
        app.previewQ = ''
        app.previewOp1 = ''
        app.previewOp2 = ''
        app.previewHr = ''
        app.previewMin = ''
        app.mode = 'profPage'
    if clickIn(x, y, 10, 25, 40, 55):
        app.mode = 'home'

def makePost_keyPressed(app, event):
    if app.isqclicked == True:
        if event.key == 'Enter':
            app.isqclicked = False
            app.isop1clicked = True
        elif event.key == 'Space':
            app.previewQ += ' '
        elif event.key == 'Backspace':
            app.previewQ = app.previewQ[:-1]
        else:
            app.previewQ += event.key
    
    elif app.isop1clicked == True:
        if event.key == 'Enter':
            app.isop1clicked = False
            app.isop2clicked = True
        elif event.key == 'Space':
            app.previewOp1 += ' '
        elif event.key == 'Backspace':
            app.previewOp1 = app.previewOp1[:-1]
        else:
            app.previewOp1 += event.key

    elif app.isop2clicked == True:
        if event.key == 'Enter':
            app.isop2clicked = False
            app.ishrclicked = True
        elif event.key == 'Space':
            app.previewOp2 += ' '
        elif event.key == 'Backspace':
            app.previewOp2 = app.previewOp2[:-1]
        else:
            app.previewOp2 += event.key

    elif app.ishrclicked == True:
        if event.key == 'Enter':
            app.ishrclicked = False
            app.isminclicked = True
        elif event.key == 'Space':
            app.previewHr += ' '
        elif event.key == 'Backspace':
            app.previewHr = app.previewHr[:-1]
        else:
            app.previewHr += event.key

    elif app.isminclicked == True:
        if event.key == 'Enter':
            app.isminclicked = False
        elif event.key == 'Space':
            app.previewMin += ' '
        elif event.key == 'Backspace':
            app.previewMin = app.previewMin[:-1]
        else:
            app.previewMin += event.key

def makePost_redrawAll(app, canvas):
    canvas.create_rectangle(
        282.0,
        36.0,
        363.0,
        68.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        14.0,
        27.0,
        anchor="nw",
        text="x",
        fill="#000000",
        font=("Inter", 36 * -1)
    )

    canvas.create_text(
        305.0,
        43.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_rectangle(
        72.0,
        89.0,
        317.0,
        485.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        72.0,
        382.0,
        317.0,
        485.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_rectangle( #Question
        48.0,
        515.0,
        341.0,
        556.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(48, 515, anchor = 'nw', text = app.previewQ, font = ("Inter", 12 * -1))
    canvas.create_rectangle( #Choice 1
        48.0,
        583.0,
        341.0,
        624.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(48, 583, anchor = 'nw', text = app.previewOp1, font = ("Inter", 12 * -1))
    canvas.create_rectangle( #Choice 2
        48.0,
        657.0,
        341.0,
        698.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(48, 657, anchor = 'nw', text = app.previewOp2, font = ("Inter", 12 * -1))
    canvas.create_text(
        48.0,
        495.0,
        anchor="nw",
        text="Question",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        48.0,
        563.0,
        anchor="nw",
        text="Choice 1",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        48.0,
        637.0,
        anchor="nw",
        text="Choice 2",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle( #exp hr
        48.0,
        731.0,
        182.0,
        772.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle( #exp min
        207.0,
        731.0,
        341.0,
        772.0,
        fill="#D9D9D9",
        outline="")
    canvas.create_text(48, 731, anchor = 'nw', text = app.previewHr, font = ("Inter", 12 * -1))
    canvas.create_text(
        48.0,
        711.0,
        anchor="nw",
        text="Expire Hour",
        fill="#000000",
        font=("Inter", 12 * -1)
    )
    canvas.create_text(207, 731, anchor = 'nw', text = app.previewMin, font = ("Inter", 12 * -1))
    canvas.create_text(
        207.0,
        711.0,
        anchor="nw",
        text="Expire Minute",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

#Leaderboard screen
def leaderb_mousePressed(app, event):
    x = event.x
    y = event.y
    if clickIn(x, y, 0, 745, 77, 800): #home
        app.mode = 'home'
    if clickIn(x, y, 78, 745, 156, 800): #current bets
        app.mode = 'currBets'
    if clickIn(x, y, 157, 745, 226, 800): #post
        app.mode = 'makePost'
    if clickIn(x, y, 227, 745, 305, 800): #leaderboard
        app.mode = 'leaderb'
    if clickIn(x, y, 306, 745, 390, 800): #profile
        app.mode = 'profPage'

def leaderb_redrawAll(app, canvas):
    canvas.create_rectangle(
        52.0,
        56.0,
        337.0,
        99.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        53.0,
        70.0,
        anchor="nw",
        text="Friends | International | National",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle(
        0.0,
        131.0,
        363.0,
        227.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        249.0,
        300.0,
        345.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        367.0,
        236.0,
        463.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        485.0,
        189.0,
        549.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        571.0,
        165.0,
        622.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        0.0,
        644.0,
        135.0,
        678.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        19.0,
        167.0,
        anchor="nw",
        text="1st ",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        95.0,
        167.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        90.0,
        291.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        88.0,
        513.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        589.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        67.0,
        653.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        79.0,
        415.0,
        anchor="nw",
        text="username",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        19.0,
        297.0,
        anchor="nw",
        text="2nd",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        19.0,
        413.0,
        anchor="nw",
        text="3rd",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        19.0,
        509.0,
        anchor="nw",
        text="4th",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        19.0,
        589.0,
        anchor="nw",
        text="5th",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        19.0,
        653.0,
        anchor="nw",
        text="6th",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_rectangle(
        266.0,
        143.0,
        338.0,
        215.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        146.0,
        380.0,
        218.0,
        452.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        116.0,
        578.0,
        154.0,
        616.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        125.0,
        491.0,
        176.0,
        542.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        101.0,
        649.0,
        125.0,
        673.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        214.0,
        261.0,
        286.0,
        333.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        0.0,
        711.0,
        390.0,
        798.0,
        fill="#B6B6B6",
        outline="")

    canvas.create_text(
        28.0,
        745.0,
        anchor="nw",
        text="Home",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        745.0,
        anchor="nw",
        text="Current Bets",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        319.0,
        745.0,
        anchor="nw",
        text="Profile",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        182.0,
        745.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        227.0,
        745.0,
        anchor="nw",
        text="Leaderboard",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

#Profile Screen
def profPage_mousePressed(app, event):
    x = event.x
    y = event.y
    if clickIn(x, y, 0, 745, 77, 800): #home
        app.mode = 'home'
    if clickIn(x, y, 78, 745, 156, 800): #current bets
        app.mode = 'currBets'
    if clickIn(x, y, 157, 745, 226, 800): #post
        app.mode = 'makePost'
    if clickIn(x, y, 227, 745, 305, 800): #leaderboard
        app.mode = 'leaderb'
    if clickIn(x, y, 306, 745, 390, 800): #profile
        app.mode = 'profPage'

def profPage_redrawAll(app, canvas):
    canvas.create_rectangle(
        34.0,
        113.0,
        144.0,
        223.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        34.0,
        241.0,
        190.0,
        279.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        319.0,
        40.0,
        357.0,
        78.0,
        fill="#D9D9D9",
        outline="")

    
    canvas.create_rectangle( #Most recent bet
        34.0,
        321.0,
        356.0,
        407.0,
        fill="#D9D9D9",
        outline="")

    lastBetT = app.hugom.posts[-1].title if len(app.hugom.posts)>0 else ''
    lastBetE = f'Expires in: {app.hugom.posts[-1].expires} minutes' if len(app.hugom.posts)>0 else ''
    canvas.create_text(34, 321, anchor = 'nw', text = lastBetT, 
                        font = ("Inter", 12 * -1))
    canvas.create_text(34, 370, anchor = 'nw', text = lastBetE,
                        font = ("Inter", 12 * -1))
    canvas.create_rectangle(
        34.0,
        417.0,
        190.0,
        503.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        417.0,
        356.0,
        503.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        609.0,
        190.0,
        695.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        609.0,
        356.0,
        695.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        34.0,
        513.0,
        190.0,
        599.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        513.0,
        356.0,
        599.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_rectangle(
        200.0,
        241.0,
        356.0,
        279.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        168.0,
        161.0,
        anchor="nw",
        text="Net Earnings",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        221.0,
        210.0,
        anchor="nw",
        text="Accuracy",
        fill="#000000",
        font=("Inter", 8 * -1)
    )

    canvas.create_text(
        312.0,
        210.0,
        anchor="nw",
        text="Wins-loses",
        fill="#000000",
        font=("Inter", 8 * -1)
    )

    canvas.create_text(
        266.0,
        161.0,
        anchor="nw",
        text="Friends",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        168.0,
        125.0,
        anchor="nw",
        text=app.hugom.netEarnings,
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        34.0,
        41.0,
        anchor="nw",
        text=app.hugom.username,
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_text(
        221.0,
        186.0,
        anchor="nw",
        text=f'{app.hugom.accuracy}%',
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        312.0,
        186.0,
        anchor="nw",
        text=f'{len(app.hugom.wins)} - {len(app.hugom.losses)}',
        fill="#000000",
        font=("Inter", 20 * -1)
    )

    canvas.create_text(
        259.0,
        125.0,
        anchor="nw",
        text="450",
        fill="#000000",
        font=("Inter", 30 * -1)
    )

    canvas.create_rectangle(
        168.0,
        253.0,
        183.0,
        268.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        0.0,
        711.0,
        390.0,
        798.0,
        fill="#B6B6B6",
        outline="")

    canvas.create_text(
        28.0,
        745.0,
        anchor="nw",
        text="Home",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        80.0,
        745.0,
        anchor="nw",
        text="Current Bets",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        319.0,
        745.0,
        anchor="nw",
        text="Profile",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        182.0,
        745.0,
        anchor="nw",
        text="Post",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

    canvas.create_text(
        227.0,
        745.0,
        anchor="nw",
        text="Leaderboard",
        fill="#000000",
        font=("Inter", 12 * -1)
    )

runApp(width = 390, height = 844)