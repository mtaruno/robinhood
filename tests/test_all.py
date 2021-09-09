import unittest
import pandas as pd
import sys

sys.path.insert(1, "../")
from ingest import ETL


class TestEverything(unittest.TestCase):
    def test_robinhood_ingestion(self):
        e = ETL()

        with open(e.paths["data"]) as f:
            raw = f.read()

        df = e.ingest_robin_table(data=raw)

        print(df.head())

        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_add_additional_columns(self):
        e = ETL()

        with open(e.paths["data"]) as f:
            raw = f.read()

        df = e.ingest_robin_table(data=raw)

        df = e.additional_robin_columns(df)

        print(df.head())

        self.assertTrue(isinstance(df, pd.DataFrame))

    # def test_get_full_table(self):
    #     e = ETL()
    #     df = e.get_full_table()

    #     print(df.head())

    #     self.assertTrue(isinstance(df, pd.DataFrame))


unittest.main()
