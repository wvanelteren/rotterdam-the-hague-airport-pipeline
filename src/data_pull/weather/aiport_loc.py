from dataclasses import dataclass


@dataclass(frozen=True)
class AirportLoc:
    LAT: str = "51.95763674245107"
    LON: str = "4.442139576041504"
    ZIP_CODE: str = "3045AP"
    COUNTRY: str = "NL"
