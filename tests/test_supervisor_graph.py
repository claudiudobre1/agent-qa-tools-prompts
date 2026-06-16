from project.graph.supervisor_graph import run_supervisor


def test_supervisor_routes_to_rag_worker():
    result = run_supervisor("What does the contract say about termination notice?")

    assert "rag_worker" in result["selected_agents"]
    assert result["final_answer"] is not None
    assert "contract.txt" in result["final_answer"]


def test_supervisor_routes_to_csv_worker():
    result = run_supervisor("show csv rows and columns")

    assert "csv_worker" in result["selected_agents"]
    assert result["final_answer"] is not None
    assert "CSV loaded successfully" in result["final_answer"]


def test_supervisor_routes_to_multiple_workers():
    result = run_supervisor(
        "What does the contract say about termination notice and show csv rows?"
    )

    assert "rag_worker" in result["selected_agents"]
    assert "csv_worker" in result["selected_agents"]
    assert result["final_answer"] is not None
    assert "contract.txt" in result["final_answer"]
    assert "CSV loaded successfully" in result["final_answer"]


def test_supervisor_uses_fallback_worker():
    result = run_supervisor("hello there")

    assert result["selected_agents"] == ["fallback_worker"]
    assert result["final_answer"] is not None
    assert "Fallback worker" in result["final_answer"]