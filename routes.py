import logging
import json

from flask import Blueprint, jsonify, request

from scripts.score_real_collections import score_collection_main
from scripts.score_generated_collection import score_datasets_main

logger = logging.getLogger(__name__)

main_routes = Blueprint('main', __name__)


@main_routes.route('/api/submit_collection', methods=['POST'])
def submit_collection():
    try:
        collection_name = request.form.get('collection_name')
        
        #return jsonify({'collection': str(collection_name)})
        output_json = score_collection_main(collection_name)
        return json.dumps(output_json)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_routes.route('/api/submit_datasets', methods=['POST'])
def submit_datasets():
    try:
        name = request.json['name']
        attributes_frequency_counts = request.json['attributes_frequency_counts']
        contract_address = request.json['contract_address']
        token_standard = request.json['token_standard']
        metadata_string_attributes = request.json['metadata_string_attributes']

        #return jsonify({'collection': str(collection_name)})
        output_json = score_datasets_main(name, attributes_frequency_counts, contract_address, token_standard, metadata_string_attributes)
        return json.dumps(output_json)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500