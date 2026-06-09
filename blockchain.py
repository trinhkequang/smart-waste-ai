import hashlib
import json
import os
from time import time
from datetime import datetime


# =========================================
# BLOCK
# =========================================
class Block:

    def __init__(
        self,
        index,
        timestamp,
        waste_type,
        confidence,
        status,
        previous_hash,
        nonce=0,
        real_time=None
    ):

        self.index = index

        # UNIX TIME
        self.timestamp = timestamp

        # REAL TIME
        self.real_time = real_time or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # DATA
        self.waste_type = waste_type
        self.confidence = confidence

        # ĐỔI location -> status
        self.status = status

        # BLOCKCHAIN
        self.previous_hash = previous_hash
        self.nonce = nonce

        # HASH
        self.hash = self.calculate_hash()

    # =========================================
    # HASH
    # =========================================
    def calculate_hash(self):

        block_data = {

            "index": self.index,

            "timestamp": self.timestamp,

            "real_time": self.real_time,

            "waste_type": self.waste_type,

            "confidence": self.confidence,

            # đổi thành status
            "status": self.status,

            "previous_hash": self.previous_hash,

            "nonce": self.nonce
        }

        block_string = json.dumps(
            block_data,
            sort_keys=True
        ).encode()

        return hashlib.sha256(
            block_string
        ).hexdigest()

    # =========================================
    # MINING
    # =========================================
    def mine_block(self, difficulty):

        target = "0" * difficulty

        print(f"\n⛏ Mining Block {self.index}...")

        start = time()

        while not self.hash.startswith(target):

            self.nonce += 1

            self.hash = self.calculate_hash()

        end = time()

        print("✅ Block Mined")
        print("⏱ Mining Time:", round(end - start, 2), "sec")
        print("🔢 Nonce:", self.nonce)
        print("🔐 Hash :", self.hash)

    # =========================================
    # TO DICT
    # =========================================
    def to_dict(self):

        return {

            "index": self.index,

            "timestamp": self.timestamp,

            "real_time": self.real_time,

            "waste_type": self.waste_type,

            "confidence": self.confidence,

            # đổi thành status
            "status": self.status,

            "previous_hash": self.previous_hash,

            "nonce": self.nonce,

            "hash": self.hash
        }


# =========================================
# BLOCKCHAIN
# =========================================
class Blockchain:

    def __init__(
        self,
        filename="blockchain_data.json"
    ):

        self.filename = filename

        # mining difficulty
        self.difficulty = 4

        # =========================================
        # LOAD
        # =========================================
        if os.path.exists(self.filename):

            try:

                self.chain = self.load_chain()

                print("\n📂 Blockchain Loaded")

            except Exception as e:

                print("\n⚠️ Blockchain Error:", e)

                print("⚠️ Creating New Blockchain...")

                self.chain = [
                    self.create_genesis_block()
                ]

                self.save_to_file()

        else:

            self.chain = [
                self.create_genesis_block()
            ]

            self.save_to_file()

            print("\n🆕 New Blockchain Created")

    # =========================================
    # GENESIS
    # =========================================
    def create_genesis_block(self):

        genesis = Block(

            0,
            time(),
            "Genesis",
            1.0,
            "SYSTEM",
            "0"
        )

        genesis.mine_block(self.difficulty)

        return genesis

    # =========================================
    # LAST BLOCK
    # =========================================
    def get_latest_block(self):

        return self.chain[-1]

    # =========================================
    # ADD BLOCK
    # =========================================
    def add_block(
        self,
        waste_type,
        confidence,
        status="UNPROCESSED"
    ):

        latest_block = self.get_latest_block()

        new_block = Block(

            len(self.chain),

            time(),

            waste_type,

            confidence,

            # status mới
            status,

            latest_block.hash
        )

        # mine
        new_block.mine_block(
            self.difficulty
        )

        # add chain
        self.chain.append(new_block)

        # save json
        self.save_to_file()

        print("\n================================")
        print("✅ BLOCK ADDED")
        print("================================")

        print("Block:", new_block.index)

        print("Time:", new_block.real_time)

        print("Waste Type:", new_block.waste_type)

        print("Confidence:", new_block.confidence)

        # đổi status
        print("Status:", new_block.status)

        print("Nonce:", new_block.nonce)

        print("\nPrevious Hash:")
        print(new_block.previous_hash)

        print("\nHash:")
        print(new_block.hash)

        print("================================\n")

    # =========================================
    # VALIDATE
    # =========================================
    def is_chain_valid(self):

        print("\n🔎 VALIDATING BLOCKCHAIN...\n")

        for i in range(1, len(self.chain)):

            current = self.chain[i]

            previous = self.chain[i - 1]

            # hash check
            if current.hash != current.calculate_hash():

                print(f"❌ BLOCK {i} HASH INVALID")

                return False

            # link check
            if current.previous_hash != previous.hash:

                print(f"❌ BLOCK {i} LINK INVALID")

                return False

            # mining check
            if not current.hash.startswith(
                "0" * self.difficulty
            ):

                print(f"❌ BLOCK {i} NOT MINED")

                return False

        print("✅ Blockchain Valid")

        return True

    # =========================================
    # SHOW CHAIN
    # =========================================
    def show_chain(self):

        print("\n========== BLOCKCHAIN ==========\n")

        for block in self.chain:

            print("--------------------------------")

            print("Block:", block.index)

            print("Time:", block.real_time)

            print("Waste:", block.waste_type)

            print("Confidence:", block.confidence)

            # đổi status
            print("Status:", block.status)

            print("Nonce:", block.nonce)

            print("\nPrevious Hash:")
            print(block.previous_hash)

            print("\nHash:")
            print(block.hash)

            print("--------------------------------\n")

    # =========================================
    # SAVE JSON
    # =========================================
    def save_to_file(self):

        blockchain_data = []

        for block in self.chain:

            blockchain_data.append(
                block.to_dict()
            )

        with open(
            self.filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                blockchain_data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"💾 Blockchain Saved -> {self.filename}"
        )

    # =========================================
    # LOAD JSON
    # =========================================
    def load_chain(self):

        with open(
            self.filename,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        chain = []

        for item in data:

            block = Block(

                item["index"],

                item["timestamp"],

                item.get("waste_type", "Unknown"),

                item.get("confidence", 0.0),

                # đọc status mới
                item.get("status", "UNPROCESSED"),

                item.get("previous_hash", "0"),

                item.get("nonce", 0),

                item.get(
                    "real_time",
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            block.hash = item.get(
                "hash",
                block.calculate_hash()
            )

            chain.append(block)

        return chain
    def verify_chain_detail(self):

        for i in range(1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():

                return {
                    "valid": False,
                    "block": i,
                    "error": "HASH_INVALID"
                }

            if current.previous_hash != previous.hash:

                return {
                    "valid": False,
                    "block": i,
                    "error": "LINK_INVALID"
               }

            if not current.hash.startswith(
                "0" * self.difficulty
            ):

                return {
                    "valid": False,
                    "block": i,
                    "error": "NOT_MINED"
                }

        return {
            "valid": True,
            "block": None,
            "error": None
        }