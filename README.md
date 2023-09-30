# Blockchain Supply Chain Management System

This system utilizes a basic blockchain implementation to track transactions in a supply chain environment, primarily between manufacturers, distributors, and clients. The system also includes QR code generation for transactional data and a verification mechanism.

## Functions

### 1. Transaction Class

- `__init__`: Initializes a new transaction with distributor and client details, the product involved, and its status.
- `distributor_dispatched`: Updates the transaction status to "Dispatched".
- `client_received`: Updates the transaction status to "Received".
- `confirm_delivery`: Confirms the delivery of the product.

### 2. Block Class

- `__init__`: Initializes a new block with the provided transactions and previous block's hash.
- `calculate_hash`: Calculates the hash of the block using its attributes.
- `calculate_merkle_root`: Calculates the Merkle root of the block's transactions.

### 3. Node Class

- `__init__`: Initializes a new node with its ID.
- `stake_coins`: Enables the node to stake coins.
- `receive_reward`: Rewards the node for block validation.

### 4. Client & Distributor Classes

- `__init__`: Registers a new client or distributor with an ID and deposit amount.

### 5. Blockchain Class

- `register_client`: Registers a new client in the system.
- `register_distributor`: Registers a new distributor in the system.
- `register_manufacturer`: Registers a manufacturer.
- `create_genesis_block`: Creates the first block in the blockchain.
- `can_add_transaction`: Checks if a transaction can be added based on the distributor.
- `display_balances`: Displays the balances of distributors, clients, and the manufacturer.
- `add_transaction`: Adds a transaction to the list of pending transactions.
- `display_pending_transactions`: Displays all pending transactions.
- `register_node`: Adds a node (validator) to the blockchain.
- `get_next_validator`: Chooses the next node for validation based on staked coins.
- `add_block`: Adds a new block with confirmed transactions to the blockchain.
- `display_chain`: Displays details of each block in the blockchain.
- `verify_transactions`: Verifies pending transactions and either confirms or removes them.

### 6. QR Functionality

- `generate_qr`: Generates a QR code containing the details of a transaction.
- `decode_qr`: Decodes and displays the contents of a QR code.

## User Interface

The user interface provides a simple command-line menu for the user to interact with the blockchain system. Through the menu, users can register clients and distributors, create transactions, generate QR codes, and more.

---

This README provides an overview of the functions and methods available in the blockchain system. More detailed documentation can be added as necessary for each function, especially if the codebase expands or more features are added in the future.