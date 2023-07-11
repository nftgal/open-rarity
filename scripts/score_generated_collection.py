from open_rarity import (
    Collection,
    Token,
    RarityRanker,
    TokenMetadata,
    StringAttribute,
)
from open_rarity.models.token_identifier import EVMContractTokenIdentifier
from open_rarity.models.token_standard import TokenStandard

import json

def score_datasets_main(name, attributes_frequency_counts, contract_address, token_standard, metadata_string_attributes):
    attributes={}
    for key, value in metadata_string_attributes.items():
        attributes[key] = StringAttribute(name=value["name"], value=value["value"])

    # Create OpenRarity collection object and provide all metadata information
    collection = Collection(
        name=name,
        attributes_frequency_counts=attributes_frequency_counts,
        tokens=[
            Token(
                token_identifier=EVMContractTokenIdentifier(
                    contract_address=contract_address, token_id=1
                ),
                token_standard=getattr(TokenStandard, token_standard),
                metadata=TokenMetadata(
                    string_attributes=attributes
                ),
            ),
        ],
    )  # Replace inputs with your collection-specific details here

    # Generate scores for a collection
    ranked_tokens = RarityRanker.rank_collection(collection=collection)

    for token_rarity in ranked_tokens:
        return token_rarity