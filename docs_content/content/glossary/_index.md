+++
title = "Glossary"
weight = 3
sort_by = "weight"
+++

Sawtooth
========

This glossary defines terms and concepts related to Sawtooth.

**Application**  
A group of components, including a transaction processor and transaction submission client, that run on top of the Sawtooth platform.

**Batch**  
A group of one or more transactions which comprise the atomic unit of state change for the blockchain. If one transaction in the batch fails, they all fail.

**Blockchain**  
A group of cryptographically linked records. Each block contains a list of batches, a state root hash of the state created by the application of the block's transactions, and the ID of the previous block in the blockchain.

**Client**  
The application component which is responsible for displaying blockchain data and/or submitting transactions. A client can be in the form of a webapp, mobile application, IoT sensor, etc.

**Consensus**  
A protocol used to establish agreement regarding state in a blockchain system. In Sawtooth, the consensus mechanism is dynamic and pluggable, meaning that the consensus algorithm used by all nodes on the chain can be altered by submitting a transaction to change the on-chain setting.

**Events**  
Data broadcasted by the validator when blocks are committed. Clients can choose to subscribe to certain events. There are two core Sawtooth events, ``sawtooth/block-commit`` and ``sawtooth/state-delta``. ``sawtooth/block-commit`` events contain data about the block that was just committed, and ``sawtooth/state-delta`` contains all state changes that occurred for a given address. Applications can define additional events if necessary. 

**Fork**  
A situation where previously valid data is now considered to be invalid by the consensus mechanism.

**Genesis Block**  
The first block of the blockchain.

**Hyperledger**  
A multi-project open source collaborative effort hosted by The Linux Foundation, created to advance cross-industry blockchain technologies.

**Node**  
A participant in the Sawtooth network. Each node in a Sawtooth network consists of a validator and an identical set of transaction processors.

**Reporting Database**  
A database which contains a copy of state, typically constructed by a state delta subscription client. This allows clients to richly query the blockchain data, rather than relying on the Merkle-Radix tree database on the validator directly. The reporting database may utilize the Type 2 Slowly Changing Dimensions pattern to handle fork resolution.

**REST API**  
Used as a layer on top of Sawtooth's ZMQ connection interface, to allow clients to send and receive data from the validator using HTTP/JSON or octet-stream. May also connect to an off-chain reporting database to allow for rich querying.

**Sawtooth**  
An enterprise blockchain platform for building distributed applications. Sawtooth is designed to be highly modular, and separates the blockchain and consensus logic from the application domain.

**State**  
A view of all transactions applied up to a given block. In Sawtooth, state is represented as a Merkle-Radix tree. It can be thought of as a cache, as it can be regenerated at any time by executing the transactions in the blockchain.

**State Delta Subscriber**  
A client which subscribes to ``sawtooth/state-delta`` events in order to store a copy of state in an off-chain database.

**Transaction**  
A state transition function defined by the rules of the application. All transactions follow the format: ``T(S) -> S'``.

**Transaction Processor**  
The component that defines and executes the business logic of the application.

**Validator**  
The core component of the Sawtooth platform. The validator is in charge of validating incoming batches, creating blocks, broadcasting batches and blocks, maintaining consensus throughout the Sawtooth network, coordinating communication with other validators, and sending transactions to attached transaction processors.

Creg
====

This glossary defines terms and concepts related to the Certificate Registry (Creg) application and business domain.

**Agent**  
An entity who acts on behalf of an organization on the blockchain network. Associated with a public/private key pair which is used to sign transactions.

**Certifying Body**  
Also known as an auditing body, a certifying body is accredited by a standards body to issue certificates of a specified standard to factories.

**Certificate**  
A document asserting that a factory has met the quality/regulatory requirements for a certain certification standard.

**Factory**  
An entity that is able to hold certificates and request certification.

**Standard**  
A set of requirements set by a standards body. Certifications must be issued against a certain certification standard.

**Standards Body**  
Describes an organization that is responsible for developing certification standards and accrediting certifying bodies to issue certifications against their standards.

**Organization**  
Describes a factory, certifying body, or standards body. Organizations have lists of agents who are authorized to act on their behalf.

**Request**  
Requests for certification by a specific standard. Requests are created on behalf of factories. They can be approved by agents associated with certifying bodies that are accredited to audit against the requested standard.
