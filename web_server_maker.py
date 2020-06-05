from http.server import BaseHTTPRequestHandler, HTTPServer
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
from datetime import datetime
import sys,os
import inspect
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import socket


f = open(os.devnull, 'w')
# sys.stdout = f
sys.stderr = f

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

CONST_PORT_NUMBER = 8080

class file_unit():
    def __init__(self):
        self.f_count=0
        self.filename=self.output_unit.filename
        self.user = os.environ.get('USERNAME')
        self.dir_path=self.output_unit.dir_path
        # print("File cheak: "+self.filename)

    def save_file(self, file_content, mode='a'):
        os.makedirs(self.dir_path, exist_ok=True)
        if mode=='x':
            try:
                with open(os.path.join(self.dir_path, self.filename), mode) as f:
                    f.write(file_content)
                self.output_unit.write_msg("Create File: "+self.filename)
                
            except FileExistsError as e:
                # print("File exists: "+self.filename)
                file_splitname = os.path.splitext(self.filename)[0] if self.f_count==0 else self.filename.rsplit("_",1)[0]
                self.f_count+=1
                self.filename= file_splitname + "_" + str(self.f_count) + os.path.splitext(self.filename)[1]
                self.save_file(file_content,"x")

        else:   
            with open(os.path.join(self.dir_path, self.filename), mode) as f:
                f.write(file_content.replace("\n","")+"\n")

class input_data(file_unit):
    def __init__(self):
        super(input_data,self).__init__()
        file_unit.save_file(self,"#header\n","x")
        self.date_flag=self.output_unit.date_flag

    def analysis_post(self,post_data):
        
        post_recieved_time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # print(self.dir_path)
        if self.date_flag:
            file_unit.save_file(self,post_data+","+post_recieved_time)
            self.output_unit.write_msg("GET:"+post_data+","+post_recieved_time)
        else:
            file_unit.save_file(self,post_data)
            self.output_unit.write_msg("GET:"+post_data)
        


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # self.output_unit.write_msg('---post_recieve---')
        # print(self.headers)
        try:
            self.send_response(200)
            self.end_headers()

            # print("Created Header!")
            content_len  = int(self.headers.get("content-length"))
            req_body = self.rfile.read(content_len).decode("utf-8")
            # self.output_unit.write_msg(req_body)
        
            self.write_unit.analysis_post(req_body)
            # print(self.write_unit.dir_path)
            # self.output_unit.write_msg("hoge")

            # print("File CLosed!")
            
            return
        except  IOError:
            self.send_error(400, 'File Not Found...')

    def shut_down(self):
        self.server.server_close()
        # self.server.shutdown()
        # print("shutdown Web Server")





class tk_ui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IoT Web Server Maker")
        self.iconfile = resource_path("favicon.ico")
        self.root.iconbitmap(default=self.iconfile)

        self.root.geometry("200x500+100+100")

        self.frame_main = tk.Frame()
        self.label_main = tk.Label(master=self.frame_main,text="IoT Web server maker!")
        self.label_main.pack()

        self.frame_host = tk.Frame()
        self.host = socket.gethostname()
        self.ip= "-".join(list(set(socket.gethostbyname_ex(self.host)[2])))
        self.port = CONST_PORT_NUMBER

        self.label_strhost = tk.Label(master=self.frame_host,text="host:")
        self.label_strhost.pack(side='left')
        self.label_host = tk.Label(master=self.frame_host,text=self.host)
        self.label_host.pack(side='right')

        self.frame_ip = tk.Frame()
        self.label_ip_strip = tk.Label(master=self.frame_ip,text="ip:")
        self.label_ip_strip.pack(side='left')
        self.label_ip = tk.Label(master=self.frame_ip,text=self.ip)
        self.label_ip.pack(side='right')

        self.frame_port = tk.Frame()
        self.label_port = tk.Label(master=self.frame_port,text="port:")
        self.label_port.pack(side='left')
        self.entry_port = tk.Entry(master=self.frame_port,justify="right",width=6)
        self.entry_port.insert(tk.END,str(self.port))
        self.entry_port.pack(side='right')


        self.frame_main.pack()
        self.frame_host.pack()
        self.frame_ip.pack()
        self.frame_port.pack()

        self.filename="output.csv"
        self.frame_filename = tk.Frame()
        self.label_filename = tk.Label(master=self.frame_filename,text="filename:")
        self.label_filename.pack(side='left')
        self.entry_filename = tk.Entry(master=self.frame_filename,justify="right",width=16)
        self.entry_filename.insert(tk.END,str(self.filename))
        self.entry_filename.pack(side='right')

        self.frame_filename.pack()


        self.frame_button = tk.Frame()        
        self.set_button = tk.Button(
            master=self.frame_button,
            text="save",
            width=4,
            height=1,
            command = self.port_showDialog,
        )

        self.set_button.pack(side='right')


        self.user = os.environ.get('USERNAME')
        self.dir_path='C:/Users/' + self.user + '/Desktop'

        self.dir_button = tk.Button(
            master=self.frame_button,
            text="folder",
            width=6,
            height=1,
            command = self.dir_showDialog,
        )

        self.dir_button.pack(side='left')

        self.frame_button.pack()

        self.frame_date = tk.Frame()
        self.date_flag = True
        self.date_bool=tk.BooleanVar()
        self.date_bool.set(True)
        self.checkbox_date = tk.Checkbutton(master=self.frame_date,variable=self.date_bool,command=self.checkbox_get)
        self.checkbox_date.pack(side='right')

        self.label_date = tk.Label(master=self.frame_date,text="date:")
        self.label_date.pack(side='left')

        self.frame_date.pack()

        self.frame_server = tk.Frame()
        self.c = tk.Canvas(master=self.frame_server,width=40,height=40)
        self.c.pack(side='left')
        self.c.create_oval(15,15,25,25,fill="#ff0000")

        self.set_server_text=tk.StringVar()
        self.set_server_text.set("Stopped")
        self.label_server = tk.Label(master=self.frame_server,textvariable=self.set_server_text)
        self.label_server.pack(side='right')
        self.frame_server.pack()

        self.frame_set_server = tk.Frame()
        self.on_button = tk.Button(
            master=self.frame_set_server,
            text="on",
            width=4,
            height=1,
            command = self.on_showDialog,
        )
        self.on_button.pack(side="left")

        self.off_button = tk.Button(
            master=self.frame_set_server,
            text="off",
            width=4,
            height=1,
            command = self.off_showDialog,
        )
        self.off_button.pack(side="left")

        self.frame_set_server.pack()

        self.frame_recieve = tk.LabelFrame(self.root,text="post_data", width=190, height=300, relief="ridge", borderwidth=4)
        self.text_recieve = tk.Text(self.frame_recieve)
        self.text_recieve.pack(anchor="n")
        self.write_msg("Welcome to IoT Web Server Maker!!")
        self.frame_recieve.pack()
        self.frame_recieve.propagate(0)

        self.frame_server = tk.Frame()

        self.server_flag = True

        self.root.mainloop()

    def checkbox_get(self):
        self.date_flag=self.date_bool.get()
    
    def write_msg(self,msg):
        self.text_recieve.insert(tk.END,msg.replace("\n","")+"\n")
        pos=self.text_recieve.index("end")
        if int(pos.split(".")[0])>10:
            self.text_recieve.delete("1.0","2.end")

    def port_showDialog(self):
        ret = messagebox.askokcancel(title="confirm dialog",message="Set port & file name?")
        if ret:
            self.port=self.entry_port.get()
            self.filename=self.entry_filename.get()
            if 5001<int(self.port)<49151:
                self.write_msg("Set port: "+ self.port)
                self.write_msg("Set file name: "+ self.filename)

                # print(self.port)
            else:
                self.write_msg("Error! please set 5001<port<49151")
                self.port=CONST_PORT_NUMBER
    
    def dir_showDialog(self):
        self.dir_path=filedialog.askdirectory(initialdir=self.dir_path)
        if not self.dir_path:
            self.dir_path='C:/Users/' + self.user + '/Desktop'
        self.write_msg("Selected Dir_PATH is \n"+self.dir_path)
        # messagebox.showinfo('SELECTED DIRECROTY is ...',"Selected Dir_PATH is \n"+self.dir_path)

    def on_showDialog(self):
        self.date_bool.get()
        # print(self.checkbox_date.get())
        if self.server_flag:
            self.write_msg("start Web Server")
            self.c.create_oval(15,15,25,25,fill="#00ff00")
            self.set_server_text.set("Start")
            #  messagebox.showinfo('start Web Server',"START Web Server")
       
            MyHandler.output_unit = self
            input_data.output_unit = self
            MyHandler.write_unit = input_data()
            

            
            MyHandler.write_unit.dir_path=self.dir_path
            self.filename=MyHandler.write_unit.filename
            # print(MyHandler.write_unit.filename)
            self.write_msg("Write PATH to "+self.dir_path +"/"+ self.filename)


            self.server = HTTPServer(('', int(self.port)), MyHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.server_flag = False
        else:
            messagebox.showinfo('Error! ',"already Starting Web Server")
        

        
         
    def off_showDialog(self):
        if not self.server_flag:
            self.write_msg("stop Web Server")
            self.c.create_oval(15,15,25,25,fill="#ff0000")
            self.set_server_text.set("Stopped")
            # messagebox.showinfo('stop Web Server',"STOP Web Server。")

            self.server.shutdown() 
            
            self.server_flag = True
            self.filename = self.entry_filename.get()
        else:
            messagebox.showinfo('Error! ',"already Stopped Web Server")
    

app=tk_ui()
