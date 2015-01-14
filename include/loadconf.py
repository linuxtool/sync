#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program: Load the config.
# Author:  Clumart.G(翅儿学飞)
# Date:    2014-05-09
# Update:  2014050901 None

#Build-in Module
import os
import sys 
import string
import ConfigParser

#Third Part Module

#Project Module

file_path = os.path.realpath(__file__)
file_dir = os.path.dirname(file_path)
home_dir = os.path.dirname(file_dir)
etc_dir = home_dir+"/etc" 

class GetConfig():
    '''Get the config setting.'''
     
    def __init__(self,config_file="main.conf"):
        '''set config file path ,load all the settings'''
        
        self.conf={};
        #get the config file path
        config_file = config_file.lstrip();
        if config_file[0:1] == "/":
            conf_file_path = config_file;
        else:
            conf_file_path = etc_dir+"/"+config_file;
        
        if os.access(conf_file_path,os.R_OK):
            #Load config file
            config = ConfigParser.ConfigParser()
            config.read(conf_file_path)
            sections=config.sections()
            for sct in sections: 
                sec_item=config.items(sct)
                for (k,v) in sec_item:
                    self.conf.setdefault(sct+"_"+k,v);
            #print self.conf                                                                                           
        else:
            print "Config File Access Error."
            exit();
 
if __name__ == '__main__':
    a=GetConfig();
    #print a.conf["log_log_file"];
