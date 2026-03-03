from langchain_core.messages import AIMessage, AIMessageChunk

from src.archi.pipelines.agents.base_react import BaseReActAgent


def _agent() -> BaseReActAgent:
    return object.__new__(BaseReActAgent)


def test_extract_usage_from_message_prefers_usage_metadata() -> None:
    agent = _agent()
    chunk = AIMessageChunk(
        content="",
        usage_metadata={"input_tokens": 12, "output_tokens": 8, "total_tokens": 20},
        response_metadata={"usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}},
    )
    usage = agent._extract_usage_from_message(chunk)
    assert usage == {"prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20}


def test_extract_usage_from_messages_supports_usage_metadata() -> None:
    agent = _agent()
    messages = [
        AIMessage(content="a", usage_metadata={"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}),
        AIMessage(content="b", response_metadata={"usage": {"input_tokens": 2, "output_tokens": 3, "total_tokens": 5}}),
    ]
    usage = agent._extract_usage_from_messages(messages)
    assert usage == {"prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20}


def test_sum_usage_records() -> None:
    agent = _agent()
    usage = agent._sum_usage(
        [
            {"prompt_tokens": 4, "completion_tokens": 2, "total_tokens": 6},
            {"prompt_tokens": 1, "completion_tokens": 3, "total_tokens": 4},
        ]
    )
    assert usage == {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10}
