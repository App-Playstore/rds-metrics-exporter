import unittest
from unittest.mock import patch

from exporter import (
    get_instances, update_metrics, engine_version_gauge, rds_client
)

class TestExporter(unittest.TestCase):

    @patch('exporter.rds_client.describe_db_instances')
    def test_get_instances(self, mock_describe):
        mock_data = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'my-db-instance',
                    'EngineVersion': '16.3'
                    'Engine': 'postgres'
                }
            ]
        }
        mock_describe.return_value = mock_data

        instances = get_instances()
        self.assertEqual(instances, mock_data['DBInstances'])

    @patch('exporter.rds_client.describe_db_instances')
    def test_update_metrics(self, mock_describe):
        mock_data = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'my-db-instance',
                    'EngineVersion': '16.3'
                }
            ]
        }
        mock_describe.return_value = mock_data

        update_metrics()

        self.assertEqual(engine_version_gauge.labels(instance_identifier='my-db-instance').set(10.0), None)

if __name__ == '__main__':
    unittest.main()


