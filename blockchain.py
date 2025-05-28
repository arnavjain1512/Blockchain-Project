import hashlib
import json
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    difficulty = 2  # Number of leading 0s required in hash

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          timestamp=time.time(),
                          data=data,
                          previous_hash=last_block.hash)
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if not current.hash.startswith("0" * Blockchain.difficulty):
                return False

        return True

    def replace_chain(self, new_chain):
        if len(new_chain) > len(self.chain) and self.is_chain_valid(new_chain):
            self.chain = new_chain
            return True
        return False

    def to_dict(self):
        return [block.__dict__ for block in self.chain]


#Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_block("Patient A record")

    print("Mining block 2...")
    blockchain.add_block("Patient B record")

    for block in blockchain.chain:
        print(json.dumps(block.__dict__, indent=4))






