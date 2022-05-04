#!/bin/env python
#-*- coding: utf-8 -*-

from history_all import *
import datetime

def get_datetime(date_str) :
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

def history_by_date(history_list, start_date, end_date) :
    cmd_list = []
    for h in history_list :
        history_date = get_datetime(h[0])
        if(history_date >= start_date and history_date <= end_date) :
            cmd_list.append(h)
    return cmd_list


if __name__ == "__main__" :
    print ("어느 시간에 실행한 명령어를 조회하시겠습니까?")
    input_date = input("년-월-일 시각을 입력하세요(예. 2016-08-11 14) :")
    input_date = input_date + ":00:00"

    date = get_datetime(input_date)
    start_date = date - datetime.timedelta(hours=1)
    end_date = date + datetime.timedelta(hours=1)

    
    file = open('report_time_' + now.strftime("%Y-%m-%d %H_%M_%S") + '.txt', "w")
    print (start_date, "~", end_date, "동안 입력된 명령어")
    file.write("{} ~ {} 동안 입력된 명령어\n".format(start_date, end_date))
    print ("-" * 70)
    file.write("-" * 70)
    file.write("\n")
    print (start_date, "~", end_date, "동안 입력된 명령어")
    file.write("{} ~ {} 동안 입력된 명령어\n".format(start_date, end_date))
    print ("-" * 70)
    file.write("-" * 70)
    file.write("\n")

    accounts = get_accounts()
    for account in accounts :
        history_list = history(account)
        if len(history_list) == 0:
            continue

        history_list = history_by_date(history_list, start_date, end_date)
        if len(history_list) == 0 :
            continue

        print ("계정 :", account)
        file.write("계정 :", account)
        file.write("\n")
        for h in history_list :
            print ("\t%s\t%s" %h)
            file.write("\t {0} \t {1}".format(h[0], h[1]))
            file.write("\n")
        print ("-" * 70)
        file.write("-" * 70)
        print ("계정 :", account)
        file.write("계정 :", account)
        file.write("\n")
        for h in history_list :
            print ("\t%s\t%s" %h)
            file.write("\t {0} \t {1}".format(h[0], h[1]))
            file.write("\n")
        print ("-" * 70)
        file.write("-" * 70)
    file.close()
