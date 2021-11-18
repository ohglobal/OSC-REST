# OSC-REST
A simple python application to bridge Open Sound Control (OSC) to REST APIs

## About
REST APIs are a popular method for communicating with web servers and other databases. Often, physical equipment will also (for better or for worse) implement a REST API for its remote interfacing capabilities. Open Sound Control (OSC) is a commonly used protocol in the entertainment technology industry for inter-application communications across LAN. Occasionally, a piece of equipment that would seem suited for a UDP/TCP API will instead implement REST, and hardware / software not suited for web request communications will be unable to integrate those appliances. This application seeks to resolve the issue by allowing the mechanisms of OSC to communicate with web servers via GET, POST, and PUT requests for bridging OSC to REST APIs.

## Setup
Launch the application and either select the default networking options or input your own information for the OSC network. Then, send OSC command to the application via the API below. Commands sent to OSC-REST will begin with /OSC and commands sent back from OSC-REST will begin with /REST

## Commands to Send
/OSC/REST/GET {string uri, [optional] string fileName} - initiate a GET request with the server located at the URI string. If a file name is provided, the response will be logged in a text file and a notification will be sent via OSC when the file write is complete. Otherwise, the response will be sent back via OSC as a string. This is implemented to avoid potential OSC packet size overflows with large database responses that may be requested via GET.

/OSC/REST/POST {string uri, string json} - initiate a POST request with the provided JSON string passed as the argument. If the server responds, the response will be sent via OSC.

/OSC/REST/PUT {string uri, string json} - initiate a PUT request with the provided JSON string passed as the argument. If the server responds, the response will be sent via OSC.

/OSC/REST/PATCH {string uri, string json} - initiate a PATCH request with the provided JSON string passed as the argument. If the server responds, the response will be sent via OSC.

/OSC/REST/DELETE {string uri} - initiate a DELETE request with the server located at the URI string. If the server responds, the response will be sent via OSC.

## Commands to Receive
/REST/OSC {string response} - the response string from the given request

/REST/OSC/fileComplete {int 1} - an indication that the file containing the response has been written to disk

## Limitations / TODO
There is currently no way to distinguish which replies come from which request. To resolve this, a tag field will be added to a future update of the software that will become included as an OSC wildcard in the address scheme of the response packets, so the responses can be filtered with standard OSC address syntax. 

JSON is currently the only valid payload to send to the web server. OSC provides plenty of mechanisms for alternative communication methods, so in the future it would be nice to allow OSC args to be passed individually within a packet and have the software construct JSON from those packets. Some REST APIs do not implement JSON, so a method of passing the parameters and wrapping them with headers in a different format may be needed eventually. 

