#	OSC-REST
#	A bridge between Open Sound Control (OSC) and REST APIs
#	Office Hours Global Community Project
#	Created and maintained by Andy Carluccio - Washington, D.C.

#OSC variables & libraries
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client 
from pythonosc import osc_bundle
from pythonosc import osc_bundle_builder

#Argument management
import argparse

#system
import sys

#REST
import requests
import json

#GET Request
def getRequest(unused_addr, *args):
	print("Received info for GET Request")
	uri = args[0]
	file_name = ""

	#determine if a file name was provided as an arg
	if(len(args) > 1):
		file_name = args[1]

	response = requests.get(uri)

	#if a file name was provided, save the response to disk and notify via OSC
	if(file_name != ""):
		print("Sending response via disk")
		outFile = open(file_name,"w+")
		outFile.write(str(response.json()))
		client.send_message("/REST/OSC/fileComplete", 1)
	#otherwise, send the entire response via OSC
	else:
		print("Sending response via OSC")
		client.send_message("/REST/OSC", str(response.json()))

#POST Request
def postRequest(unused_addr, uri, args):
	print("Received info for POST request")
	in_json = json.loads(args)
	print(str(in_json))
	reply = requests.post(uri, json = in_json)
	client.send_message("/REST/OSC", reply.text)

#PUT Request
def putRequest(unused_addr, uri, args):
	print("Received info for PUT request")
	in_json = json.loads(args)
	print(str(in_json))
	reply = requests.put(uri, json = in_json)
	client.send_message("/REST/OSC", reply.text)

#PATCH Request
def patchRequest(unused_addr, uri, args):
	print("Received info for PATCH request")
	in_json = json.loads(args)
	print(str(in_json))
	reply = requests.patch(uri, json = in_json)
	client.send_message("/REST/OSC", reply.text)

#DELETE Request
def deleteRequest(unused_addr, uri):
	print("Received info for DELETE request")
	reply = requests.delete(uri)
	client.send_message("/REST/OSC", reply.text)

#Main execution script--------------------------------------
if __name__ == "__main__":

	#Greeting
	print("Welcome to OSC-REST")
	print("Created by Andy Carluccio")
	print("This program establishes a bidirectional OSC interface with REST APIs")
	print("See ReadMe for commands and useage")
	print()

	#OSC Setup
	print("Would you like to [1] Input network parameters or [2] use default: 127.0.0.1:1234 (sending) :7050 (receiving)")
	
	send_ip = "127.0.0.1"
	send_port = 1234
	receive_port = 7050

	selection = int(input())
	if(selection == 1):
		print("Input network parameters")
		send_ip = str(input("Send ip?: "))
		send_port = int(input("Send port?: "))
		receive_port = int(input("Receive port?: "))
	else:
		print("Using default network settings")

	#create the osc sending client
	client = udp_client.SimpleUDPClient(send_ip,send_port)

	#catches OSC messages
	dispatcher = dispatcher.Dispatcher()

	#map functions here:
	dispatcher.map("/OSC/REST/GET", getRequest)
	dispatcher.map("/OSC/REST/POST", postRequest)
	dispatcher.map("/OSC/REST/PUT", putRequest)
	dispatcher.map("/OSC/REST/PATCH", patchRequest)
	dispatcher.map("/OSC/REST/DELETE", deleteRequest)

	#set up server to listen for osc messages
	server = osc_server.ThreadingOSCUDPServer((send_ip,receive_port),dispatcher)

	#Print the info
	sys.stdout.write("Opened Client on: ")
	sys.stdout.write(send_ip)
	sys.stdout.write(":")
	sys.stdout.write(str(send_port))
	sys.stdout.write('\n')
	sys.stdout.write("Listening on: ")
	sys.stdout.write(str(receive_port))
	sys.stdout.write('\n')

	print()

	#begin the infinite loop
	server.serve_forever()