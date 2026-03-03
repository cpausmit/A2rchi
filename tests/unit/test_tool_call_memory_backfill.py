from types import SimpleNamespace

from src.archi.pipelines.agents.base_react import BaseReActAgent
from src.archi.pipelines.agents.utils.run_memory import RunMemory


def test_run_memory_resolves_pending_tool_input_by_name_when_args_are_empty():
    memory = RunMemory()
    memory.record_tool_input("search_local_files", {"query": "Tier0 transfer errors"})

    msg = SimpleNamespace(
        tool_calls=[{"id": "call_1", "name": "search_local_files", "args": {}}],
        additional_kwargs={},
    )
    memory.record_tool_calls_from_message(msg)

    by_id = memory.tool_inputs_by_id()
    assert by_id["call_1"]["tool_name"] == "search_local_files"
    assert by_id["call_1"]["tool_input"] == {"query": "Tier0 transfer errors"}


def test_run_memory_uses_tool_call_chunks_to_fill_name_and_args():
    memory = RunMemory()

    msg = SimpleNamespace(
        tool_calls=[{"id": "call_2", "name": "unknown", "args": {}}],
        tool_call_chunks=[{"id": "call_2", "name": "search_metadata_index", "args": "{\"query\": \"CMSTRANSF-1078\"}"}],
        additional_kwargs={},
    )
    memory.record_tool_calls_from_message(msg)

    by_id = memory.tool_inputs_by_id()
    assert by_id["call_2"]["tool_name"] == "search_metadata_index"
    assert by_id["call_2"]["tool_input"] == {"query": "CMSTRANSF-1078"}


def test_finalize_output_includes_tool_inputs_by_id_metadata():
    agent = object.__new__(BaseReActAgent)
    memory = RunMemory()
    memory.record_tool_call("call_3", "fetch_catalog_document", {"resource_hash": "abc"})

    output = agent.finalize_output(
        answer="",
        memory=memory,
        messages=[],
        metadata={"event_type": "tool_output"},
        final=False,
    )

    assert output.metadata["event_type"] == "tool_output"
    assert output.metadata["tool_inputs_by_id"]["call_3"]["tool_name"] == "fetch_catalog_document"
    assert output.metadata["tool_inputs_by_id"]["call_3"]["tool_input"] == {"resource_hash": "abc"}
