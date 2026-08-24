import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# geocode_address takes an address and returns the latitude and longitude as a tuple.
def geocode_address(
    street: str,
    house_number: str,
    postal_code: str,
    city: str,
) -> tuple[float, float] | None:
    address = f"{street} {house_number}, {postal_code} {city}"

    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "CareLink/1.0"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])

    return latitude, longitude