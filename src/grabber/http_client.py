from typing import Optional

import requests
from requests import Response

from src.constants import Language, Category

BASE_URL = "https://cre-api.kufar.by"
PATH = "/ads-search/v1/engine/v1/search/rendered-paginated"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
)
HEADERS = {
    "authority": "cre-api.kufar.by",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "x-segmentation": "routing=web_generalist;platform=web;application=ad_view",
    "sec-fetch-dest": "empty",
    "user-agent": USER_AGENT,
    "content-type": "application/json",
    "accept": "*/*",
    "origin": BASE_URL,
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "referer": "https://www.kufar.by/listings?query=iphone&ot=1&rgn=7&ar=",
    "accept-language": "en,ru;q=0.9,en-US;q=0.8",
}


class HTTPClient:
    @classmethod
    def _get_params(
        cls,
        search_phrase,
        token,
        size_of_announcement_on_page=42,
        language=Language.RU.value,
        ot=7,
        rgn=7,
        cat: Optional[Category] = None,
    ) -> dict:
        return dict(
            query=search_phrase,
            ot=ot,
            rgn=rgn,
            size=size_of_announcement_on_page,
            lang=language,
            cursor=token,
            cat=cat,
        )

    @classmethod
    def get_ads(
        cls, search_phrase, token: Optional[str], cat: Optional[Category]
    ) -> Response:
        return requests.get(
            url=f"{BASE_URL}{PATH}",
            headers=HEADERS,
            params=cls._get_params(search_phrase, token, cat=cat),
        )
