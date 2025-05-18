import unittest
import time
from blockchain import Blockchain, Block


class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0")

    def test_add_block(self):
        self.blockchain.add_block("Patient Record A")
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(self.blockchain.chain[1].data, "Patient Record A")

    def test_proof_of_work_difficulty(self):
        block = Block(1, time.time(), "Test", self.blockchain.chain[0].hash)
        valid_hash = self.blockchain.proof_of_work(block)
        self.assertTrue(valid_hash.startswith("0" * Blockchain.difficulty))

    def test_chain_validation(self):
        self.blockchain.add_block("A")
        self.blockchain.add_block("B")
        self.assertTrue(self.blockchain.is_chain_valid(self.blockchain.chain))

        # Tamper
        self.blockchain.chain[1].data = "Tampered"
        self.assertFalse(self.blockchain.is_chain_valid(self.blockchain.chain))

    def test_consensus_replace_chain(self):
        blockchain_2 = Blockchain()
        blockchain_2.add_block("A")
        blockchain_2.add_block("B")
        replaced = self.blockchain.replace_chain(blockchain_2.chain)
        self.assertTrue(replaced)
        self.assertEqual(len(self.blockchain.chain), 3)


if __name__ == '__main__':
    unittest.main()
