#!/usr/bin/env python
import gzip
import io
import json
import logging
import os
import sys
import zipfile as zf

import requests
import us
import shapefile

AREAS_TO_PROCESS = [
    # 'block',
    # 'blockgroup',
    'cd',
    'county',
    'state',
    'tract',
    'zcta'
]


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class GeoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            # for why we use this see
            # http://gis.stackexchange.com/a/3663
            return obj.decode('ISO8859-1')
        return json.JSONEncoder.default(self, obj)


def unzip_to_filetypes(data):
    zp = zf.ZipFile(data)
    filenames = [info.filename for info in zp.filelist]
    filetypes = [name.split('.')[-1] for name in filenames]
    filedata = [zp.read(name) for name in filenames]

    return dict(zip(filetypes, filedata))


def generate_features(field_names, shape_reader):
    for sr in shape_reader.iterShapeRecords():
        feature = dict(
            type='Feature',
            geometry=sr.shape.__geo_interface__,
            properties=dict(zip(field_names, sr.record))
        )
        yield feature


def process_state(state):
    logger.info('Processing {}'.format(state.name))
    for area, url in state.shapefile_urls().items():
        if area not in AREAS_TO_PROCESS:
            continue

        resp = requests.get(url)
        data = unzip_to_filetypes(io.BytesIO(resp.content))
        shape_reader = shapefile.Reader(
            **{k: io.BytesIO(data[k]) for k in data})
        field_names = [item[0] for item in shape_reader.fields]
        feature_collection = dict(
            type='FeatureCollection',
            features=list(generate_features(field_names, shape_reader))
        )
        target_dir = 'US/{}'.format(state.name)
        out_file = '{}/{}.geojson.gz'.format(target_dir, area)
        logger.info('Generating {}'.format(out_file))
        os.makedirs(target_dir, exist_ok=True)
        with gzip.open(out_file, 'wt') as fp:
            json.dump(feature_collection, fp, cls=GeoJSONEncoder)


def main():
    logger.debug('Start main')
    for state in us.STATES:
        process_state(state)


if __name__ == '__main__':
    main()
