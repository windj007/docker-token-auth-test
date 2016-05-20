#!/bin/bash

openssl req -config openssl-server.cnf -newkey rsa:2048 -sha256 -nodes -out server.csr -outform PEM
