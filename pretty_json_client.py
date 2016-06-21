#!/usr/bin/python

"""
This file runs an HTTP client on port 8001.

It reads one byte from the HTTP response at a time and appends it to 
a temporary buffer (byte string). It determines from the structure of
JSON where one object ends and another begins. Once it detects the end 
of an object, it decodes the object using utf-8 and prints it 
(followed by a line break) on the standard output and reads the next byte
if any. If a final HTTP chunk is detected, then the client closes the 
connection.

This code will run in Python 3, and possibly also in 2.7.
"""

import json
import sys

# Handle version differences between Python 2 and 3
if sys.version_info.major >= 3:
    from http.client import HTTPConnection
else:
    from httplib import HTTPConnection


def readChar():
    """
    Read and return one byte from the HTTP response at a time.
    """
    return response.read(1)

def parseDoubleQuotes():
    """
    Append all the bytes to the temporary byte string.
    Return the string after '"' (that is not escaped) is encountered.
    """

    tempbuf = b""
    
    while True:
        c = readChar()
        tempbuf += c

        # An escape character is encountered
        # append the next character to the buffer
        if (c == b"\\"):
            tempbuf += readChar()
            continue

        # The closing " is encounted, so
        # return the buffer
        if (c == b'"'):
            return tempbuf

if __name__ == '__main__':
    conn = HTTPConnection("127.0.0.1: 8001")
    conn.request('GET', "/")
    response = conn.getresponse()

    # Temporary buffer for a JSON object
    # only contains one object at a time.
    resbuf = b""

    # Incremented by 1 if "{" is encountered
    # otherwise, decremented by 1 if "}" is encountered.
    # Curly brackets encountered within double quotes
    # are not counted.
    curlyBracketCount = 0

    while True:
        c = readChar()

        if (len(c) == 0):
            break

        # Append all characters except newline and space to
        # the temporary byte string
        if (c != b"\n" and c != b" "):
            resbuf += c

            if (c == b"{"):
                curlyBracketCount = curlyBracketCount + 1

            elif (c == b"}"):
                curlyBracketCount = curlyBracketCount - 1

                if (curlyBracketCount == 0):
                    # The closing curly bracket for the outermost
                    # JSON object is encountered, so decode the 
                    # byte string using utf-8 and print it 
                    # (followed by a line break) on the
                    # standard output
                    print(resbuf.decode('utf-8'))
                    resbuf = b""

            elif (c == b'"'):
                resbuf += parseDoubleQuotes()

            elif (c == b":" or c == b","):
                # Add space after a ":" and "," to beautify
                # the JSON object
                resbuf += b" "

    # We have just received an empty chunk or the final HTTP chunk 
    # so we close the connection
    conn.close()





