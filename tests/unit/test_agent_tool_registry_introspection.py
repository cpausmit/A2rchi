from src.archi.pipelines.agents.cms_comp_ops_agent import CMSCompOpsAgent


def test_cms_comp_ops_registry_available_on_uninitialized_instance():
    """Tool discovery endpoints introspect via __new__; this must stay safe."""
    dummy = CMSCompOpsAgent.__new__(CMSCompOpsAgent)

    registry = dummy.get_tool_registry()
    descriptions = dummy.get_tool_descriptions()

    assert "search_local_files" in registry
    assert "search_metadata_index" in registry
    assert "fetch_catalog_document" in registry
    assert "mcp" in registry
    assert "search_local_files" in descriptions
