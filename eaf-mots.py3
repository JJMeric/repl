#!/usr/bin/python
# -*- coding: utf8 -*-
# coding=UTF-8

import os
import re
import sys

fileINname= str(sys.argv[1])

fileIN = open(fileINname, "r")
tout=fileIN.read()
fileIN.close()

mot_speaker=re.findall(r'<TIER LINGUISTIC_TYPE_REF="mot" PARENT_REF="[^"]+" TIER_ID="[^"]+">(?:\n\s*<ANNOTATION>\n\s*<REF_ANNOTATION ANNOTATION_ID="[^"]+" ANNOTATION_REF="[^"]+"(?: PREVIOUS_ANNOTATION="[^"]+")*>\n\s*<ANNOTATION_VALUE>[^<]+</ANNOTATION_VALUE>\n\s*</REF_ANNOTATION>\n\s*</ANNOTATION>)+',tout,re.U|re.MULTILINE)

nmots=0
for speaker in mot_speaker:
    nannot=re.findall(r'<ANNOTATION>',speaker,re.U|re.MULTILINE)
    nmots+=len(nannot)


print("\033[42;30;1m",fileINname,"\t",nmots,"mots\033[0m\n")