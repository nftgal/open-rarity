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
    token_attr_scores, token_attr_names, sorted_token_rarities = RarityRanker.rank_collection(collection=collection)

    json_output = {}
    for idx, rarity_token in enumerate(sorted_token_rarities):
        token_id = rarity_token.token.token_identifier.token_id
        rank = rarity_token.rank
        score = rarity_token.score
        json_output[token_id] = {"rank": rank, "score": score, "token_attr_scores": token_attr_scores[idx], "token_attr_names": token_attr_names[idx]}
    return json_output