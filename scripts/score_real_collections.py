import argparse
import csv
import json

from open_rarity import RarityRanker
from open_rarity.models.token_rarity import TokenRarity
from open_rarity.resolver.opensea_api_helpers import get_collection_from_opensea

parser = argparse.ArgumentParser()
parser.add_argument(
    "slugs",
    type=str,
    default=["boredapeyachtclub"],
    nargs="*",
    help="Slugs you want to generate scoring for, separated by spaces",
)
parser.add_argument(
    "--filename_prefix",
    dest="filename_prefix",
    default="score_real_collections_results",
    help="The filename prefix to output the ranking results to. "
    "The filename will be {prefix}_{slug}.json/csv",
)

parser.add_argument(
    "--filetype",
    dest="filetype",
    default="json",
    choices=["json", "csv"],
    help="Determines output file type. Either 'json' or 'csv'.",
)

parser.add_argument(
    "--cache",
    action=argparse.BooleanOptionalAction,
    dest="use_cache",
    default=True,
    help="Determines whether we force refetch all Token and trait data "
    "from Opensea or read data from a local cache file",
)


def score_collection_and_output_results(
    slug: str, output_filename: str, use_cache: bool
):
    # Get collection
    collection = get_collection_from_opensea(slug, use_cache=use_cache)
    print(f"Created collection {slug} with {collection.token_total_supply} tokens")

    # Score, rank  and sort ascending by token rarity rank
    token_attr_scores, token_attr_names, sorted_token_rarities = RarityRanker.rank_collection(
        collection=collection
    )

    # Print out ranks and scores
    print("Token ID and their ranks and scores, sorted by rank")
    json_output = {}
    csv_rows = []
    for idx, rarity_token in enumerate(sorted_token_rarities):
        token_id = rarity_token.token.token_identifier.token_id
        rank = rarity_token.rank
        score = rarity_token.score
        json_output[token_id] = {"rank": rank, "score": score, "token_attr_scores": token_attr_scores[idx], "token_attr_names": token_attr_names[idx]}
        csv_rows.append([token_id, rank, score])
    return json_output


def score_collection_main(collection_name):
    """This script by default fetches bored ape yacht club collection and token
    metadata from the Opensea API via opensea_api_helpers and scores + ranks the
    collection via OpenRarity scorer.

    It will output results into {prefix}_{slug}.json/csv file, with the default
    filename being "score_real_collections_results.json".

    If JSON, format is:
    {
        <token_id>: {
            "rank": <int>,
            "score": <float>,
        }
    }

    If CSV, format is:
    Columns: Token ID, Rank, Score

    Command:
        `python -m scripts.score_real_collections`

        If you want to set your own slugs to process, you may pass it in via
        command-line.
        Example:
        `python -m scripts.score_real_collections boredapeyachtclub proof-moonbirds`
    """
    
    args = parser.parse_args()
    args.slugs = [collection_name]
    use_cache = args.use_cache
    print(f"Scoring collections: {args.slugs} with {use_cache=}")
    print(f"Output file prefix: {args.filename_prefix} with type .{args.filetype}")

    files = []
    for slug in args.slugs:
        output_filename = f"{args.filename_prefix}_{slug}.{args.filetype}"
        print(f"Generating results for: {slug}")
        return score_collection_and_output_results(
            slug=slug,
            output_filename=output_filename,
            use_cache=use_cache,
        )
