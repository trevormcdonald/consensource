"""Client API for the Consensource application.

This client is meant to act as an interface between the Sawtooth REST
API, and an integration test suite. It is responsible for transaction
creation, submission, and fetching data using the Sawtooth REST API.

Todo:
    * Extend transaction creation functionality across all transactions
    * Extend addressing functionality across all data types
    * Extend fetching functionality across all data types
"""

from base64 import b64decode
import hashlib

from sawtooth_cli.rest_client import RestClient
from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import transaction_pb2

from protobuf import agent_pb2
from protobuf import payload_pb2


class ConsensourceTestClient():
    """Client application for Consensource used for testing.

    This class defines methods for each transaction and data type
    covered by the integration test suite.

    Args:
        url (str): URL of the Sawtooth REST API.

    Attributes:
        _client (RestClient): Defines functions for interfacing with
            the Sawtooth REST API.
        _family_name (str): Name of the application. This should match
            the family name in the transaction processor's metadata.
        _family_version (str): Version of the application. This should
            match the family version in the transaction processor's
            metadata.
        _namespace (str): First 6 chars of the family name
    """

    def __init__(self, url):
        self._client = RestClient(base_url="http://{}".format(url))
        self._family_name = 'certificate_registry'
        self._family_version = '0.1'
        self._namespace = hashlib.sha256(
            self._family_name.encode('utf-8')).hexdigest()[:6]

    def create_agent(self, signer, name, timestamp):
        """Creates and submits a create agent transaction.
        Args:
            signer (Signer): Transaction and batch signer.
            name (str): Name of the agent.
            timestamp(int): Unix timestamp at which the transaction is
                being submitted.
        Returns:
            list of dict: Dicts with 'id' and 'status' properties.
        """
        agent_address = self._make_agent_address(
            signer.get_public_key().as_hex())

        payload = payload_pb2.CertificateRegistryPayload(
            action=payload_pb2.CertificateRegistryPayload.CREATE_AGENT,
            create_agent=payload_pb2.CreateAgentAction(
                name=name, timestamp=timestamp))

        batch = self._make_batch(
            payload=payload,
            inputs=[agent_address],
            outputs=[agent_address],
            signer=signer)

        return self._send_batch(batch)

    def fetch_agent(self, public_key):
        """Fetches an agent resource from state.
        Args:
            public_key (str): Public key that identifies the agent.
        Returns:
            agent_pb2.Agent: Protobuf message describing the agent.
        """
        agent_address = self._make_agent_address(public_key)
        state = self._client.list_state(subtree=agent_address)
        if state:
            container = agent_pb2.AgentContainer()
            container.ParseFromString(b64decode(state['data'][0]['data']))
            for agent in container.entries:
                if agent.public_key == public_key:
                    return agent
        return None

    def _make_agent_address(self, public_key):
        """Addressing method for agents.
        """
        return self._namespace + '00' + '00' + hashlib.sha256(
            public_key.encode('utf-8')).hexdigest()[:60]

    def _make_batch(self, payload, inputs, outputs, signer):
        """Creates and signs a batch.
        """
        signer_public_key = signer.get_public_key().as_hex()
        payload_bytes = payload.SerializeToString()

        txn_header = transaction_pb2.TransactionHeader(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=signer_public_key,
            batcher_public_key=signer_public_key,
            payload_sha512=hashlib.sha512(payload_bytes).hexdigest())
        txn_header_bytes = txn_header.SerializeToString()
        txn = transaction_pb2.Transaction(
            header=txn_header_bytes,
            header_signature=signer.sign(txn_header_bytes),
            payload=payload_bytes)

        batch_header = batch_pb2.BatchHeader(
            signer_public_key=signer_public_key,
            transaction_ids=[txn.header_signature])
        batch_header_bytes = batch_header.SerializeToString()
        batch = batch_pb2.Batch(
            header=batch_header_bytes,
            header_signature=signer.sign(batch_header_bytes),
            transactions=[txn])

        return batch

    def _send_batch(self, batch):
        """Submits a batch to the validator.

        After submission, the client will query the REST API again to
        retrieve the commit status of the batch.
        """
        batch_id = batch.header_signature
        batch_list = batch_pb2.BatchList(batches=[batch])
        self._client.send_batches(batch_list)
        return self._client.get_statuses([batch_id], wait=10)
