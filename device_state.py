from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DeviceState:
    session_id: str
    state: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)

    def update(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.state.get(key, default)

    def append_event(self, event_type: str, data: Dict[str, Any]) -> None:
        self.history.append({"type": event_type, "data": data})

    def clear(self) -> None:
        self.state.clear()
        self.history.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {"session_id": self.session_id, "state": self.state, "history": self.history}
