from enum import Enum

class GenerationMethod(str, Enum):
    DEFAULT = "default",
    PHYSICS_ART = "physics"
    CLIP = "clip"
    READER = "reader"

