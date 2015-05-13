#!/usr/bin/env python3
__author__ = 'Jason Yao'


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.email = username + '@nyu.edu'
        self.emailDuplicate = username + '+NYU@nyu.edu'
