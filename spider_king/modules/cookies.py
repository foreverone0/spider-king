def get_cookies(cookies: str) -> list[dict]:
    """
    把cookies转换为selenium的cookies
    """

    ck = cookies.split(";")
    ck = [c.strip() for c in ck]
    ck = [c.split("=") for c in ck]
    return [
        {
            "name": c[0],
            "value": c[1],
            "path": "/",
        }
        for c in ck
        if len(c) == 2
    ]


def parse_cookies(cookies: list[dict]) -> dict:
    """把selenium的cookies转换为requests的cookies

    Args:
        cookies (list[dict]): _description_

    Returns:
        dict: _description_
    """

    return {c["name"]: c["value"] for c in cookies}
