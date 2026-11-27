from pydantic import RootModel

class AutocompleteResponse(RootModel[list[str]]):
    """Model returned for an autocomplete query"""