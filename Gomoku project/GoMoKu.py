from tkinter import *
import sqlite3
from hash import hashf


def main_window_initialize():
    global main_screen
    global frame
    main_screen = Tk()
    # setting the title of the game
    main_screen.title('GoMoKu')

    # initializing the width and height of the game window
    window_width = 600
    window_height = 640
    # setting up the background
    frame = Frame(main_screen)
    frame.pack()

    # getting the score
    # en dimension
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()

    # calculating the center point and setting up the window
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    main_screen.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    main_screen.resizable(False, False)

    # calling up the buttons
    Buttons(8, 7).create_buttons()

    # setting up icon
    main_screen.iconbitmap('./image.ico')


class GameBoard:
    def __init__(self, board_size=19):
        # create the game board itself using 2 for loops, each point is represented using ''
        self.board = [['' for col in range(19)] for row in range(19)]
        # create the canvas(game-board)
        self.canvas = Canvas(frame, width=600, height=600, bg='#F7DCB4')
        self.canvas.pack()
        self.board_size = board_size
        # start as black
        self.colour = 'black'
        # set the size for each square in the board
        self.size = 30
        # draw the initial lines on the board
        self.ini_lines()
        # get the coordinates of the board once the board received a Left Mouse click
        self.canvas.bind("<Button-1>", self.get_coord)
        # creating a flag for board clearing
        self.flag = False
        # creating another flag for equal checking in slant checks
        self.eql_check = False
        # initialize a counter that counts the renjus
        self.horizontal_counter = 0
        self.vertical_counter = 0
        self.vert_si = 0
        self.uld_si = 2
        self.drd_si = 2
        self.d_counter = 1
        # set the winner to none
        self.winner = ''
        # initialize the 'New' button, this is initialized here because it required a function inside this class
        Button(
            master=main_screen,
            text='New',
            command=lambda: self.clear_canvas(),
            padx=8, pady=7).pack(side=LEFT)

    def ini_lines(self):
        # create lines for the board with the order (x,y,x1,y1)
        for x in range(self.board_size):
            # drawing all the lines on x-axis
            self.canvas.create_line(self.size + x * self.size, self.size, self.size + x * self.size,
                                    self.size + 18 * self.size)
        for y in range(self.board_size):
            # drawing all the lines on y-axis
            self.canvas.create_line(self.size, self.size + y * self.size, self.size + 18 * self.size,
                                    self.size + self.size * y)

    # used as a clearing method for 'New' button
    def clear_canvas(self):
        self.canvas.delete('all')
        self.ini_lines()
        self.colour = 'black'
        self.board = [['' for col in range(19)] for row in range(19)]

    def get_coord(self, event):
        coord_x = self.canvas.canvasx(event.x)
        coord_y = self.canvas.canvasy(event.y)
        rounded_row = round(coord_x / 30)
        rounded_col = round(coord_y / 30)
        if rounded_col > 19:
            rounded_col = 19
        if rounded_col < 1:
            rounded_col = 1
        if rounded_row > 19:
            rounded_row = 19
        if rounded_row < 1:
            rounded_row = 1
        self.encode_coord_to_board(rounded_row, rounded_col)

    def encode_coord_to_board(self, rounded_row, rounded_col):
        if self.board[rounded_col - 1][rounded_row - 1] == '':
            self.board[rounded_col - 1].pop(rounded_row - 1)
            if self.colour == 'black':
                self.board[rounded_col - 1].insert(rounded_row - 1, 'b')
                self.did_black_win(rounded_row, rounded_col)
            if self.colour == 'white':
                self.board[rounded_col - 1].insert(rounded_row - 1, 'w')
                self.did_white_win(rounded_row, rounded_col)
            self.decide_colour(rounded_row, rounded_col)
            self.horizontal_counter += 1
        elif self.board[rounded_col - 1][rounded_row - 1] != '':
            self.canvas.bind("<Button-1>", self.get_coord)

    def draw_black_pieces(self, rounded_row, rounded_col):
        pieces_coordX = rounded_row * 30
        pieces_coordY = rounded_col * 30
        self.canvas.create_oval(pieces_coordX + 13, pieces_coordY + 13, pieces_coordX - 13, pieces_coordY - 13,
                                fill='black')

    def draw_white_pieces(self, rounded_row, rounded_col):
        pieces_coordX = rounded_row * 30
        pieces_coordY = rounded_col * 30
        self.canvas.create_oval(pieces_coordX + 13, pieces_coordY + 13, pieces_coordX - 13, pieces_coordY - 13,
                                fill='white')

    def decide_colour(self, rounded_row, rounded_col):
        if self.colour == 'black':
            self.draw_black_pieces(rounded_row, rounded_col)
            self.colour = 'white'
        else:
            self.draw_white_pieces(rounded_row, rounded_col)
            self.colour = 'black'

    def b_horizontal_check(self, rounded_col):
        for check in self.board[rounded_col - 1][1:19]:
            if check != 'b':
                self.horizontal_counter = 0
            elif check == 'b':
                self.horizontal_counter += 1
            if self.horizontal_counter >= 5:
                return True

    def w_horizontal_check(self, rounded_col):
        for check in self.board[rounded_col - 1][1:19]:
            if check != 'w':
                self.horizontal_counter = 0
            elif check == 'w':
                self.horizontal_counter += 1
            if self.horizontal_counter >= 5:
                return True

    def b_vertical_check(self, rounded_row):
        self.vert_si = 0
        for check in range(19):
            if self.board[self.vert_si][rounded_row - 1] != 'b':
                self.vertical_counter = 0
                self.vert_si += 1
            elif self.board[self.vert_si][rounded_row - 1] == 'b':
                self.vertical_counter += 1
                self.vert_si += 1
            if self.vertical_counter >= 5:
                return True

    def w_vertical_check(self, rounded_row):
        self.vert_si = 0
        for check in range(19):
            if self.board[self.vert_si][rounded_row - 1] != 'w':
                self.vertical_counter = 0
                self.vert_si += 1
            elif self.board[self.vert_si][rounded_row - 1] == 'w':
                self.vertical_counter += 1
                self.vert_si += 1
            if self.vertical_counter >= 5:
                return True

    # check from top left to bottom right
    def b_tl_br_check(self, rounded_row, rounded_col):
        try:
            self.y_tl = rounded_row - 1 - 1
            self.x_tl = rounded_col - 1 - 1

            self.y_br = rounded_row - 1 + 1
            self.x_br = rounded_col - 1 + 1

            self.d_counter = 1

            while self.board[self.x_tl][self.y_tl] == 'b':  # top left black
                self.x_tl -= 1
                self.y_tl -= 1
                self.d_counter += 1

            while self.board[self.x_br][self.y_br] == 'b':  # bottom right black
                self.x_br += 1
                self.y_br += 1
                self.d_counter += 1

            if self.d_counter >= 5:
                return True
        except IndexError:
            pass

    # check from top right to bottom left
    def b_tr_bl_check(self, rounded_row, rounded_col):
        try:
            self.y_tr = rounded_row - 1 + 1
            self.x_tr = rounded_col - 1 - 1

            self.y_bl = rounded_row - 1 - 1
            self.x_bl = rounded_col - 1 + 1

            self.d_counter = 1

            while self.board[self.x_tr][self.y_tr] == 'b':  # top right black
                self.x_tr -= 1
                self.y_tr += 1
                self.d_counter += 1

            while self.board[self.x_bl][self.y_bl] == 'b':  # bottom left black
                self.x_bl += 1
                self.y_bl -= 1
                self.d_counter += 1

            if self.d_counter >= 5:
                return True
        except IndexError:
            pass

    def w_tl_br_check(self, rounded_row, rounded_col):
        try:
            self.y_tl = rounded_row - 1 - 1
            self.x_tl = rounded_col - 1 - 1

            self.y_br = rounded_row - 1 + 1
            self.x_br = rounded_col - 1 + 1

            self.d_counter = 1

            while self.board[self.x_tl][self.y_tl] == 'w':  # top left white
                self.x_tl -= 1
                self.y_tl -= 1
                self.d_counter += 1

            while self.board[self.x_br][self.y_br] == 'w':  # bottom right white
                self.x_br += 1
                self.y_br += 1
                self.d_counter += 1

            if self.d_counter >= 5:
                return True
        except IndexError:
            pass

    def w_tr_bl_check(self, rounded_row, rounded_col):
        try:
            self.y_tr = rounded_row - 1 + 1
            self.x_tr = rounded_col - 1 - 1

            self.y_bl = rounded_row - 1 - 1
            self.x_bl = rounded_col - 1 + 1

            self.d_counter = 1

            while self.board[self.x_tr][self.y_tr] == 'w':  # top right white
                self.x_tr -= 1
                self.y_tr += 1
                self.d_counter += 1

            while self.board[self.x_bl][self.y_bl] == 'w':  # bottom left white
                self.x_bl += 1
                self.y_bl -= 1
                self.d_counter += 1

            if self.d_counter >= 5:
                return True
        except IndexError:
            pass

    def did_black_win(self, rounded_row, rounded_col, black='b'):
        if self.board[rounded_col - 1][rounded_row - 1] == black:
            if self.b_horizontal_check(rounded_col):
                self.end_state('b')
            elif self.b_vertical_check(rounded_row):
                self.end_state('b')
            elif self.b_tl_br_check(rounded_row, rounded_col):
                self.end_state('b')
            elif self.b_tr_bl_check(rounded_row, rounded_col):
                self.end_state('b')

    def did_white_win(self, rounded_row, rounded_col, white='w'):
        if self.board[rounded_col - 1][rounded_row - 1] == white:
            if self.w_horizontal_check(rounded_col):
                self.end_state('w')
            elif self.w_vertical_check(rounded_row):
                self.end_state('w')
            elif self.w_tl_br_check(rounded_row, rounded_col):
                self.end_state('w')
            elif self.w_tr_bl_check(rounded_row, rounded_col):
                self.end_state('w')

    def end_state(self, winner):
        if winner == 'w':
            self.winner = 'White'
        if winner == 'b':
            self.winner = 'Black'
        end_w = Toplevel(main_screen)
        end_w.title('Game Over')
        end_w.geometry('250x175')
        end_w.resizable(False, False)
        end_w.iconbitmap('./image.ico')
        end_w.grab_set()
        Label(end_w, text='').pack()
        Label(end_w, text='Game is now over').pack()
        Label(end_w, text=self.winner + ' is the winner').pack()
        Label(end_w, text='').pack()
        Button(end_w, text='Play again', command=lambda: [self.clear_canvas(), end_w.destroy()]).pack()


def register_user():
    flag = False
    a_list_of_forbidden_characters = ['\\', '#', '@', '<', '>', '$', '+', '%', '!', '`', '&',
                                      '*', '(', ')', '=', '{', '[', ']', '}', '|', ':', ';', ' ']
    username_info = username.get()
    password_info = password.get()
    hashed_pw = hashf(password_info)
    for checker1 in username_info:
        for checker2 in a_list_of_forbidden_characters:
            if checker1 == checker2:
                flag = True

    if flag or len(username_info) < 6 or len(password_info) < 6 or len(username_info) > 11 or len(password_info) > 11:
        error_reg_label = Label(register_screen, text="Your name is not suitable, please try again", fg='red')
        error_reg_label.pack()
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        error_reg_label.after(2000, lambda: error_reg_label.destroy())
    else:
        table_info = [username_info, hashed_pw]
        sqlt3 = sqlite3_connections(username_info, hashed_pw, 'userlog.db')
        sqlt3.create_objects(table_info)
        return register_checker(username_info, password_info)


def register_checker(username_info, password_info):
    hashed_pw = hashf(password_info)
    sqlt3 = sqlite3_connections(username_info, hashed_pw, 'userlog.db')
    if not sqlt3.select_objects(username_info):
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        invalid_regi_label = Label(register_screen, text="This username is not unique", fg='red')
        invalid_regi_label.pack()
        invalid_regi_label.after(2000, lambda: invalid_regi_label.destroy())
    else:
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        Label(register_screen, text="Register successful", fg='green').pack()
        register_screen.after(2000, lambda: register_screen.destroy())
        return login_window_initialize()


def login_checker():
    username_info = username_login.get()
    password_info = password_login.get()
    hashed_pw = hashf(password_info)
    sqlt3 = sqlite3_connections(username_info, hashed_pw, 'userlog.db')
    if sqlt3.login_checks(username_info, hashed_pw):
        username_login.delete(0, END)
        password_login.delete(0, END)
        Label(login_screen, text="Login successful ! Welcome back !", fg='green').pack()
        login_screen.after(2000, lambda: login_screen.destroy())
    else:
        username_login.delete(0, END)
        password_login.delete(0, END)
        invalid_login_label = Label(login_screen, text="Invalid username or password !", fg='red')
        invalid_login_label.pack()
        invalid_login_label.after(2000, lambda: invalid_login_label.destroy())


def login_window_initialize():
    global login_screen
    global username_login
    global password_login
    login_screen = Toplevel(main_screen)
    login_screen.title('Sign In')
    login_screen.geometry("300x250")
    login_screen.resizable(False, False)
    login_screen.iconbitmap('./image.ico')

    username_login = StringVar()
    password_login = StringVar()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Please enter your login details").pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Username *").pack()
    username_login = Entry(login_screen, textvariable=username_login)
    username_login.pack()
    Label(login_screen, text="Password *").pack()
    password_login = Entry(login_screen, textvariable=password_login)
    password_login.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1,
           command=login_checker).pack()


def register_window_initialize():
    global password
    global username
    global username_entry
    global password_entry
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title('Register')
    register_screen.geometry("400x300")

    username = StringVar()
    password = StringVar()
    Label(register_screen, text='!!Do not use special symbols in your username and password !!').pack()
    Label(register_screen, text="Please fill in the details").pack()
    Label(register_screen, text="Username and password should be longer than 6 letters").pack()
    Label(register_screen, text="Username and password should be no longer than 12 letters").pack()
    Label(register_screen, text="").pack()
    Label(register_screen, text="Username *").pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Label(register_screen, text="Password *").pack()
    password_entry = Entry(register_screen, textvariable=password)
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, command=register_user).pack()


class Buttons:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.column = 0
        self.keywords = ['Exit', 'Login', 'Register']

    def create_buttons(self):
        for g in self.keywords:
            if g == 'Exit':
                Button(master=main_screen,
                       text=g,
                       command=lambda: main_screen.quit(),
                       padx=self.x, pady=self.y).pack(side=LEFT)

            elif g == 'Login':
                Button(master=main_screen,
                       text=g,
                       command=login_window_initialize,
                       padx=self.x, pady=self.y).pack(side=LEFT)

            else:
                Button(master=main_screen,
                       text=g,
                       command=register_window_initialize,
                       padx=self.x, pady=self.y).pack(side=LEFT)


class sqlite3_connections:
    def __init__(self, user, passw, database):
        self.username = user
        self.password = passw
        try:
            self.conn = sqlite3.connect(database)
            self.cur = self.conn.cursor()
        except Exception as errors:
            print('Error during connect: ', str(errors))

    def create_objects(self, info):
        insert = 'INSERT OR IGNORE INTO userlogs(username, password) VALUES(?,?)'
        self.cur.execute(insert, info)
        self.conn.commit()
        self.conn.close()

    def select_objects(self, name):
        for row in self.cur.execute('SELECT username FROM userlogs ORDER BY rowid'):
            x = 0
            if row[x] == name:
                return True
            elif row[x] != name:
                x += 1
                pass
            else:
                return False

    def login_checks(self, name, h_pw):
        for u, p in self.cur.execute("SELECT username, password FROM userlogs ORDER BY rowid"):
            if u != name and p != h_pw:
                pass
            elif u == name and p == h_pw:
                return True
            else:
                return False


def main():
    main_window_initialize()
    GameBoard()
    main_screen.mainloop()


main()

