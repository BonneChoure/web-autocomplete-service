# web-autocomplete-service

This application is a simple web service that answers prefix queries with autocomplete suggestions, built with FastAPI.
It can be run locally with the package manager `uv` or with docker.

The built-in dictionary is a merge of the following wordlists:
* [eff.org/files/2016/07/18/eff_large_wordlist.txt](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt)
* [eff.org/files/2018/08/29/gameofthrones_8k-2018.txt](https://www.eff.org/files/2018/08/29/gameofthrones_8k-2018.txt)
*  [eff.org/files/2018/08/29/memory-alpha_8k_2018.txt](https://www.eff.org/files/2018/08/29/memory-alpha_8k_2018.txt)
* [eff.org/files/2018/08/29/starwars_8k_2018.txt](https://www.eff.org/files/2018/08/29/starwars_8k_2018.txt)
* [eff.org/files/2018/08/29/harrypotter_8k_3column-txt.txt](https://www.eff.org/files/2018/08/29/harrypotter_8k_3column-txt.txt)

## Installation

### Docker image

```bash
# Clone repo
git clone https://github.com/BonneChoure/web-autocomplete-service.git

# Build Docker image
docker build -t web-autocomplete-service .

# Run Docker container
docker run --rm -p 8000:8000 web-autocomplete-service
```

###  uv

Prerequisite : uv >= 0.13.10

```bash
# Clone repo
git clone https://github.com/BonneChoure/web-autocomplete-service.git

# Sync Python environment
uv sync

# Run instance
uv run uvicorn web_autocomplete_service.main:app --app-dir src --reload
```

## Usage

Once the instance is running, you can query it with any  client. 

Example with curl :

```bash
curl http://127.0.0.1:8000/autocomplete?query=duck
```
### /autocomplete

The main entrypoint is the `/autocomplete` entrypoint. It required the `query` parameter.

The query is limited to 100 characters maximum.

By default, the maximum suggestionsreturned for a query is 4.


### /docs

The auto-generated FastAPI doc can be found on the `/docs` endpoint.

## Design choices

Some aspects of the project structure may be considered overly elaborated given the small scope it covers. The idea was to be as modular as possible to allow for future potential evolutions. 

### Data structure

A specific tree-based structure was chosen to store the dictionary : a **Radix Trie**. 

It enables quick search through a long list of words without having the go through the entire structure.

In a traditional Trie, each node represents to a single character.

The following example illustrates a Trie containing the words `duck`, `ducky` and `duckling` (* marks the end of a word)

```bash
root
└── d
    └── u
        └── c
            └── k *
                ├──l
                |  └──i
                |     └──n
                |        └──g *
                └── y *

```
This kind of Trie is already efficient but the number of nodes (and memory it uses) can be reduced. 

In a Radix Trie, consecutive nodes that have only one child and do not mark the end of a word are compressed into a single node.

The same example with a Radix Trie (* marks the end of a word):

```bash
root
└──duck*
    └──ling*
    └──y*
```

### Implementation

The core logic of the Radix Trie is located in `src\web_autocomplete_service\core\trie.py`.

Each Tree node has 4 attributes :
* `label` : a string representing the node (e.g. "ling" from above example)  
* `is_end_of_word` : a boolean stating if it marks the end of a word
* `is_sorted` : a boolean stating if the node's children are alphabetically sorted
* `children` : a dictionary containing all children nodes. The children are keyed with the first letter of their label. This allow to quickly retrieve the correct child to follow when searching for a prefix, as every children's label starts with a different letter.

### Sorting 

The queries' response must be alphabetically sorted. 

When inserting a node into the RadixTrie, if it not naturally already sorted, it adds the parent node into a list of unsorted nodes. This allows to skip any sorting when inserting an already sorted dictionary, or only sort the required nodes and not the whole tree when sorting is required.

For the initial scenario, the whole Trie is sorted once at the application start-up and never again. No sorting needs to be done at runtime when answering queries.