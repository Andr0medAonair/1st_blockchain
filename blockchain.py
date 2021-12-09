# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 17:52:05 2021

@author: Rafaéla "Andr0medA" Jàneczko
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    
    def__init__(self):
        
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
        def create_block(self, proof, previous_hash):
            
            
