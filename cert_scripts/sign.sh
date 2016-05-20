#!/bin/bash

openssl ca -config openssl-ca.cnf -policy signing_policy -extensions signing_req -out server.pem -infiles server.csr
