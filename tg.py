import subprocess
import threading
import os
import re

class Tg:
    PUB_FILE =None
    PATH = None
    proc = None
    flag=False
    thread_bot =None
    COLOR_RED="\033[0;31m"
    COLOR_REDB="\033[1;31m"
    COLOR_NORMAL="\033[0m"
    COLOR_GREEN="\033[32;1m"
    COLOR_GREY="\033[37;1m"
    COLOR_YELLOW="\033[33;1m"
    COLOR_BLUE="\033[34;1m"
    COLOR_MAGENTA="\033[35;1m"
    COLOR_CYAN="\033[36;1m"
    COLOR_LCYAN="\033[0;36m"
    COLOR_INVERSE="\033[7m"


    iter_user_begin = COLOR_NORMAL+' '+COLOR_RED
    iter_user_end = COLOR_BLUE+" >>> "
    iter_receve_meta = COLOR_BLUE + ' >>> '
    iter_group_meta = ' ' + COLOR_NORMAL + ' ' + COLOR_MAGENTA
    iter_msg = COLOR_BLUE+" >>>"

    ansi_escape = re.compile(r'\x1b[^m]*m')
    flag=None
    def __init__(self,PATH=os.getcwd(),PUB_FILE="tg-server.pub"):
        self.PATH = PATH
        self.PUB_FILE = self.PATH+"/"+PUB_FILE
        self.flag=False

    def bot(self):
        self.proc = subprocess.Popen([self.PATH+"/bin/telegram-cli","-k",self.PUB_FILE],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        self.proc.stdin.write(("contact_list").encode('utf-8'))
        self.proc.stdin.flush()
        user = None;
        msg =None;
        group = None;
        while (self.flag):

            for line in iter(self.proc.stdout.readline,''):
                line =line.decode('utf-8')
                if (self.iter_group_meta in line and self.iter_receve_meta in line):
                    print('group')
                    group = line.split(self.COLOR_MAGENTA)[2].split(self.COLOR_NORMAL)[0]
                    user = line[line.find(self.iter_user_begin)+len(self.iter_user_begin) : line.find(self.iter_user_end)]
                    msg = line[line.find(self.iter_msg)+len(self.iter_msg):]
                    print("group chat group: " +group +"user : " +user+" msg : "+msg)
                elif (self.iter_user_begin in line and self.iter_receve_meta in line):
                    print("user")
                    user = line[line.find(self.iter_user_begin)+len(self.iter_user_begin) : line.rfind(self.iter_user_end)]
                    msg = line[line.find(self.iter_msg)+len(self.iter_msg):]
                    print("1:1 chat user : " +user+" msg : "+msg)
                else:
                    pass
                if user!=None or group!=None:
                    if  msg.endswith("[0m\n"):
                        msg=msg.rstrip('[0m\n')
                    user = re.compile(r'\x1b[^m]*m').sub('', user)
                    self.ai(msg,user,group)


                    user = None;
                    msg =None;
                    group = None;
        print("bot shoudown")

    def run(self):
        self.flag=True
        self.thread_bot = threading.Thread(target=self.bot)
        self.thread_bot.start()
        self.thread_bot.join()
    def ai(self,msg,user,group):
        if (group is None):
            user = user.replace(' ','_')
            print("msg "+user+' '+msg+'\n')
            self.proc.stdin.write(("msg "+user+' '+msg+'\n').encode('utf-8'))
            self.proc.stdin.flush()
        else:
            group = group.replace(' ','_')
            self.proc.stdin.write(("msg "+group+" "+msg+'  \n').encode('utf-8'))
            self.proc.stdin.flush()


    def end(self):
        self.flag=False
