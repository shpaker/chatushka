from pydantic import BaseModel


class HeroesSettings(BaseModel):
    calendar_collection: str = "heroes_calendar"
    activations_collection: str = "heroes_activations"
