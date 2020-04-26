from dataclasses import dataclass
import dateutil.parser

from typing import Any, List, Union, Optional, TypeVar, Callable, Type, cast
from enum import Enum
from datetime import datetime

from requests import Response

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class AccountParameter:
    pl: str
    vl: str
    p: str
    v: str

    @staticmethod
    def from_dict(obj: Any) -> "AccountParameter":
        assert isinstance(obj, dict)
        pl = from_str(obj.get("pl"))
        vl = from_str(obj.get("vl"))
        p = from_str(obj.get("p"))
        v = from_str(obj.get("v"))
        return AccountParameter(pl, vl, p, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pl"] = from_str(self.pl)
        result["vl"] = from_str(self.vl)
        result["p"] = from_str(self.p)
        result["v"] = from_str(self.v)
        return result


class TypeEnum(Enum):
    SELL = "sell"


@dataclass
class AdParameter:
    pl: str
    vl: Union[List[str], str]
    p: str
    v: Union[List[int], bool, TypeEnum, int]

    @staticmethod
    def from_dict(obj: Any) -> "AdParameter":
        assert isinstance(obj, dict)
        pl = str(obj.get("pl"))
        vl = from_union([lambda x: from_list(from_str, x), from_str], obj.get("vl"))
        p = str(obj.get("p"))
        v = from_union(
            [
                from_int,
                from_bool,
                lambda x: from_union([TypeEnum, lambda x: int(x)], from_str(x)),
                lambda x: from_list(from_int, x),
            ],
            obj.get("v"),
        )
        return AdParameter(pl, vl, p, v)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pl"] = self.pl
        result["vl"] = from_union([lambda x: from_list(from_str, x), from_str], self.vl)
        result["p"] = self.p
        result["v"] = from_union(
            [
                lambda x: from_int((lambda x: is_type(int, x))(x)),
                lambda x: from_bool((lambda x: is_type(bool, x))(x)),
                lambda x: from_str(
                    (lambda x: to_enum(TypeEnum, (lambda x: is_type(TypeEnum, x))(x)))(
                        x
                    )
                ),
                lambda x: from_list(from_int, (lambda x: is_type(List, x))(x)),
            ],
            self.v,
        )
        return result


class Currency(Enum):
    BYN = "BYR"
    USD = "USD"


@dataclass
class Image:
    id: str
    yams_storage: bool

    @staticmethod
    def from_dict(obj: Any) -> "Image":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        yams_storage = from_bool(obj.get("yams_storage"))
        return Image(id, yams_storage)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["yams_storage"] = from_bool(self.yams_storage)
        return result


@dataclass
class PaidServices:
    halva: bool
    highlight: bool
    polepos: bool
    ribbons: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "PaidServices":
        assert isinstance(obj, dict)
        halva = from_bool(obj.get("halva"))
        highlight = from_bool(obj.get("highlight"))
        polepos = from_bool(obj.get("polepos"))
        ribbons = from_union([from_none, from_str], obj.get("ribbons"))
        return PaidServices(halva, highlight, polepos, ribbons)

    def to_dict(self) -> dict:
        result: dict = {}
        result["halva"] = from_bool(self.halva)
        result["highlight"] = from_bool(self.highlight)
        result["polepos"] = from_bool(self.polepos)
        result["ribbons"] = from_union([from_none, from_str], self.ribbons)
        return result


@dataclass
class Ad:
    account_id: int
    account_parameters: List[AccountParameter]
    ad_id: int
    ad_link: str
    ad_parameters: List[AdParameter]
    body: None
    category: int
    company_ad: bool
    currency: Currency
    images: List[Image]
    list_id: int
    list_time: datetime
    paid_services: PaidServices
    price_byn: int
    price_usd: int
    remuneration_type: int
    subject: str
    type: TypeEnum
    phone: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Ad":
        assert isinstance(obj, dict)
        account_id = from_int(obj.get("account_id"))
        account_parameters = from_list(
            AccountParameter.from_dict, obj.get("account_parameters")
        )
        ad_id = from_int(obj.get("ad_id"))
        ad_link = from_str(obj.get("ad_link"))
        ad_parameters = from_list(AdParameter.from_dict, obj.get("ad_parameters"))
        body = from_none(obj.get("body"))
        category = int(from_str(obj.get("category")))
        company_ad = from_bool(obj.get("company_ad"))
        currency = Currency(obj.get("currency"))
        images = from_list(Image.from_dict, obj.get("images"))
        list_id = from_int(obj.get("list_id"))
        list_time = from_datetime(obj.get("list_time"))
        paid_services = PaidServices.from_dict(obj.get("paid_services"))
        price_byn = int(from_str(obj.get("price_byn")))
        price_usd = int(from_str(obj.get("price_usd")))
        remuneration_type = int(from_str(obj.get("remuneration_type")))
        subject = from_str(obj.get("subject"))
        type = TypeEnum(obj.get("type"))
        phone = from_union([from_none, from_str], obj.get("phone"))
        return Ad(
            account_id,
            account_parameters,
            ad_id,
            ad_link,
            ad_parameters,
            body,
            category,
            company_ad,
            currency,
            images,
            list_id,
            list_time,
            paid_services,
            price_byn,
            price_usd,
            remuneration_type,
            subject,
            type,
            phone,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["account_id"] = from_int(self.account_id)
        result["account_parameters"] = from_list(
            lambda x: to_class(AccountParameter, x), self.account_parameters
        )
        result["ad_id"] = from_int(self.ad_id)
        result["ad_link"] = from_str(self.ad_link)
        result["ad_parameters"] = from_list(
            lambda x: to_class(AdParameter, x), self.ad_parameters
        )
        result["body"] = from_none(self.body)
        result["category"] = from_str(str(self.category))
        result["company_ad"] = from_bool(self.company_ad)
        result["currency"] = to_enum(Currency, self.currency)
        result["images"] = from_list(lambda x: to_class(Image, x), self.images)
        result["list_id"] = from_int(self.list_id)
        result["list_time"] = self.list_time.isoformat()
        result["paid_services"] = to_class(PaidServices, self.paid_services)
        result["price_byn"] = from_str(str(self.price_byn))
        result["price_usd"] = from_str(str(self.price_usd))
        result["remuneration_type"] = from_str(str(self.remuneration_type))
        result["subject"] = from_str(self.subject)
        result["type"] = to_enum(TypeEnum, self.type)
        result["phone"] = from_union([from_none, from_str], self.phone)
        return result


@dataclass
class Page:
    label: str
    num: int
    token: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Page":
        assert isinstance(obj, dict)
        label = from_str(obj.get("label"))
        num = from_int(obj.get("num"))
        token = from_union([from_none, from_str], obj.get("token"))
        return Page(label, num, token)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_str(self.label)
        result["num"] = from_int(self.num)
        result["token"] = from_union([from_none, from_str], self.token)
        return result


@dataclass
class Pagination:
    pages: List[Page]

    @staticmethod
    def from_dict(obj: Any) -> "Pagination":
        assert isinstance(obj, dict)
        pages = from_list(Page.from_dict, obj.get("pages"))
        return Pagination(pages)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pages"] = from_list(lambda x: to_class(Page, x), self.pages)
        return result


@dataclass
class SearchResultModel:
    ads: List[Ad]
    pagination: Pagination
    total: int

    @staticmethod
    def from_http_response(http_response: Response) -> "SearchResultModel":
        assert isinstance(http_response, Response)
        json_object = http_response.json()
        ads = from_list(Ad.from_dict, json_object.get("ads"))
        pagination = Pagination.from_dict(json_object.get("pagination"))
        total = from_int(json_object.get("total"))
        return SearchResultModel(ads, pagination, total)

    @staticmethod
    def from_dict(obj: Any) -> "SearchResultModel":
        assert isinstance(obj, dict)
        ads = from_list(Ad.from_dict, obj.get("ads"))
        pagination = Pagination.from_dict(obj.get("pagination"))
        total = from_int(obj.get("total"))
        return SearchResultModel(ads, pagination, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ads"] = from_list(lambda x: to_class(Ad, x), self.ads)
        result["pagination"] = to_class(Pagination, self.pagination)
        result["total"] = from_int(self.total)
        return result


def search_result_from_dict(s: Any) -> SearchResultModel:
    return SearchResultModel.from_dict(s)


def search_result_to_dict(x: SearchResultModel) -> Any:
    return to_class(SearchResultModel, x)
