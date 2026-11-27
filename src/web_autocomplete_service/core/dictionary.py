import logging
from pathlib import Path

from web_autocomplete_service.core.trie import RadixTrie
from web_autocomplete_service.core.normalization import normalize

logger = logging.getLogger(__name__)

def load_trie(trie: RadixTrie, input_path:Path) -> None:
    """Build a RadixTrie `trie` from a given text file path `input_path`
    
    Expects input file to contain one word per line. 
    Words are normalized before being inserted into `trie`.
    """
    logger.info("Loading dictionary from %s", input_path)
    try:
        with open(input_path, encoding="utf-8") as input_file:
            for line in input_file:
                word = normalize(line)
                trie.insert(word)
    except FileNotFoundError:
        logger.error("Dictionary file not found at %s", input_path)
        raise
    logger.info("Loaded dictionary from %s", input_path)
    return trie