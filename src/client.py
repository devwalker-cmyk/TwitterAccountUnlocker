from httpx import Client

from typing import Dict, Optional, List
from uuid import uuid4
from enum import Enum
from .utils import get_random_proxies


class AccountStatus(Enum):
    ACTIVE = 0
    LOCKED = 1
    SUSPENDED = 2
    DEACTIVATED = 3
    UNKNOWN = 4


class SessionManager:
    def __init__(self, proxies: Optional[List[str]] = None) -> None:
        self.proxies = proxies

    @property
    def account_statuses(self) -> Dict[int, AccountStatus]:


        EXCEPTIONS = {
            326: AccountStatus.LOCKED,
            64: AccountStatus.SUSPENDED ,
            141: AccountStatus.SUSPENDED,
            200: AccountStatus.ACTIVE,
            32 : AccountStatus.DEACTIVATED
        }

        return EXCEPTIONS

    def check_token(self, token: str) -> AccountStatus:
        session = self.init_session(token)
        check = session.post(
            "https://x.com/i/api/1.1/account/update_profile.json"
        )
        status = self.account_statuses.get(check.status_code, AccountStatus.UNKNOWN)
        return status


    def init_session(self, token: str) -> Client:
        session = Client(
            proxies=get_random_proxies(self.proxies),
            timeout=30
        )
        session.cookies["auth_token"] = token
        
        self._get_cookies(session)
        return session

    def _get_cookies(self, session: Client) -> None:
        try:
            session.headers = {
                "authority": "x.com",
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.7",
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "content-type": "application/json",
                "referer": "https://x.com/",
                "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="120", "Chromium";v="120"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "x-client-uuid": str(uuid4()),
                "x-twitter-active-user": "yes",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "en",
            }
            session.post(
                "https://x.com/i/api/1.1/account/update_profile.json"
            )
            session.headers["x-csrf-token"] = session.cookies.get("ct0")
        except TimeoutError:
            return