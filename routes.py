import logging
import json

from flask import Blueprint, jsonify, request

from scripts.score_real_collections import score_collection_main

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
