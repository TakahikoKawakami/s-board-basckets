import dataclasses
import logging
# from typing import 
from app.entities.Baskets import Basket
from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs

@dataclasses.dataclass
class Analyzer():
    logger: logging.Logger
    basket_list: list[Basket]
    fpgrowth: Fpgrowth
    vis_js: VisJs

    def __init__(self) -> None:
        pass
