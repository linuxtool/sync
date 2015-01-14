#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program: log recode 
# Author:  Clumart.G(翅儿学飞)
# Date:    2014-05-12
# Update:  2014051201 None

#Build-in Module
import os
import string
import ConfigParser

#Third Part Module

#Project Module

file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)
home_dir = os.path.dirname(file_dir)
log_dir = home_dir+"/var/log" 

class LogRecord():
    '''Log Module.'''
     
    def __init__(self,config_file="main.log"):
        '''set log file path ,load all the settings'''
        
        #get the config file path
        config_file = config_file.lstrip();
        if config_file[0:1] == "/":
            conf_file_path = config_file;
        else:
            conf_file_path = log_dir+"/"+config_file;
        
        #check log file is exists ,and create it if not.
        if not os.path.isfile(conf_file_path):
            conf_dir_path = os.path.dirname(conf_file_path);
            print conf_file_path;
            print conf_dir_path;
            if not os.path.exists(conf_dir_path):
                os.makedirs(conf_dir_path)
            open(conf_file_path,"w").write("") 
            #fix me: add file/dir create check. 
            #fix me: add file read/write check.

if __name__ == '__main__':
    a=LogRecord("test_can_del.log");
    #print a.conf["log_log_file"];
