#!/usr/bin/env python

import sys, secrets

# List of allowed characters in the password.
num_list = '0123456789'
alpha_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
punc_list = '~!@#$%^&*()_+'
char_list = num_list + alpha_list + punc_list

assert len(sys.argv) == 3

n = int(sys.argv[1])  # Number of passwords to generate
l = int(sys.argv[2])  # Length of the password

for i in range(n):
    password = ''.join(secrets.choice(char_list) for j in range(l))
    print(password)

