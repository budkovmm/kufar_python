from dataclasses import dataclass
from typing import List, Any, Optional


@dataclass
class Ad:
    ad_id: int
    subject: str
    ad_link: str
    price_byn: float
    price_usd: float
    category: str

    @staticmethod
    def from_dict(obj) -> "Ad":
        ad_id = obj.get("ad_id")
        subject = obj.get("subject")
        ad_link = obj.get("ad_link")
        category = obj.get("category")
        price_byn = int(obj.get("price_byn")) / 100
        price_usd = int(obj.get("price_usd")) / 100

        return Ad(
            ad_id=ad_id,
            subject=subject,
            ad_link=ad_link,
            price_byn=price_byn,
            price_usd=price_usd,
            category=category,
        )


@dataclass
class Page:
    label: str
    num: int
    token: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Page":
        assert isinstance(obj, dict)
        label = obj.get("label")
        num = obj.get("num")
        token = obj.get("token")
        return Page(label, num, token)


@dataclass
class Pagination:
    pages: List[Page]

    @staticmethod
    def from_dict(obj: Any) -> "Pagination":
        pages = [Page.from_dict(page) for page in obj.get("pages")]
        return Pagination(pages)
