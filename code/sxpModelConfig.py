# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:22:04 2017

@author: sunxp
"""
#-------------------------------------------------------------------------------
# Name:        sxpModelConfig.py.py
# Purpose:  The package is to define a set of model dicts that can be ussed to run
#
# Author:      sunxp
#
# Created:      Tue Dec 19 09:22:04 2017
# Copyright:   (c) sunxp 2017
# Licence:     <MIT licence>
#-------------------------------------------------------------------------------
import sxp
def news20test():
    pass
model_conf_dict={}    
model_conf_dict['news20test']=news20test()
def GetModelConfigure(model_conf_name):
    if model_conf_name in model_conf_dict:
        return model_conf_dict[model_conf_name]
    else:
        return None
        