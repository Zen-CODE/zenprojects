from pydantic import BaseModel


class StateModel(BaseModel):
    """
    Represents the state of the currently playing audio track.
    """
    state: str
    position: float
    volume: float
