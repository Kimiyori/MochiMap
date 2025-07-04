from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class NodeType(Enum):
    TOPIC = "topic"
    CONCEPT = "concept"
    PROJECT = "project"
    QUIZ = "quiz"
    RESOURCE = "resource"
    MILESTONE = "milestone"


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass(frozen=True)
class Difficulty:
    level: DifficultyLevel

    def __str__(self) -> str:
        return self.level.value

    def __composite_values__(self):
        return (self.level,)
    
    @classmethod
    def from_composite(cls, level):
        return cls(level=level)
    
@dataclass(frozen=True)
class Position:
    x: float
    y: float

class TimeUnit(Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"

@dataclass(frozen=True)
class EstimatedTime:
    value: int
    unit: TimeUnit
    
    def __str__(self) -> str:
        return f"{self.value} {self.unit.value}"
        
    def __composite_values__(self):
        return (self.value, self.unit)
    
    @classmethod
    def from_composite(cls, value, unit):
        return cls(value=value, unit=unit)
    
class ResourceType(Enum):
    ARTICLE = "article"
    VIDEO = "video"
    BOOK = "book"
    COURSE = "course"
    GITHUB = "github"
    DOCUMENTATION = "documentation"
    OTHER = "other"

@dataclass
class Resource:
    id: UUID
    title: str
    url: str
    resource_type: ResourceType
    description: str = ""
    is_free: bool = True

class ConnectionType(Enum):
    SEQUENTIAL = "sequential"  # Must complete source before target
    OPTIONAL = "optional"      # Suggested but not required path
    REFERENCE = "reference" 

@dataclass
class Connection:
    id: UUID 
    source_id: UUID
    target_id: UUID
    connection_type: ConnectionType = ConnectionType.SEQUENTIAL
    label: str = ""