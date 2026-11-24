from pydantic import RootModel

class AutocompleteResponse(RootModel[list[str]]):
    """Terms returned for an autocomplete query"""