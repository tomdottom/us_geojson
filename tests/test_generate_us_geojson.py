from io import BytesIO
import unittest

import generate_us_geojson as gusg


TEST_ZIP_FILE = b'PK\x03\x04\x14\x00\x00\x00\x00\x00\xa3ucJ\xc9\x11f\x06\x13\x00\x00\x00\x13\x00\x00\x00\x08\x00\x00\x00test.txtThis is a test filePK\x01\x02\x14\x03\x14\x00\x00\x00\x00\x00\xa3ucJ\xc9\x11f\x06\x13\x00\x00\x00\x13\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x00\x00\x00\x00test.txtPK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x006\x00\x00\x009\x00\x00\x00\x00\x00'


class TestGenerateGeoJSON(unittest.TestCase):

    def test_unzip_to_memory(self):
        a_zip_filehandle = BytesIO(TEST_ZIP_FILE)

        unzipped_filetypes = gusg.unzip_to_filetypes(a_zip_filehandle)

        self.assertIn('txt', unzipped_filetypes)
        self.assertEqual(
            unzipped_filetypes,
            {'txt': b'This is a test file'}
        )
