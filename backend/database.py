# backend/database.py

from typing import Any, Optional, Dict, List, AnyStr, Tuple

import pymongo
from pydantic import BaseModel, Field


class AuthCredentials(BaseModel):
    username: str = Field(..., example="username")
    password: str = Field(..., example="password")
    auth_source: str = Field(..., example="db_name")
    auth_mechanism: str = Field(..., example="DEFAULT")


class MongoAdapter:

    def __init__(
            self,
            host: AnyStr,
            port: AnyStr,
            db_name: AnyStr,
            collection_name: AnyStr,
            requires_auth: Optional[bool] = True,
            username: Optional[AnyStr] = None,
            password: Optional[AnyStr] = None,
            auth_source: Optional[AnyStr] = None,
            auth_mechanism: Optional[AnyStr] = "DEFAULT",
            recreate_indexes: Optional[bool] = True,
            required_index_params: Optional[List[Tuple[str, bool]]] = None,
            logger: Optional[Any] = None
    ):
        self.host: AnyStr = host
        self.port: AnyStr = port,
        self.db_name: AnyStr = db_name,
        self.collection_name: AnyStr = collection_name,
        self.requires_auth: bool = requires_auth
        self.username: AnyStr = username
        self.password: AnyStr = password
        self.auth_source: AnyStr = self.db_name
        self.client: pymongo.MongoClient
        if auth_source: self.auth_source = auth_source
        self.auth_mechanism = auth_mechanism
        self.recreate_indexes: bool = recreate_indexes
        self.logger: Any = logger
        self.required_index_params: List[Tuple[str, bool]] = [("book_id", True)]

        if required_index_params: self.required_index_params = required_index_params
        
        if self.recreate_indexes: self.recreate_required_indexes()


    def __str__(self):
        return """
            The MongoAdapter class is used to control and support the work with MongoDB collections executed for 
            FastAPI Demo Project service purposes.
            Supports either usage with the MongoDB that requires authentication (accepts username, password, 
            auth_source, auth_mechanism if bool flag 'requires_auth' passed as True).
            Accepts passing custom 'required_index_params' in the proper format to ensure that important indexes are set 
            for the given collection (passes <[("book_id", True)]> as 'required_index_params' by default).
            Automatically calls inner method 'recreate_required_indexes' to ensure that all needed indexes will be set.
            Allows turning off automatic indexes recreation by manual passing False to the bool flag 
            'recreate_indexes' (True by default).
        """
    
    def __repr__(self):
        return f"""
            {self.__class__.__name__}({self.host}, {self.port}, {self.db_name}, {self.collection_name}, 
            {self.requires_auth if self.requires_auth else ''}, {self.username if self.username else ''}, 
            {self.password if self.password else ''}, {self.auth_source if self.auth_source else ''}, 
            {self.auth_mechanism if self.auth_mechanism else ''}, {self.logger if self.logger else ''})
        """
    
    def init_mongo_client(self):
        """_summary_
        """
        if self.requires_auth:
            auth_credentials = AuthCredentials(
                username=self.username,
                password=self.password,
                auth_source=self.auth_source,
                auth_mechanism=self.auth_mechanism
            )
            self.client = pymongo.MongoClient(
                host=self.host,
                port=self.port,
                **auth_credentials.__dict__
            )
        else:
            self.client = pymongo.MongoClient(
                host=self.host,
                port=self.port
            )

    def recreate_required_indexes(self) -> None:
        """
        Checks that required index names exist within the collection, restores them if they does not exist yet,
        and marks selected indexes as either unique to allow only unique entries in DB or not unique
        (depending on developer choice)

        :param required_index_params: list of tuples of the following format:
                                    [("<index_name>", <uniqueness_bool>), ("<index_name>", <uniqueness_bool>)],
                                    where <index_name> indicates required index name, while <uniqueness_bool> flag
                                    marks if required index should be unique
        :type required_index_params: List[Tuple[str, bool]]
        :return None:
        """
        # extract currently existing indexes from the DB collection
        db_index_names_tuple = tuple(dict(self.collection.index_information()).keys())
        if self.logger: self.logger.debug(
            f"There are the following indexes {self.collection.name} within the collection: {', '.join(db_index_names_tuple)}"
        )
        # check that self.required_index_params value is valid, else return None
        if not isinstance(self.required_index_params, list):
            raise ValueError(
                f"Invalid value was passed as <required_index_params> or the format is not compatible with the requirements: "
                f"List[Tuple[str, bool]]"
            )
        # iterate over List[Tuple[str, bool]]
        for required_index_data_piece in self.required_index_params:
            if not isinstance(required_index_data_piece, tuple) or len(required_index_data_piece) != 2:
                raise ValueError(
                    f"One of the elements of <required_index_params> has invalid value or the format is not compatible with the requirements: "
                    f"Tuple[str, bool], or there were more than 2 elements passed within the tuple"
                )
            required_index_name, uniqueness_bool = required_index_data_piece
            # check if need to restore absent index name
            if required_index_name not in db_index_names_tuple:
                if self.logger: self.logger.warning(
                    f"THe following index is required for the work: {required_index_name}, although it is absent in the collection. "
                    f"Required index will be restored!"
                )
                self.collection.create_index(
                    [(required_index_name, pymongo.ASCENDING)],
                    unique=uniqueness_bool,
                    name=required_index_name
                )
        
    def insert_db_entry(self, data: Dict[str, Any]) -> Any:
            """
            Writes document in the collection, returning _id of inserted document

            :param Dict[str, Any] data: document to be written in DB
            :return Any: _id of inserted entry
            """
            return self.collection.insert_one(data).inserted_id

    def silent_replace_db_entry(self, index_name: str, data: Dict[str, Any]) -> Any:
        """
        Silently replaces (updates and inserts) DB entry with new data piece by given index name.
        If no DB entry is found by the filter within the collection, creates DB entry with new data piece without
        raising exception.

        :param str index_name: index name used to filter data in DB collection
        :param Dict[str, Any] data: new data piece
        :raises ValueError: if number of modified entries in DB collection is not equal to 1, raises ValueError
        :return Any upserted_id: the _id of the new document if a matching document did not exist and
                                inserting a new document took place. Otherwise None
        """
        q_filter = {index_name: data[index_name]}
        result = self.collection.replace_one(filter=q_filter, replacement=data, upsert=True)
        if result.modified_count > 1:
            raise ValueError(
                f"Error while rewriting the block of data! Replaced entries: {result.modified_count}, expected: 1!"
            )
        return result.upserted_id

    def extract_db_entry(self, index_name: str, entry_id: str) -> Any:
        """
        Extract one document from the DB collection using filter based on passed index_name and entry_id

        :param str index_name: index name used to filter data in DB collection
        :param Any entry_id: ID of the DB entry to be extracted from the collection
        :return Any: document
        """
        q_filter = {index_name: entry_id}
        result = self.collection.find_one(filter=q_filter)
        return result

    def read_first_match(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns first matching document from the collection

        :param Dict[str, Any] data: document to be written in DB
        :return Dict[str: Any]: document
        """
        return self.collection.find_one(data)

    def get_collection_names(self) -> List[AnyStr]:
        """
        Gets a list of all the collection names in this database

        :return List[AnyStr]: list of all the collection names in the DB
        """
        return self.db.list_collection_names()

    def delete_db_entry(self, index_name: str, entry_id: Any) -> pymongo.results.DeleteResult:
        """
        Deletes DB entry from the collection by given index name and entry_id. Raises exception if number of deleted
        entries is not equal to 1

        :param str index_name: index name used to filter data in DB collection
        :param Any entry_id: ID of the DB entry to be deleted from the collection
        :raises ValueError: if number of deleted entries in DB collection is greater than 1, raises ValueError
        :return result: pymongo.results.DeleteResult
        """
        q_filter = {index_name: entry_id}
        result = self.collection.delete_one(filter=q_filter)
        if result.deleted_count > 1:
            raise ValueError(
                f"Error while deleting entry {entry_id} by index {index_name} from the collection {self.collection}, "
                f"deleted: {result.deleted_count} entries, expected: 0 or 1!"
            )
        return result

    def find_one_and_delete(self, data: Dict[str, Any]) -> Dict:
        """
        Finds a single document and deletes it, returning the document

        :param Dict[str, Any] data: document to be deleted from DB
        :return Dict: document
        """
        return self.collection.find_one_and_delete(data)
