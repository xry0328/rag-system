from __future__ import annotations

from src.application.knowledge_base.commands import CreateKnowledgeBaseCommand, IngestMarkdownCommand
from src.domain.document.entities import Document, DocumentChunk
from src.domain.document.services import DocumentDomainService
from src.domain.knowledge_base.entities import KnowledgeBase
from src.domain.knowledge_base.repositories import DocumentRepository, KnowledgeBaseRepository
from src.domain.knowledge_base.services import KnowledgeBaseDomainService
from src.domain.shared.ids import new_id


class KnowledgeBaseApplicationService:
    def __init__(
        self,
        knowledge_base_repository: KnowledgeBaseRepository,
        document_repository: DocumentRepository,
        file_store,
        markdown_loader,
        text_splitter,
        embedding_provider,
        vector_repository,
    ) -> None:
        self.knowledge_base_repository = knowledge_base_repository
        self.document_repository = document_repository
        self.file_store = file_store
        self.markdown_loader = markdown_loader
        self.text_splitter = text_splitter
        self.embedding_provider = embedding_provider
        self.vector_repository = vector_repository
        self.kb_domain_service = KnowledgeBaseDomainService()
        self.document_domain_service = DocumentDomainService()

    def create_knowledge_base(self, command: CreateKnowledgeBaseCommand) -> KnowledgeBase:
        name = command.name.strip()
        existing = self.knowledge_base_repository.find_by_name(name)
        self.kb_domain_service.ensure_can_create(existing, name)
        knowledge_base = KnowledgeBase(id=new_id("kb"), name=name, description=command.description.strip())
        self.vector_repository.ensure_collection(knowledge_base.id)
        return self.knowledge_base_repository.create(knowledge_base)

    def list_knowledge_bases(self) -> list[KnowledgeBase]:
        return self.knowledge_base_repository.list()

    def list_documents(self, knowledge_base_id: str) -> list[Document]:
        return self.document_repository.list_by_knowledge_base(knowledge_base_id)

    def ingest_markdown(self, command: IngestMarkdownCommand) -> Document:
        self.document_domain_service.validate_markdown(command.filename, command.content)
        knowledge_base = self.knowledge_base_repository.get(command.knowledge_base_id)
        source_path = self.file_store.save(knowledge_base.id, command.filename, command.content)
        document = Document(
            id=new_id("doc"),
            knowledge_base_id=knowledge_base.id,
            filename=command.filename,
            source_path=str(source_path),
        )
        self.document_repository.add(document)

        try:
            text = self.markdown_loader.load(source_path)
            split_docs = self.text_splitter.split(text)
            chunks = [
                DocumentChunk(
                    id=new_id("chunk"),
                    knowledge_base_id=knowledge_base.id,
                    document_id=document.id,
                    content=item.content,
                    metadata={
                        **item.metadata,
                        "knowledge_base_id": knowledge_base.id,
                        "document_id": document.id,
                        "filename": document.filename,
                    },
                )
                for item in split_docs
            ]
            embeddings = self.embedding_provider.embed_documents([chunk.content for chunk in chunks])
            self.vector_repository.add_chunks(knowledge_base.id, chunks, embeddings)
            document.mark_completed(len(chunks))
            knowledge_base.add_ingested_document(len(chunks))
            self.document_repository.update(document)
            self.knowledge_base_repository.update(knowledge_base)
            return document
        except Exception as exc:
            document.mark_failed(str(exc))
            self.document_repository.update(document)
            raise

