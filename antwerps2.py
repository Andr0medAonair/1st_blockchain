# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 17:36:08 2021

@author: rafaela.janeczko
"""

import blockchain
import constants
from uuid import uuid4
from flask import Flask, jsonify

app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

blockchain = blockchain.Blockchain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(
        sender=node_address, receiver='Andr0medA', ammount=1)
    block = blockchain.create_block(proof, previous_hash)
    res = {
        'message': 'Greetings and salutations, miner! You mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
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


@app.route('/add_transaction', methods=['POST'])
def add_transaction(req):
    json = req.get_json()
    transaction_keys = ['sender', 'receiver', 'ammount']
    if not all(key in json for key in transaction_keys):
        return 'Missing some transaction elements', constants.STATUS_BAD_REQUEST
    index = blockchain.add_transaction(
        json['sender'], json['receiver'], json['ammount'])
    res = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(res), constants.STATUS_CREATED


app.run(host=constants.HOST, port=constants.PORT_B)