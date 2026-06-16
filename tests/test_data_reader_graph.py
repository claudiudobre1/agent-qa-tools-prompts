from project.graph.data_reader_graph import run_data_reader


def test_data_reader_routes_to_rag():
    result = run_data_reader("What does the contract say about termination notice?")

    assert result["source"] == "rag"
    assert result["error"] is None
    assert "contract.txt" in result["result"]


def test_data_reader_routes_to_csv():
    result = run_data_reader("show csv rows and columns")

    assert result["source"] == "csv"
    assert result["error"] is None
    assert "CSV loaded successfully" in result["result"]
    assert "Rows: 3" in result["result"]


def test_data_reader_uses_fallback_for_unknown_query():
    result = run_data_reader("hello there")

    assert result["source"] == "fallback"
    assert result["error"] is None
    assert "Fallback" in result["result"]