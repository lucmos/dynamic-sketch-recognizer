# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Point:
    time: Optional[int]
    component: int
    x: float
    y: float

    @staticmethod
    def from_dict(obj: Any) -> 'Point':
        assert isinstance(obj, dict)
        time = from_union([from_int, from_none], obj.get("time"))
        component = from_int(obj.get("component"))
        x = from_float(obj.get("x"))
        y = from_float(obj.get("y"))
        return Point(time, component, x, y)

    def to_dict(self) -> dict:
        result: dict = {}
        result["time"] = from_union([from_int, from_none], self.time)
        result["component"] = from_int(self.component)
        result["x"] = to_float(self.x)
        result["y"] = to_float(self.y)
        return result


@dataclass
class Configuration:
    guide_lines: bool
    items: List[str]
    repetitions: int
    repetitions_label: str
    title: str

    @staticmethod
    def from_dict(obj: Any) -> 'Configuration':
        assert isinstance(obj, dict)
        guide_lines = from_bool(obj.get("guide_lines"))
        items = from_list(from_str, obj.get("items"))
        repetitions = from_int(obj.get("repetitions"))
        repetitions_label = from_str(obj.get("repetitions_label"))
        title = from_str(obj.get("title"))
        return Configuration(guide_lines, items, repetitions, repetitions_label, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["guide_lines"] = from_bool(self.guide_lines)
        result["items"] = from_list(from_str, self.items)
        result["repetitions"] = from_int(self.repetitions)
        result["repetitions_label"] = from_str(self.repetitions_label)
        result["title"] = from_str(self.title)
        return result


@dataclass
class DeviceData:
    device_finger_print: str
    device_model: str
    heigth_pixels: int
    width_pixels: int
    xdpi: float
    ydpi: float

    @staticmethod
    def from_dict(obj: Any) -> 'DeviceData':
        assert isinstance(obj, dict)
        device_finger_print = from_str(obj.get("deviceFingerPrint"))
        device_model = from_str(obj.get("deviceModel"))
        heigth_pixels = from_int(obj.get("heigthPixels"))
        width_pixels = from_int(obj.get("widthPixels"))
        xdpi = from_float(obj.get("xdpi"))
        ydpi = from_float(obj.get("ydpi"))
        return DeviceData(device_finger_print, device_model, heigth_pixels, width_pixels, xdpi, ydpi)

    def to_dict(self) -> dict:
        result: dict = {}
        result["deviceFingerPrint"] = from_str(self.device_finger_print)
        result["deviceModel"] = from_str(self.device_model)
        result["heigthPixels"] = from_int(self.heigth_pixels)
        result["widthPixels"] = from_int(self.width_pixels)
        result["xdpi"] = to_float(self.xdpi)
        result["ydpi"] = to_float(self.ydpi)
        return result


@dataclass
class SessionData:
    age: int
    configuration: Configuration
    date: str
    device_data: DeviceData
    gender: str
    name: str
    surname: str

    @staticmethod
    def from_dict(obj: Any) -> 'SessionData':
        assert isinstance(obj, dict)
        age = from_int(obj.get("age"))
        configuration = Configuration.from_dict(obj.get("configuration"))
        date = from_str(obj.get("date"))
        device_data = DeviceData.from_dict(obj.get("deviceData"))
        gender = from_str(obj.get("gender"))
        name = from_str(obj.get("name"))
        surname = from_str(obj.get("surname"))
        return SessionData(age, configuration, date, device_data, gender, name, surname)

    def to_dict(self) -> dict:
        result: dict = {}
        result["age"] = from_int(self.age)
        result["configuration"] = to_class(Configuration, self.configuration)
        result["date"] = from_str(self.date)
        result["deviceData"] = to_class(DeviceData, self.device_data)
        result["gender"] = from_str(self.gender)
        result["name"] = from_str(self.name)
        result["surname"] = from_str(self.surname)
        return result


@dataclass
class ItemDataJson:
    date: str
    item: str
    item_index: int
    movement_points: List[Point]
    sampled_points: List[List[Point]]
    session_data: SessionData
    touch_down_points: List[Point]
    touch_up_points: List[Point]

    @staticmethod
    def from_dict(obj: Any) -> 'ItemDataJson':
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        item = from_str(obj.get("item"))
        item_index = from_int(obj.get("item_index"))
        movement_points = from_list(Point.from_dict, obj.get("movementPoints"))
        sampled_points = from_list(lambda x: from_list(Point.from_dict, x), obj.get("sampledPoints"))
        session_data = SessionData.from_dict(obj.get("sessionData"))
        touch_down_points = from_list(Point.from_dict, obj.get("touchDownPoints"))
        touch_up_points = from_list(Point.from_dict, obj.get("touchUpPoints"))
        return ItemDataJson(date, item, item_index, movement_points, sampled_points, session_data, touch_down_points, touch_up_points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_str(self.date)
        result["item"] = from_str(self.item)
        result["item_index"] = from_int(self.item_index)
        result["movementPoints"] = from_list(lambda x: to_class(Point, x), self.movement_points)
        result["sampledPoints"] = from_list(lambda x: from_list(lambda x: to_class(Point, x), x), self.sampled_points)
        result["sessionData"] = to_class(SessionData, self.session_data)
        result["touchDownPoints"] = from_list(lambda x: to_class(Point, x), self.touch_down_points)
        result["touchUpPoints"] = from_list(lambda x: to_class(Point, x), self.touch_up_points)
        return result


def itemdata_from_dict(s: Any) -> ItemDataJson:
    return ItemDataJson.from_dict(s)


def itemdata_to_dict(x: ItemDataJson) -> Any:
    return to_class(ItemDataJson, x)
