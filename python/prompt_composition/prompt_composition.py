from bs4 import BeautifulSoup
import ast
from requests import get
from functools import partial


def get_data(url: str) -> dict:
    """Fetch arbitrary data"""
    print("                                                    > Fetching data")
    data = get(url)
    return data.json()

def get_members(policy_no: int) -> list:
    """Return a list of members for the policy"""
    return ["Bob Chop", "Harry Houndini", "The other Guy"]

def process_prompt(raw_prompt_text: str, roles: list, consents: list, fetches: dict[callable]) -> str:
    """Process the `raw_prompt_string` and insert data if role appropriate."""

    soup = BeautifulSoup("<root>" + raw_prompt_text + "</root>", "xml")
    # for tag in soup.find_all("claim_data"):
    for tag in soup.find_all(True):
        fetch_name = tag.get("callable")
        if fetch_name:
            del tag["callable"]

            # We have a tag for which data is defined
            roles_attr = tag.get("requires_roles")
            if roles_attr:
                required_roles = ast.literal_eval(roles_attr)
                if any(role in roles for role in required_roles):
                    # Authorised
                    func = fetches[fetch_name]  # Get the function to call for the data based on the tag name
                    tag.append(str(func()) + "\n")
                    del tag["requires_roles"]
                else:
                    tag.replace_with("Data omitted due to insufficient permissions.")

            consents_attr = tag.get("requires_consents")
            if consents_attr:
                requires_consents = ast.literal_eval(consents_attr)
                if any(consent in consents for consent in requires_consents):
                    # Authorised
                    func = fetches[fetch_name]  # Get the function to call for the data based on the tag name
                    tag.append(str(func()) + "\n")
                    del tag["requires_consents"]
                else:
                    tag.replace_with("Consent is required to view this data")



    final_output = "".join(str(child) for child in soup.find("root").contents)
    return final_output.strip()


markdown_template = """
Prompt
======

# Claim Analysis
<sec_fence callable="claim_data" requires_roles="['PP', 'PHA']">
</sec_fence>

# View Policy
<sec_fence callable="list_members" requires_consents="['VIEW_POLICY']">
</sec_fence>
"""


fetches = {
    "claim_data": partial(get_data, 'https://jsonplaceholder.typicode.com/todos/1'),
    "list_members": partial(get_members, 1234)
}
"""A dictionary defining functions to be called to insert data as defiend by the 'callable' attribute."""


print("\n================================================  1. Spouse prompt")
print(process_prompt(markdown_template, roles=["CH"], consents=[], fetches=fetches))

print("\n#================================================ 2. Principle pass")
print(process_prompt(markdown_template, roles=["PH", "PP"], consents=["VIEW_POLICY"], fetches=fetches))

