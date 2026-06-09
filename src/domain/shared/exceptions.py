class DomainError(Exception):
    """Base exception for domain-level rule violations."""


class KnowledgeBaseAlreadyExists(DomainError):
    pass


class KnowledgeBaseNotFound(DomainError):
    pass


class InvalidMarkdownDocument(DomainError):
    pass

