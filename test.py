from http.server import BaseHTTPRequestHandler, HTTPServer
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
import os
import inspect
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import socket



PORT_NUMBER = 8080


class file_unit():
    def __init__(self):
        self.f_count=0
        self.file_name="output.csv"
        self.user = os.environ.get('USERNAME')
        self.dir_path='C:/Users/' + self.user + '/Desktop/sosa/'
        print("File cheak: "+self.file_name)

    def save_file(self, file_content, mode='a'):
        os.makedirs(self.dir_path, exist_ok=True)
        if mode=='x':
            try:
                with open(os.path.join(self.dir_path, self.file_name), mode) as f:
                    f.write(file_content)
                
            except FileExistsError as e:
                print("File exists: "+self.file_name)
                file_splitname = os.path.splitext(self.file_name)[0] if self.f_count==0 else self.file_name.rsplit("_",1)[0]
                self.f_count+=1
                self.file_name= file_splitname + "_" + str(self.f_count) + os.path.splitext(self.file_name)[1]
                self.save_file(file_content,"x")

        else:   
            with open(os.path.join(self.dir_path, self.file_name), mode) as f:
                f.write(file_content)

class input_data(file_unit):
    def __init__(self):
        super(input_data,self).__init__()
        file_unit.save_file(self,"#header\n","x")

    def analysis_post(self,post_data,cheacker=False):
        post_recieved_time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        file_unit.save_file(self,post_data)


        if cheacker:
          pass  
        


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print('---post_recieve---')
        # print(self.headers)
        try:
            self.send_response(200)
            self.end_headers()
            # print("Created Header!")
            content_len  = int(self.headers.get("content-length"))
            req_body = self.rfile.read(content_len).decode("utf-8")
            print(req_body)
        
            self.test.analysis_post(req_body)
            # print("File CLosed!")
            return
        except  IOError:
                self.send_error(400, 'File Nout Found...')





class tk_ui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IoT Web Server Maker")
        self.iconfile = "./favicon.ico"
        self.root.iconbitmap(default=self.iconfile)

        self.root.geometry("200x500+100+100")

        self.frame_main = tk.Frame()
        self.label_main = tk.Label(master=self.frame_main,text="IoT Web server maker!")
        self.label_main.pack()

        self.frame_host = tk.Frame()
        self.host = socket.gethostname()
        self.ip= socket.gethostbyname(self.host)
        self.port = PORT_NUMBER

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

        self.set_button = tk.Button(
            text="set",
            width=4,
            height=1,
            command = self.port_showDialog,
        )

        self.set_button.pack()


        self.user = os.environ.get('USERNAME')
        self.dir_path='C:/Users/' + self.user

        self.dir_button = tk.Button(
            text="保存先",
            width=6,
            height=1,
            command = self.dir_showDialog,
        )

        self.dir_button.pack()



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
        self.write_msg("first")
        self.frame_recieve.pack()
        self.frame_recieve.propagate(0)

        self.frame_server = tk.Frame()

        self.root.mainloop()
    
    def write_msg(self,msg):
        self.text_recieve.insert(tk.END,msg+"\n")
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

                print(self.port)
            else:
                self.write_msg("Error! please set 5001<port<49151")
    
    def dir_showDialog(self):
        self.dir_path=filedialog.askdirectory(initialdir=self.dir_path)
        if not self.dir_path:
            self.dir_path='C:/Users/' + self.user
        self.write_msg("Selected Dir_PATH is \n"+self.dir_path)
        # messagebox.showinfo('SELECTED DIRECROTY is ...',"Selected Dir_PATH is \n"+self.dir_path)

    def on_showDialog(self):
        self.write_msg("start Web Server")
        self.c.create_oval(15,15,25,25,fill="#00ff00")
        self.set_server_text.set("Start")
        #  messagebox.showinfo('start Web Server',"Web Serverを立ち上げます。")
         
    def off_showDialog(self):
        self.write_msg("stop Web Server")
        self.c.create_oval(15,15,25,25,fill="#ff0000")
        self.set_server_text.set("Stopped")
        # messagebox.showinfo('start Web Server',"Web Serverを立ち上げます。")    

    

app=tk_ui()

# try:
#     MyHandler.test = input_data()   

#     server = HTTPServer(('', PORT_NUMBER), MyHandler)
#     print("Server started")
#     server.serve_forever()

# except Exception as e:
#     print(e)
