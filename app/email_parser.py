import re

def parse_email(email_address: str):
    """
    Parses an email address to extract the local part, domain,
    and attempts to derive a first name, last name, and full name.

    Args:
        email_address (str): The email address to parse.

    Returns:
        dict: A dictionary containing 'local_part', 'domain', 'first_name', 'last_name', 'full_name'.
              Returns None for any field if it cannot be extracted.
    """
    if not isinstance(email_address, str) or "@" not in email_address:
        print(f"Error: Invalid email address format: {email_address}")
        return {
            "local_part": None,
            "domain": None,
            "first_name": None,
            "last_name": None,  # Added last_name
            "full_name": None
        }

    try:
        local_part, domain = email_address.split("@", 1)
        first_name = None
        last_name = None    # Initialize last_name
        full_name = None

        # Attempt to extract name from local part
        # Remove common delimiters (., _, -) and non-alphabetic characters, replace with space
        cleaned_local_part = re.sub(r'[^a-zA-Z]+', ' ', local_part).strip()
        name_parts = [part for part in cleaned_local_part.split(' ') if part] # Filter out empty strings from split

        if name_parts:
            # Capitalize each part for proper casing
            capitalized_parts = [part.capitalize() for part in name_parts]

            first_name = capitalized_parts[0]
            if len(capitalized_parts) > 1:
                last_name = capitalized_parts[-1] # Last part as last name
            full_name = ' '.join(capitalized_parts)
        else:
            # Fallback if no alphabetic parts are found (e.g., if local_part was only symbols like '...@domain.com')
            # In this case, first_name and full_name remain None, as intended.
            pass

        return {
            "local_part": local_part,
            "domain": domain.lower(), # Ensure domain is lowercase
            "first_name": first_name,
            "last_name": last_name,   # Include last_name in the return
            "full_name": full_name
        }
    except Exception as e:
        print(f"Error parsing email '{email_address}': {e}")
        return {
            "local_part": None,
            "domain": None,
            "first_name": None,
            "last_name": None,  # Added last_name
            "full_name": None
        }

if __name__ == "__main__":
    # Example Usage:
    email1 = "john.smith@dadaautorepair.com"
    parsed1 = parse_email(email1)
    print(f"Parsing '{email1}': {parsed1}")

    email2 = "jane.doe@example.co.uk"
    parsed2 = parse_email(email2)
    print(f"Parsing '{email2}': {parsed2}")

    email3 = "f.lastname@company.net"
    parsed3 = parse_email(email3)
    print(f"Parsing '{email3}': {parsed3}")

    email4 = "info@startup.org"
    parsed4 = parse_email(email4)
    print(f"Parsing '{email4}': {parsed4}")

    email5 = "no_name_here@domain.com"
    parsed5 = parse_email(email5)
    print(f"Parsing '{email5}': {parsed5}")

    email6 = "another-one@test.xyz"
    parsed6 = parse_email(email6)
    print(f"Parsing '{email6}': {parsed6}")

    email7 = "invalid-email"
    parsed7 = parse_email(email7)
    print(f"Parsing '{email7}': {parsed7}")

    email8 = "singleword@domain.com" # New test case for single word local part
    parsed8 = parse_email(email8)
    print(f"Parsing '{email8}': {parsed8}")

    email9 = "mary-ann.jones@corp.com" # New test case with hyphen and multiple parts
    parsed9 = parse_email(email9)
    print(f"Parsing '{email9}': {parsed9}")
