import unittest
import hashlib
import crc32c
from google.cloud import storage


class TestUpload(unittest.TestCase):
    
    TEST_FILE_NAME = "test.cram"
    
    def setUp(self, test_file_name=TEST_FILE_NAME):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket("my_bucket_name")
        blob = self.bucket.blob(test_file_name)
        blob.upload_from_filename(test_file_name)

    def test_crc32c_hash(self, test_file_name=TEST_FILE_NAME):
        test_blob = self.bucket.get_blob(test_file_name)
        test_blob_crc32c_hash = test_blob.crc32c
        with open(test_file_name, "rb") as file:
            file_content = file.read()
            test_file_crc32c_hash = crc32c.crc32c(file_content)
        self.assertEqual(test_blob_crc32c_hash, test_file_crc32c_hash)

    def test_md5_hash(self, test_file_name=TEST_FILE_NAME):
        test_blob = self.bucket.get_blob(test_file_name)
        test_blob_md5_hash = test_blob.md5_hash
        with open(test_file_name, "rb") as file:
            file_content = file.read()
            test_file_md5_hash = hashlib.md5(file_content).hexdigest()
        self.assertEqual(test_blob_md5_hash, test_file_md5_hash)

    def tearDown(self, test_file_name=TEST_FILE_NAME):
        self.bucket.delete_blob(test_file_name)


if __name__ == '__main__':
    unittest.main()

