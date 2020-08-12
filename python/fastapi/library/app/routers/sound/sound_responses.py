# from pydantic import BaseModel
# class SoundStateModel(BaseModel):
from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass
class SoundStateModel:
    """
    Represents the state of the currently playing audio track.
    """
    state: str = Field(description="The state of the currently playing audio.")

    position: float = Field(
        description="The position in the track between 0 and 1.", ge=0, le=1)

    volume: float = Field(
        description="The current volume between 0 and 1.", ge=0, le=1)

    filename: str = Field(
        description="The full path to the currently playing file.")
