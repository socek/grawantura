from enum import Enum
from typing import Optional


class Event(Enum):
    question_draw = "question draw"
    change_view = "change view"
    end_auction = "end auction"
    init_money = "init money"
    hint = "hint"
    answer = "answer"


class Calculator:
    def __init__(self):
        self.result = {}

    def calculate(self, events):
        for event in events:
            event_type = Event(event["typename"])
            calculator = getattr(self, event_type.name, None)
            if calculator:
                calculator(event)
        return self.result


class MoneyCalculator(Calculator):
    def __init__(self):
        self.result = {
            "money_pool": 0,
        }
        self.last_auction_win = None

    def init_money(self, event):
        for key, value in event["payload"].items():
            self.result[key] = self.result.get(key, 0) + value

    def end_auction(self, event):
        self.last_auction_win = max(event["payload"], key=event["payload"].get)
        for key, value in event["payload"].items():
            if key != "addon":
                self.result[key] = self.result.get(key, 0) - value
            self.result["money_pool"] += value

    def hint(self, event):
        for key, value in event["payload"]["money"].items():
            self.result[key] = self.result.get(key, 0) + value

    def answer(self, event):
        if event["payload"]["success"]:
            self.result[self.last_auction_win] = (
                self.result.get(self.last_auction_win, 0) + self.result["money_pool"]
            )
            self.result["money_pool"] = 0


class HintsCalculator(Calculator):
    def hint(self, event):
        for key, value in event["payload"]["change"].items():
            self.result[key] = self.result.get(key, 0) + value


def is_started(events) -> bool:
    for event in events:
        if event["typename"] == Event.init_money.value:
            return True
    return False


def answering_team_id(events) -> Optional[str]:
    team_id: Optional[str] = None
    for event in events:
        if Event(event["typename"]) == Event.end_auction:
            team_id = max(event["payload"], key=event["payload"].get)
        elif Event(event["typename"]) == Event.answer:
            team_id = None
    return team_id

def show_hint(events) -> bool:
    show_hint = False
    for event in events:
        if Event(event["typename"]) == Event.hint:
            for _, value in event["payload"]["change"].items():
                if value < 0:
                    show_hint = True
        elif Event(event["typename"]) == Event.question_draw:
            show_hint = False
    return show_hint
