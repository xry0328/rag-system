from src.domain.knowledge_base.entities import KnowledgeBase
from src.infrastructure.persistence.metadata_store import JsonMetadataStore


def test_json_metadata_store_creates_and_finds_knowledge_base(tmp_path):
    store = JsonMetadataStore(tmp_path / "registry.json")
    knowledge_base = KnowledgeBase(id="kb_test", name="Support Docs")

    store.create(knowledge_base)

    assert store.get("kb_test").name == "Support Docs"
    assert store.find_by_name("support docs").id == "kb_test"

