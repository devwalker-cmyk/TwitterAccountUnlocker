
from typing import Dict, Optional, List
import random



def get_random_proxies(proxies: Optional[List[str]]) -> Optional[Dict[str, str]]:
    if not proxies:
        return None
    proxy = random.choice(proxies)
    proxy_dict = {"all://": f"http://{proxy}"}
    return proxy_dict