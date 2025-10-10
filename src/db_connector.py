import datetime
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def add_url(original_url: str, short_code: str, validity_days: int):
    """Adds a url to the database.
    Args:
        original_url: The original url string to be shortened.
        short_code: The desired 6 characters long short code to be used after the domain, e.g. ``www.domain.com/<short code>``.
    """
    supabase.table("urls").insert(
        {
            "short_code": short_code,
            "original_url": original_url,
            "expires_at": (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=validity_days)
            ).isoformat(),
        }
    ).execute()


def delete_url(short_code: str):
    """Deletes the database entry referring to ```short_code``.
    Args:
        short_code: The 6 character short code of the desired database entry.
    """
    supabase.table("urls").delete().eq("short_code", short_code).execute()


def delete_expired_urls():
    supabase.table("urls").delete().lt("expires_at", datetime.datetime.now()).execute()


def get_data(short_code: str) -> dict | None:
    """Get all columns of the database entry referring to ```short_code``.
    Args:
        short_code: The 6 character short code of the desired database entry.
    Returns:
        (dict | None): A dictionary containing all database columns and their respective values for the supplied ``short_code`` or None if ``short_code`` does not exist.
    """
    response = supabase.table("urls").select("*").eq("short_code", short_code).execute()
    if len(response.data) == 0:
        return None

    return response.data[0]


def get_url(short_code: str) -> str | None:
    """Get the original url corresponding to ```short_code``.
    Args:
        short_code: The 6 character short code of the desired url.
    Returns:
        (str | None): The url corresponding to ``short_code`` or None if ``short_code`` does not exist.
    """
    data = get_data(short_code)
    if data == None:
        return None

    return data["original_url"]


def increment_clicks(short_code: str):
    """Increment the click count of the url corresponding to ```short_code``.
    Args:
        short_code: The 6 character short code of of the url to increment the clicks for.
    """
    response = (
        supabase.table("urls").select("clicks").eq("short_code", short_code).execute()
    )
    if response.data:
        clicks = response.data[0]["clicks"]
        supabase.table("urls").update({"clicks": clicks + 1}).eq(
            "short_code", short_code
        ).execute()
