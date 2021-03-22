#!/usr/bin/env python3.8

import argparse
import subprocess
import codecs
import os
from pathlib import Path
import concurrent.futures 


parser = argparse.ArgumentParser(description='Run automated info gathering scripts')
parser.add_argument('hostname', help='Hostname/IP address for the machine')
parser.add_argument('port', nargs='?', default='80', help='Port for the machine you want to run nikto and/or gobuster on')
parser.add_argument('--nmap', '-n', nargs='*', help='Runs nmap commands with arguments')
parser.add_argument('--nikto', '-k', nargs='*', help="Runs nikto commands with arguments")
parser.add_argument('--gobust', '-g', nargs='*')
parser.add_argument('--output','-o', nargs='?', help='Output directory to write data to', required=True)
args = parser.parse_args()
datalist = []
#def nmapinterface(ip, arguments, output):
#	return outputtype(output,fixlist(arguments,'nmap',ip))

#def niktointerface(ip, arguments,port,output):
#	return(output,fixedlist(arguments, 'nikto', ip, port))


def outputtype(outputform, listformatted, scriptname):
	if outputform == None:
		processing = subprocess.Popen(listformatted, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return codecs.decode(processing.communicate()[0], 'UTF-8')
	else:
		with open(directorypath(outputform)+'/'+scriptname+"out", 'wb') as out, open(directorypath(outputform)+'/'+scriptname+"err",'wb') as err:
			processing = subprocess.Popen(listformatted, stdout=out, stderr=err)
		return processing


def fixlist(arguments,scriptname):
	fixedlist = ['-'+todo for todo in arguments]
	fixedlist.insert(0,scriptname)
	if scriptname == 'nikto':
		#niktolist.append([todo.split() for todo in arguments])
		fixedlist.insert(1, '-host')
		fixedlist.insert(2, f'http://{args.hostname}:{args.port}/')
		#print(niktolist)
		return outputtype(args.output, fixedlist, scriptname)
	elif scriptname == 'nmap':
		fixedlist.append(args.hostname)
		return outputtype(args.output, fixedlist, scriptname)
	elif scriptname == 'gobust':
		fixedlist += ['-u', f'http://{args.hostname}:{args.port}/']


def directorypath(dirpath):
	try:
		Path(dirpath).mkdir(parents=True, exist_ok=True)
		pass
	except Exception as e:
		raise e

	return str(Path(dirpath).resolve())


def printoutputtofile(datalist):
	x = 0
	while x < len(datalist):
		debug = datalist[x].poll()
		if debug == 0 or debug != None:
			datalist[x].communicate()[0]
			datalist.pop(x)
			x = 0
			continue
		if len(datalist) != 0 and x == len(datalist)-1:
			x=0
		else:
			x+=1
#nmapinterface(args.hostname,args.nmap,args.output)
#executor = concurrent.futures.ProcessPoolExecuter()
if args.nmap != None:
	datalist.append(fixlist(args.nmap, 'nmap'))
if args.nikto != None:
	datalist.append(fixlist(args.nikto, 'nikto'))
if args.gobust != None:
	datalist.append(fixlist(args.nikto, 'gobust'))
printoutputtofile(datalist)

