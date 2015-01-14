#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program: Auto Backup Script V1.0
# Author:  Clumart.G(翅儿学飞)
# Date:    2014-12-12
# Update:  2014121201 None

#Build-in Module
import os
import sys
import string
import re
from ftplib import FTP

#Third Part Module

#Project Module
sys.path.append("./include/")
import loadconf 

file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)

class SoftInfo():
    '''Show infomation of this software.'''
     
    def __init__(self,softname,softversion):
        self.softname = softname
        self.softversion = softversion
    
    def info_head(self):
        '''The header of software message(s)'''
        print " o----------------------------------------------------------------o"
        print " | :: %-35s    %20s |" % (self.softname,"V "+self.softversion)
        print " o----------------------------------------------------------------o"	
    
    def info_start(self):
        os.system("clear")
        '''Show the message when the beginning of this software.'''
        self.info_head() 
        print " |                                                                |"
        print " |              Thank you for use auto backup script!             |"
        print " |                                                                |"
        print " |                     http://www.idcsrv.com                      |"
        print " |                                                                |"
        print " |                   Author:翅儿学飞(Clumart.G)                   |"
        print " |                    Email:myregs6@gmail.com                     |"
        print " |                         QQ:1810836851                          |"
        print " |                         QQ群:61749648                          |"
        print " |                                                                |"
        print " |          Hit [ENTER] to continue or ctrl+c to exit             |"
        print " |                                                                |"
        print " o----------------------------------------------------------------o"
        raw_input()
        os.system("clear")
        
    def info_end(self):
        '''Show the message when the end of this software.'''
        self.info_head();
        print " |                                                                |"
        print " |                       Going To Sleep  :)                       |"
        print " |                                                                |"
        print " |                                                                |"
        print " |                     http://www.idcsrv.com                      |"
        print " |                                                                |"
        print " |                   Author:翅儿学飞(Clumart.G)                   |"
        print " |                    Email:myregs6@gmail.com                     |"
        print " |                         QQ:1810836851                          |"
        print " |                         QQ群:61749648                          |"
        print " |                                                                |"
        print " o----------------------------------------------------------------o"

    def info_err_head(self):
        '''The header of error message(s)'''
        print " o----------------------------------------------------------------o"
        print " | :: %-35s    %20s |" % ("Error","V "+self.softversion)
        print " o----------------------------------------------------------------o"	
    
    def info_err_info(self,errmsg):
        '''Show the error message(s)'''
        self.info_err_head()
        print "Error Message:"
        print "%s " %(errmsg)

class BackupByFtp():
    '''backup by ftp'''
     
    def __init__(self):
        print "Loading FTP ..."
    
    def login(self,host,port,user,pwd):
        '''Login the ftp server.'''
        self.f = FTP()
        self.f.set_debuglevel(0)
        self.f.connect(host,port,30)
        self.f.login(user,pwd)
        
    def server_file_list(self):
        try:
            self.f.dir("public_html")
            tmp_a = self.f.retrlines("LIST "+"public_html/a", callback=None)
            if re.search("226 0 matches total",tmp_a,re.IGNORECASE):
                print "just make a dir"
        except Exception, e:
            if str(e)[0:3]=="450" :
                print "just make a dir"
        
    def upload(self, lf="./", rf="./"):
        #future:check ftp status
        
        #filename must before realpath,beacuse links.
        local_name = os.path.basename(lf)
        #realpath is a ture path,except symbolic links;abspath will use symbolic links.
        local = os.path.realpath(lf) 
        remote = rf 
        
        #check dir or file
        if os.path.isfile(local):#a file
            #future:check remote is a dirpath
            remote_file_name = remote+"/"+local_name
            
            print "\033[1;32;-1m"+">>> transfering file %s" % (local)+"\033[0m"
            self.f.storbinary("stor "+remote_file_name,open(local,"r"))
            
        elif os.path.isdir(local):#if a dir
            for i in os.listdir(local):
                tmp_path = local+"/"+i  #realpath(i) is script_path+i,it's wrong. so must define realpath myself.
                
                if os.path.isdir(tmp_path): #if a dir ,do something
                    tmp_local = local+"/"+i
                    tmp_remote = remote+"/"+i
                    try: #test dir is exist or not;if get 405(dir not exist) or (0 matches),then create it.
                        self.f.dir(tmp_remote)
                        tmp_a = self.f.retrlines("LIST "+tmp_remote, callback=None)
                        if re.search("226 0 matches total",tmp_a,re.IGNORECASE):
                            self.f.mkd(tmp_remote)
                            print "\033[1;32;-1m"+">>> creating dir %s" % (tmp_local)+"\033[0m"
                    except Exception, e:
                        if str(e)[0:3]=="450":
                            self.f.mkd(tmp_remote)
                            print "\033[1;32;-1m"+">>> creating dir %s" % (tmp_local)+"\033[0m"
                    print "\033[1;32;-1m"+">>> transfering dir %s" % (tmp_local)+"\033[0m"
                else:
                    tmp_local = tmp_path
                    tmp_remote = remote
                self.upload(tmp_local,tmp_remote)
        else:#not a file or dir,then what's this?
            print "Get Local Source Error!May Be Dir or File Not Exist!"
        
    def close(self):
        self.f.quit()

class Task():
    '''do the task'''
     
    def __init__(self,cf):
        self.cf = cf
         
    def get_servers(self,s,res=[],except_group=[]):
        '''Get the list of server:s is servers in task,must be define;
        res is exist server_list,main for recursive.
        except_group is for dir loop,like a include b ;b include a'''
        
        #init var and set it to save recursive data
        server_list=res
        
        #trans str to list
        s = s.split(",")
         
        #get every value
        for v in s:
            tk_tmp = re.search("^ftpserver_",v,re.IGNORECASE)
            if tk_tmp: #if a server ;add it to the server list
                if v not in server_list: # if key exist then skip,if new key ;then add it.
                    server_list.append(v)
            elif re.search("^ftpgroup_",v,re.IGNORECASE):
                if v not in except_group:   #avoid dir loop
                    except_group.append(v)
                    #future:add self.cf[v+"_servers"] is exist
                    self.get_servers(self.cf[v+"_servers"],server_list,except_group) #recursive get servers
            else:
                print ""
                 
        return server_list
    
     
    def get_task(self):
        '''Get The Enable Task In Config File''' 
        self.tasks = {}
        strre = re.compile(r"^task_\w+_enable$",re.IGNORECASE)
        
        #get match tasks
        for (k,v) in self.cf.items():
            if strre.match(k) and v.lower()=="true":
                tk_tmp = re.search("^task_\w+_",k,re.IGNORECASE)
                if tk_tmp:
                    tk_pre = tk_tmp.group()
                    if self.tasks.has_key(tk_pre):
                        continue
                    else:
                        self.tasks[tk_pre] = {}
                    
                #config check
                if not self.cf.has_key(tk_pre+"source"):
                    continue
                    
                if not self.cf.has_key(tk_pre+"target"):
                    continue
                     
                if not self.cf.has_key(tk_pre+"servers"):
                    continue
                 
                #task setting.Note: value must after "continue"
                if self.cf.has_key(tk_pre+"transmothod"):
                    self.tasks[tk_pre]["transmethod"] = self.cf[tk_pre+"transmothod"]
                elif self.cf.has_key("global_transmothod"):
                    self.tasks[tk_pre]["transmethod"] = self.cf["global_transmothod"]
                else:
                    self.tasks[tk_pre]["transmethod"] = "ftp"
                     
                self.tasks[tk_pre]["source"] = self.cf[tk_pre+"source"]
                self.tasks[tk_pre]["target"] = self.cf[tk_pre+"target"]
                self.tasks[tk_pre]["servers"] = self.get_servers(self.cf[tk_pre+"servers"])
    
    def do_task(self):
        '''Running the task'''
        #Get tasks
        self.get_task()
         
        for (t,tmp) in self.tasks.items():
            s = tmp["servers"]
            
            for i in s: #servers list
                if re.search("ftp",tmp["transmethod"],re.IGNORECASE):   #match ftp transmethod
                    print "\033[1;32;-1m"+">>>>>> Running Task %s On Server %s <<<<<<" % (t,i)+"\033[0m"
                    bf = BackupByFtp()
                    bf.login(self.cf[i+"_host"],self.cf[i+"_port"],self.cf[i+"_username"],self.cf[i+"_password"])
                    bf.upload(tmp["source"],tmp["target"])
                    bf.close()


if __name__ == '__main__':
    ShowSoftInfo = SoftInfo("SYNC","1.0.0-beta")
    ShowSoftInfo.info_start()
    CF = loadconf.GetConfig()
    task = Task(CF.conf)
    task.do_task()
    ShowSoftInfo.info_end()

