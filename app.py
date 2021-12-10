# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:05:17 2021

@author: rafaela.janeczko
"""

import blockchain
import constants
from flask import Flask, jsonify

app = Flask(__name__)

blockchain = blockchain.Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    res = {
        'message': 'Greetings and salutations, miner! You mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(res), constants.STATUS_OK


@app.route('/get_chain', methods=['GET'])
def get_chain():
    res = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(res), constants.STATUS_OK

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid == True:
        res = {'message': 'Yay! The chain is valid!'}
    else:
        res = {'message': 'Uh oh... Chain is not valid.'} 
    return jsonify(res), constants.STATUS_OK

app.run(host = constants.HOST, port = constants.PORT)