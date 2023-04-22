# tests/test_database.py

from typing import Dict, Any, List

import pytest
from dotenv import dotenv_values

from backend.database import MongoAdapter


config = dotenv_values(".env")


"""
Test class for database.py module contains test cases to check functionality
of interaction with MongoDB
test run terminal command (with activated venv):
python -m pytest -rA -v --tb=line test_database.py --cov-report term-missing --cov=sources
"""


class TestDatabase:
    """
    Test class to check functionality of endpoints
    which are working with database via MongoDB Adapter
    """

    @classmethod
    def setup_class(cls):
        """
        Prepare test environment
        """
        raise NotImplementedError

    @pytest.mark.mongodb
    @pytest.mark.parametrize("insertable_data, expected", [
        ({"test_key_1": "test_value_1", "issue": "test_issue_1"}, True),
        ({"test_key_2": "test_value_2", "issue": "test_issue_2"}, True),
    ])
    def test_insert_db_entry(
        self,
        _mongo_adapter_book_shelf_collection: MongoAdapter,
        insertable_data: Dict[str, Any],
        expected: bool
    ):
        """
        Test case checks the functionality of insert_db_entry() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param insertable_data: test data in JSON format
        :type insertable_data: Dict[str, Any]
        :param expected: bool to check the result against
        :type expected: bool
        """
        inserted_id = _mongo_adapter_book_shelf_collection.insert_db_entry(
            data=insertable_data
        )
        extracted_data = _mongo_adapter_book_shelf_collection.read_first_match(
            data=insertable_data
        )
        assert inserted_id
        assert (insertable_data == extracted_data) == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("index_name, replacing_data, expected", [
        ("issue", {"test_key_1": "replacing_test_value_1", "issue": "test_issue_1"}, False),
        ("issue", {"test_key_2": "replacing_test_value_2", "issue": "test_issue_2"}, False),
        ("issue", {"test_key_3": "replacing_test_value_3", "issue": "test_issue_3"}, True),
        ("issue", {"test_key_4": "replacing_test_value_4", "issue": "test_issue_4"}, True),
        ("issue", {"test_key_5": "replacing_test_value_5", "issue": "test_issue_5"}, True),
    ])
    def test_silent_replace_db_entry(
            self,
            _mongo_adapter_book_shelf_collection: MongoAdapter,
            index_name: str,
            replacing_data: Dict[str, Any],
            expected: bool
    ):
        """
        Test case checks the functionality of silent_replace_db_entry() method
        
        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param index_name: key used as index in DB collection
        :type index_name: str
        :param replacing_data: test data in JSON format
        :type replacing_data: Dict[str, Any]
        :param expected: bool to check the result against
        :type expected: bool
        """
        upserted_id = _mongo_adapter_book_shelf_collection.silent_replace_db_entry(
            index_name=index_name,
            data=replacing_data
        )
        print(f"upserted ID: {upserted_id}")
        assert bool(upserted_id) == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("index_name, entry_id, matching_data, expected", [
        ("issue", "test_issue_1", {"test_key_1": "replacing_test_value_1", "issue": "test_issue_1"}, True),
        ("issue", "test_issue_2", {"test_key_2": "replacing_test_value_2", "issue": "test_issue_2"}, True),
        ("issue", "test_issue_3", {"test_key_3": "replacing_test_value_3", "issue": "test_issue_3"}, True),
        ("issue", "unexpected_issue", {"unexpected_key": "unexpected_value", "issue": "unexpected_issue"}, False),
    ])
    def test_extract_db_entry(
            self,
            _mongo_adapter_book_shelf_collection: MongoAdapter,
            index_name: str,
            entry_id: str,
            matching_data: Dict[str, Any],
            expected: bool
    ):
        """
        Test case checks the functionality of extract_db_entry() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param index_name: key used as index in DB collection
        :type index_name: str
        :param entry_id: ID of the DB entry
        :type entry_id: str
        :param matching_data: test data in JSON format
        :type matching_data: Dict[str, Any]
        :param expected: bool to check the result against
        :type expected: bool
        """
        extracted_data = _mongo_adapter_book_shelf_collection.extract_db_entry(
            index_name=index_name,
            entry_id=entry_id
        )
        print(f"Extracted data: {extracted_data}")
        print(f"Matching data: {matching_data}")
        assert bool(extracted_data) == expected
        if extracted_data: 
            assert (matching_data.items() <= extracted_data.items()) == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("matching_data, expected", [
        ({"test_key_1": "replacing_test_value_1", "issue": "test_issue_1"}, True),
        ({"test_key_2": "replacing_test_value_2", "issue": "test_issue_2"}, True),
        ({"test_key_3": "replacing_test_value_3", "issue": "test_issue_3"}, True),
    ])
    def test_read_first_match(
        self, 
        _mongo_adapter_book_shelf_collection: MongoAdapter, 
        matching_data: Dict[str, Any], 
        expected: bool
    ):
        """
        Test case checks the functionality of read_first_match() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param matching_data: test data in JSON format
        :type matching_data: Dict[str, Any]
        :param expected: bool to check the result against
        :type expected: bool
        """
        extracted_data = _mongo_adapter_book_shelf_collection.read_first_match(
            data=matching_data
        )
        assert (matching_data.items() <= extracted_data.items()) == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("collection_names, expected", [
        ([config["TEST_MONGODB_BOOK_SHELF_COLLECTION_NAME"], config["TEST_MONGODB_USER_COLLECTION_NAME"]], True),
        (["some_fake_collection_name", "another_fake_collection_name"], False)
    ])
    def test_get_collection_names(
            self,
            _mongo_adapter_book_shelf_collection: MongoAdapter,
            collection_names: List[str],
            expected: bool
    ):
        """
        Test case checks the functionality of get_collection_names() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param collection_names: list of collections to check their inclusion
        :type collection_names: List[str]
        :param expected: bool to check the result against
        :type expected: bool
        """
        extracted_collection_names = _mongo_adapter_book_shelf_collection.get_collection_names()
        print(f"extracted_collection_names: {extracted_collection_names}")
        assert (all([
            collection_name in extracted_collection_names
            for collection_name in collection_names
        ])) == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("index_name, entry_id, expected", [
        ("issue", "test_issue_1", 1),
        ("issue", "test_issue_2", 1),
        ("issue", "test_issue_3", 1),
    ])
    def test_delete_db_entry(
            self,
            _mongo_adapter_book_shelf_collection: MongoAdapter,
            index_name: str,
            entry_id: str,
            expected: int
    ):
        """
        Test case checks the functionality of delete_db_entry() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param index_name: key used as index in DB collection
        :type index_name: str
        :param entry_id: ID of the DB entry
        :type entry_id: str
        :param expected: expected value of deleted_count parameter
        :type expected: int
        """
        deletion_result = _mongo_adapter_book_shelf_collection.delete_db_entry(
            index_name=index_name,
            entry_id=entry_id
        )
        assert deletion_result.deleted_count == expected

    @pytest.mark.mongodb
    @pytest.mark.parametrize("deletable_data", [
        ({"test_key_4": "replacing_test_value_4", "issue": "test_issue_4"}),
        ({"test_key_5": "replacing_test_value_5", "issue": "test_issue_5"}),
    ])
    def test_find_one_and_delete(
            self,
            _mongo_adapter_book_shelf_collection: MongoAdapter,
            deletable_data: Dict[str, Any],
    ):
        """
        Test case checks the functionality of find_one_and_delete() method

        :param _mongo_adapter_book_shelf_collection: instance of MongoAdapter class
        :type _mongo_adapter_book_shelf_collection: MongoAdapter
        :param deletable_data: test data in JSON format
        :type deletable_data: Dict[str, Any]
        """
        deleted_document = _mongo_adapter_book_shelf_collection.find_one_and_delete(
            data=deletable_data
        )
        assert deletable_data.items() <= deleted_document.items()

    @classmethod
    def teardown_class(cls):
        """
        Tidy up test environment
        """
        raise NotImplementedError
