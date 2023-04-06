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
            Some info
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

    