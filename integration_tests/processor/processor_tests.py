"""Consensource transaction processor integration tests.

This module contains integration tests for the Consensource transaction
processor. These tests are meant to be run using the nose2 module. The
goal is to test the transaction processor's validation logic, as well
as the resulting state values for committed transactions.

Attributes:
    REST_URL (string): The URL of the Sawtooth REST API. This REST API
        should be connected to a Sawtooth validator that is running the
        Consensource transaction processor.

Todo:
    * Agent accreditation tests
    * Certificate tests
    * Organization tests
    * Request tests
    * Standard tests
    * Integrate testing framework into CI server
"""

import logging
import time
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

from protobuf import agent_pb2
from test_client import ConsensourceTestClient


LOGGER = logging.getLogger(__name__)
REST_URL = 'rest-api:8008'


def make_signer():
    """Generates a pub/priv key pair used for signing transatctions.
        Returns:
            sawtooth_signing.Signer: Wraps a public/private key pair.
    """
    context = create_context('secp256k1')
    private_key = context.new_random_private_key()
    signer = CryptoFactory(context).new_signer(private_key)
    return signer


class ConsensourceTest(unittest.TestCase):
    """Contains testing data, logic, and assertion functionality.

    This class first waits for the REST API to become available, and
    then initializes the ConsensourceTestClient and any reusable test
    data. All of the tests for the TP are defined in this class.

    See https://docs.python.org/3/library/unittest.html for more info.

    Attributes:
        client (ConsensourceTestClient): Class used to create and send
            transactions to the Sawtooth validator.
    """

    @classmethod
    def setUpClass(cls):
        wait_for_rest_api(REST_URL)
        cls.client = ConsensourceTestClient(REST_URL)

        cls.signer1 = make_signer()
        cls.signer2 = make_signer()

    # Agent Tests
    # Notes:
    #     CreateAgent validation rules:
    #         - Name is provided.
    #         - Public key is unique.
    def test_00_create_agent(self):
        """
        Tests creating a valid agent.
        """
        status_result = self.client.create_agent(
            signer=self.signer1,
            name='alice',
            timestamp=0)[0]
        invalid_txns = status_result.get('invalid_transactions')
        self.assertEqual(
            status_result['status'],
            "COMMITTED",
            invalid_txns[0]['message'] if invalid_txns else None)

        actual = self.client.fetch_agent(
            public_key=self.signer1.get_public_key().as_hex())
        expected = agent_pb2.Agent(
            public_key=self.signer1.get_public_key().as_hex(),
            name='alice',
            timestamp=0)
        self.assertEqual(
            actual,
            expected,
            "Agent was not created properly")

    def test_01_create_agent(self):
        """
        Tests creating an agent without providing a name.
        """
        status_result = self.client.create_agent(
            signer=self.signer2,
            name=None,
            timestamp=1)[0]
        invalid_txns = status_result.get('invalid_transactions')
        self.assertEqual(
            status_result['status'],
            "INVALID",
            "Transaction should be invalid if name is not provided")

        actual = invalid_txns[0]['message']
        expected = "Name was not provided"
        self.assertEqual(
            actual,
            expected,
            "Incorrect error message")

    def test_02_create_agent(self):
        """
        Tests creating an agent with an invalid name (empty string).
        """
        status_result = self.client.create_agent(
            signer=self.signer2,
            name='',
            timestamp=2)[0]
        invalid_txns = status_result.get('invalid_transactions')
        self.assertEqual(
            status_result['status'],
            "INVALID",
            "Transaction should be invalid if name is not provided")

        actual = invalid_txns[0]['message']
        expected = "Name was not provided"
        self.assertEqual(
            actual,
            expected,
            "Incorrect error message")

    def test_03_create_agent(self):
        """
        Tests creating an agent with a previously associated public key.
        """
        status_result = self.client.create_agent(
            signer=self.signer1,
            name='bob',
            timestamp=3)[0]
        invalid_txns = status_result.get('invalid_transactions')
        self.assertEqual(
            status_result['status'],
            "INVALID",
            "Transaction should be invalid if an agent with that " +
            "public key already exists")

        actual = invalid_txns[0]['message']
        expected = "Agent already exists: {}".format(
            self.signer1.get_public_key().as_hex())
        self.assertEqual(
            actual,
            expected,
            "Incorrect error message")


def wait_for_rest_api(endpoint, tries=5):
    """Pause the program until the given REST API endpoint is available.
    Args:
        endpoint (str): A list of host:port strings.
        tries (int, optional): The number of attempts to request the url for
            availability.
    """
    http = 'http://'
    url = endpoint if endpoint.startswith(http) else http + endpoint
    wait_until_status(
        '{}/blocks'.format(url),
        status_code=200,
        tries=tries)


def wait_until_status(url, status_code=200, tries=5):
    """Pause the program until the given url returns the required status.
    Args:
        url (str): The url to query.
        status_code (int, optional): The required status code. Defaults to 200.
        tries (int, optional): The number of attempts to request the url for
            the given status. Defaults to 5.
    Raises:
        AssertionError: If the status is not received in the given number of
            tries.
    """
    attempts = tries
    while attempts > 0:
        try:
            response = urlopen(url)
            if response.getcode() == status_code:
                return

        except HTTPError as err:
            if err.code == status_code:
                return

            LOGGER.debug('failed to read url: %s', str(err))
        except URLError as err:
            LOGGER.debug('failed to read url: %s', str(err))

        sleep_time = (tries - attempts + 1) * 2
        LOGGER.debug('Retrying in %s secs', sleep_time)
        time.sleep(sleep_time)

        attempts -= 1

    raise AssertionError(
        "{} is not available within {} attempts".format(url, tries))
