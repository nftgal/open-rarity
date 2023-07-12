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

def score_datasets_main(name, attributes_frequency_counts, contract_address, token_standard, tokens):

    tokens_parsed = []
    for token in tokens:
        token_id = token["tokenId"]
        metadata = token["metadata"]

        attributes={}
        for key, value in metadata.items():
            attributes[key] = StringAttribute(name=value["name"], value=value["value"])

        tokens_parsed.append(Token(
                token_identifier=EVMContractTokenIdentifier(
                    contract_address=contract_address, token_id=token_id
                ),
                token_standard=getattr(TokenStandard, token_standard),
                metadata=TokenMetadata(
                    string_attributes=attributes
                ),
            ),
        )

    # Create OpenRarity collection object and provide all metadata information
    collection = Collection(
        name=name,
        attributes_frequency_counts=attributes_frequency_counts,
        tokens=tokens_parsed,
    )  # Replace inputs with your collection-specific details here

    # Generate scores for a collection
    ranked_tokens = RarityRanker.rank_collection(collection=collection)

    for token_rarity in ranked_tokens:
        return token_rarity