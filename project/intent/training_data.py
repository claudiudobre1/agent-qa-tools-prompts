TRAINING_EXAMPLES = [
    ("25 * 17", "calculator"),
    ("calculate 10 + 5", "calculator"),
    ("what is 100 divided by 4", "calculator"),
    ("2 + 2", "calculator"),

    ("what time is it", "datetime"),
    ("what is today's date", "datetime"),
    ("tell me the current date", "datetime"),
    ("current time please", "datetime"),

    ("what does the contract say about termination", "rag"),
    ("find the notice clause in the document", "rag"),
    ("search the document for confidentiality", "rag"),
    ("according to the contract what is required", "rag"),

    ("show csv rows and columns", "csv"),
    ("load the csv data", "csv"),
    ("how many rows are in the table", "csv"),
    ("show data columns", "csv"),

    ("what does the contract say and show csv rows", "multi"),
    ("search the document and read csv data", "multi"),
    ("combine contract information with table data", "multi"),

    ("count the words in this text", "text_stats"),
    ("how many characters are here", "text_stats"),
    ("analyze this sentence", "text_stats"),
    ("hello there", "text_stats"),
]