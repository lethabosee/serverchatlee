import socket     #import socket module to establish network 
import threading    # import threading to enable processes to run at the same time 
import tkinter      #binds/interfaces the gui tootkit 
import tkinter.scrolledtext   #allows the usage of multiple texts in 1 line 
from tkinter import simpledialog    #a chat dialog .eg what is your name ? , respond my name is , flowing in a dialog order 

HOST = '127.0.0.1'        
PORT = 9090    

class Client:   #classify the client 

    def __init__(self, host, port):    #self will act as first argument followed by the host and port  

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #SOCK_STREAM shows thst socket used it a TCP , AF_INET shows the adress its connected to 
        self.sock.connect((host, port))

        msg = tkinter.Tk()   #this funtion has to bind the message  to toolkit
        msg.withdraw()

        self.nickname = simpledialog.askstring("nickname", "please choose a nickname", parent=msg)    

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)       #bind the argument to the loop 
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()


    def gui_loop(self):
        self.win = tkinter.Tk()

        self.text_area = tkinter.scrolledtext.scrolledtext(self.win)
        self.text_area.config(state='disabled')

        self.input_area = tkinter.Text(self.win, height=4)

        self.send_button = tkinter.Button(self.win, text='send', command=self.write)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()


    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
            


    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


        

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)

                if  message == 'NICK':
                 self.sock.send(self.nickname.encode('utf-8'))

                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

   

            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()

                break

        client = Client(HOST, PORT)
