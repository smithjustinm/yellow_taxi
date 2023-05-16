""" Module to handle postgres database operations """
import glob
import os

import pandas as pd
import sqlalchemy as sq
import structlog

from yellow_taxi_data.config.settings import settings

settings.setup_logging()

logger = structlog.get_logger(__name__)


def get_file_name(path) -> str:
    """get file name from path, removes extension"""
    full_name = os.path.basename(path)
    return full_name.split(".")[0]


class DatabaseEngine:
    """Abstracted methods for sql queries"""

    def __init__(
        self,
        connection_string,
    ):
        self.create_engine(connection_string=connection_string)

    def create_engine(self, connection_string: str):
        """
        Utility function to get engine, raises exception if engine creation fails.
        """
        try:
            self.engine = sq.create_engine(connection_string)
        except Exception as e:
            logger.exception(
                {"message": "Error in creating engine", "error": str(e)},
            )
            raise e

    @staticmethod
    def read_sql(path) -> dict:
        """read sql files from path and return a dictionary of queries"""
        sql = {}
        files = glob.glob(f"{path}/*.sql")
        for file in files:
            name = get_file_name(file)
            try:
                with open(file, "r") as f:
                    sql[name] = f.read()
            except Exception as e:
                logger.exception(
                    {
                        "message": "--- query file not found ---",
                    },
                )
                raise e
        return sql

    def get_sql_data(self, query, *args, **kwargs):
        """
        Utility function to read data from sql query, raises exception if query fails
        params: query, engine, *args, **kwargs
        """
        try:
            with self.engine.connect() as connection:
                if kwargs:
                    return pd.read_sql(query, connection, params=kwargs)
                else:
                    return pd.read_sql(query, connection, params=args)

        except Exception as e:
            logger.exception(
                {
                    "message": f"Error in reading data from query: {query}",
                },
            )
            raise e

    def exec_sql_data(self, query, auto_commit=True, *args, **kwargs):
        """
        Utility function to execute sql query, raises exception if query fails
        params: query, engine, auto_commit, *args, **kwargs
        """
        try:
            with self.engine.connect().execution_options(
                auto_commit=auto_commit
            ) as connection:
                if kwargs:
                    connection.execute(query, kwargs)
                else:
                    connection.execute(query, args)

        except Exception as e:
            logger.exception(
                {"message": f"Error in executing query: {query}"},
            )
            raise e


class Timescale:
    """Timescale is a class that manages an instance of DatabaseEngine. It is used to
    handle operations for the timescale database.
    """

    engine: DatabaseEngine = None

    def __init__(self):
        if Timescale.engine is None:
            Timescale.engine = DatabaseEngine(
                connection_string=settings.TIMESCALE_CONNECTION_STRING
            )
        root = os.path.dirname(os.path.realpath(__file__))
        self.queries = Timescale.engine.read_sql(os.path.join(root, "./sql"))

    def get_distance_by_percentile(self, percentile: float):
        """returns json list of all trips where the distance traveled is
        within the percentile given"""
        pass
