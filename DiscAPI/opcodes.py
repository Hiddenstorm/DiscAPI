def opidentify():
    """
    Creates an opcode dictionary for identifing a client
    """

    dict = {
        "op": 2,
        "d": {
            "token": str(token),
            "intents": 513,
            "properties": {
                "$os": "linux",
                "$browser": "my_library",
                "$device": "my_library"
    }