import time
import hashlib
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

MANUFACTURER_ID = "Manufacturer_A"
MAX_TRANSACTIONS_PER_BLOCK = 2
REWARD = 5  # Defined reward for a block validation

class Transaction:
    def __init__(self, distributor_id, client_id, product_id, amount=None):
        self.product_id = product_id  # Unique identifier for the product
        self.manufacturer_id = MANUFACTURER_ID
        self.distributor_id = distributor_id
        self.client_id = client_id
        self.amount = amount
        self.status = "Created"
        self.timestamps = {"created": time.time(), "dispatched": None, "received": None}

    def distributor_dispatched(self):
        self.status = "Dispatched"
        self.timestamps["dispatched"] = time.time()

    def client_received(self):
        self.status = "Received"
        self.timestamps["received"] = time.time()

    def confirm_delivery(self):
        self.status = "Confirmed"


# Define the Block class to represent individual blocks in the blockchain.
class Block:
    # Constructor initializes with previous block (for linkage) and list of transactions.
    def __init__(self, previous_block, transactions=[]):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_block.hash if previous_block else None
        # Calculate the Merkle root for the list of transactions.
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()  # Block's own hash

    # Calculate the block's hash using its attributes.
    def calculate_hash(self):
        return hashlib.sha256(
            str(self.timestamp).encode()
            + str(self.merkle_root).encode()
            + str(self.previous_hash).encode()
        ).hexdigest()

    # Calculate the Merkle root for the block's transactions.
    def calculate_merkle_root(self):
        transaction_hashes = [
            hashlib.sha256(str(tx.__dict__).encode()).hexdigest()
            for tx in self.transactions
        ]
        if not transaction_hashes:
            return hashlib.sha256("No transactions".encode()).hexdigest()
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            transaction_hashes = [
                hashlib.sha256(
                    (transaction_hashes[i] + transaction_hashes[i + 1]).encode()
                ).hexdigest()
                for i in range(0, len(transaction_hashes), 2)
            ]
        return transaction_hashes[0]


# Node class represents participants in the network that can stake coins for PoS.
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.staked_coins = 0

    # Method to stake coins.
    def stake_coins(self, amount):
        self.staked_coins += amount

    # Method to receive a reward.
    def receive_reward(self, reward_amount):
        self.staked_coins += reward_amount

class Client:
    def __init__(self, client_id, deposit):
        self.client_id = client_id
        self.balance = deposit

class Distributor:
    def __init__(self, distributor_id, deposit):
        self.distributor_id = distributor_id
        self.balance = deposit



    


# Blockchain class represents the complete blockchain.
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.confirmed_transactions = []
        self.nodes = []
        self.clients = {}
        self.distributors = {}
        self.manufacturer = None

    def register_client(self, client_id, deposit):
        if client_id not in self.clients:
            self.clients[str(client_id)] = Client(client_id, deposit)
            print(f"Client {client_id} registered with a deposit of {deposit}.")
        else:
            print(f"Client {client_id} is already registered.")

    def register_distributor(self, distributor_id, deposit):
        distributor_id = str(distributor_id)
        if distributor_id not in self.distributors:
            self.distributors[distributor_id] = Distributor(distributor_id, deposit)
            print(f"Distributor {distributor_id} registered with a deposit of {deposit}.")
        else:
            print(f"Distributor {distributor_id} is already registered.")

    def register_manufacturer(self, deposit):
        if not self.manufacturer:
            self.manufacturer = {"id": MANUFACTURER_ID, "deposit": deposit}
            print(f"Manufacturer {MANUFACTURER_ID} registered with a deposit of {deposit}.")
        else:
            print("Manufacturer is already registered.")

    # Create the initial block in the blockchain without any transactions or previous hash.
    def create_genesis_block(self):
        return Block(None, [])

    def can_add_transaction(self, transaction):
        for t in self.pending_transactions:
            if t.distributor_id == transaction.distributor_id:
                return False
        return True
    
    def display_balances(self):
        print("\nDistributors' Balances:")
        for distributor_id, distributor in self.distributors.items():
            print(f"Distributor {distributor_id}: {distributor.balance} units")

        print("\nClients' Balances:")
        for client_id, client in self.clients.items():
            print(f"Client {client_id}: {client.balance} units")

        if self.manufacturer:
            print(f"\nManufacturer's Balance: {self.manufacturer['deposit']} units")



    # Add a transaction to pending transactions if the distributor doesn't have a pending transaction.
    def add_transaction(self, transaction):
        if not self.can_add_transaction(transaction):
            print(f"Distributor {transaction.distributor_id} has an unconfirmed transaction!")
            return
        self.pending_transactions.append(transaction)
        print(f"Transaction added for Distributor {transaction.distributor_id} to Client {transaction.client_id}")
    
    def display_pending_transactions(self):
        if not self.pending_transactions:
            print("No pending transactions.")
            return

        print("\nPending Transactions:")
        for tx in self.pending_transactions:
            print(f"From {tx.manufacturer_id} to Client {tx.client_id} via Distributor {tx.distributor_id} - Status: {tx.status}")


    # Register a new node to the blockchain network.
    def register_node(self, node):
        self.nodes.append(node)

    # Select the next node (validator) based on the highest staked coins.
    def get_next_validator(self):
        if not self.nodes:
            return None
        validator = max(self.nodes, key=lambda x: x.staked_coins)
        return validator

    # Add a new block with current confirmed transactions to the blockchain.
    def add_block(self):
        validator = self.get_next_validator()
        if not validator:
            print("No validators available.")
            return
        print(f"Node {validator.node_id} has been chosen to validate the block!")
        new_block = Block(self.chain[-1], self.confirmed_transactions)
        self.chain.append(new_block)
        self.confirmed_transactions = []  # Clear the list of confirmed transactions

         # Reward the validator
        validator.receive_reward(REWARD)
        print(f"Node {validator.node_id} has received a reward of {REWARD} coins!")

    # Display details of each block in the blockchain.
    def display_chain(self):
        for block in self.chain:
            print("Timestamp:", block.timestamp)
            print("Merkle Root:", block.merkle_root)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print("\n")

    def verify_transactions(self):
        transactions_to_remove = []
        transactions_to_confirm = []

        # Loop through each transaction to check for validity
        for transaction in self.pending_transactions:
        
            # Case a: Distributor dispatched, client denies receiving
            if transaction.status == "Dispatched" and not transaction.timestamps["received"]:
                print(f"Discrepancy detected for Product {transaction.product_id}: Distributor claims dispatched but Client denies receiving!")
                self.clients[str(transaction.client_id)].balance -= 1000  # Deducting a hypothetical amount from Client
                transactions_to_remove.append(transaction)  # Add this transaction to the list to be removed
                continue  # Skip further processing for this transaction

            # Case b: Neither distributor dispatches nor client claims received
            elif not transaction.timestamps["dispatched"] and not transaction.timestamps["received"]:
                print(f"Discrepancy detected for Product {transaction.product_id}: Distributor did not dispatch and Client did not receive!")
                self.distributors[str(transaction.distributor_id)].balance -= 1000  # Deducting a hypothetical amount from Distributor
                transactions_to_remove.append(transaction)  # Add this transaction to the list to be removed
                continue  # Skip further processing for this transaction

            # If no discrepancy found, add to transactions_to_confirm
            else:
                transactions_to_confirm.append(transaction)

        # Transfer the valid transactions to confirmed_transactions
        for tx in transactions_to_confirm:
            self.clients[str(tx.client_id)].balance -= tx.amount  # Deducting the transaction amount from the client
            self.confirmed_transactions.append(tx)
            self.pending_transactions.remove(tx)
            print(f"Transaction for Product {tx.product_id} is verified and added to confirmed transactions!")

        # Remove invalid transactions
        for tx in transactions_to_remove:
            self.pending_transactions.remove(tx)



def generate_qr(transaction):
    tx_string = f"""Manufacturer: {transaction.manufacturer_id}, 
                    Distributor: {transaction.distributor_id}, 
                    Client: {transaction.client_id}, 
                    Status: {transaction.status},
                    Created: {time.ctime(transaction.timestamps['created'])},
                    Dispatched: {time.ctime(transaction.timestamps['dispatched']) if transaction.timestamps['dispatched'] else 'N/A'},
                    Received: {time.ctime(transaction.timestamps['received']) if transaction.timestamps['received'] else 'N/A'}"""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(tx_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"transaction_{transaction.distributor_id}_{transaction.client_id}.png")
    img.show()


def decode_qr(image_path):
    decoded_objects = decode(Image.open(image_path))
    for obj in decoded_objects:
        print(obj.data.decode("utf-8"))


def user_interface():
    blockchain = Blockchain()

    while True:
        print("\nChoose an action:")
        print("1. Register Client")
        print("2. Register Manufacturer")
        print("3. Register Distributor")
        print("4. Create Transaction")
        print("5. Display QR Code for a Transaction")
        print("6. Start Mining Blocks")
        print("7. Display Pending Transactions")
        print("8. Display Blockchain")
        print("9. Dispatch the Product")
        print("10. Receive the Product")
        print("11. Register a Validator Node")
        print("12. Verify and Add Transaction")
        print("13. Display Balances")
        print("14. Exit")

        choice = input("Enter your choice (1-13): ")

        if choice == "1":
            client_id = input("Enter client ID: ")
            deposit = float(input("Enter deposit amount: "))
            blockchain.register_client(client_id, deposit)

        elif choice == "2":
            deposit = float(input("Enter deposit amount for Manufacturer: "))
            blockchain.register_manufacturer(deposit)

        elif choice == "3":
            distributor_id = input("Enter distributor ID: ")
            deposit = float(input("Enter deposit amount: "))
            blockchain.register_distributor(distributor_id, deposit)

        elif choice == "4":
            distributor_id = input("Enter distributor ID for transaction: ")
            client_id = input("Enter client ID for transaction: ")
            product_id = input("Enter product ID for the transaction: ")
            amount = float(input("Enter transaction amount: "))
            new_transaction = Transaction(distributor_id, client_id, product_id, amount)

            if blockchain.can_add_transaction(new_transaction):
                blockchain.pending_transactions.append(new_transaction)
                print("Transaction added to pending transactions.")
            else:
                print(f"Cannot create transaction: Distributor {distributor_id} already has a pending transaction!")

        elif choice == "5":
            distributor_id = input("Enter distributor ID of the transaction: ")
            client_id = input("Enter client ID of the transaction: ")

            # Logic to retrieve the transaction and then generate its QR code.
            target_transaction = None

            # First, check in pending transactions
            for tx in blockchain.pending_transactions:
                if tx.distributor_id == distributor_id and tx.client_id == client_id:
                    target_transaction = tx
                    break

            # If not found in pending transactions, check in confirmed transactions
            if not target_transaction:
                for tx in blockchain.confirmed_transactions:
                    if tx.distributor_id == distributor_id and tx.client_id == client_id:
                        target_transaction = tx
                        break

            if target_transaction:
                generate_qr(target_transaction)
                print(f"QR code for the transaction between distributor {distributor_id} and client {client_id} is displayed.")
            else:
                print("No such transaction found!")

        elif choice == "6":
            blockchain.add_block()

        elif choice == "7":
            blockchain.display_pending_transactions()

        elif choice == "8":
            blockchain.display_chain()

        elif choice == "9":
            distributor_id = input("Enter distributor ID for dispatch: ")
            for tx in blockchain.pending_transactions:
                if tx.distributor_id == distributor_id and tx.status == "Created":
                    tx.distributor_dispatched()
                    print(f"Product dispatched by {distributor_id} for transaction with client {tx.client_id}")
                    break

        elif choice == "10":
            client_id = input("Enter client ID for receiving product: ")
            for tx in blockchain.pending_transactions:
                if tx.client_id == client_id and tx.status == "Dispatched":
                    tx.client_received()
                    print(f"Product received by {client_id} for transaction with distributor {tx.distributor_id}")
                    break

        elif choice == "11":
            node_id = input("Enter the Node ID for the validator: ")
            staked_amount = float(input("Enter the amount of coins the node will stake: "))
            new_node = Node(node_id)
            new_node.stake_coins(staked_amount)
            blockchain.register_node(new_node)
            print(f"Validator Node {node_id} registered and staked {staked_amount} coins.")

        elif choice == "12":
            blockchain.verify_transactions()

        elif choice == "13":
            blockchain.display_balances()

        elif choice == "14":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please choose between 1 and 12.")

user_interface()