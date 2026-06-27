from bs4 import BeautifulSoup
import ast
from requests import get
from functools import partial


def get_data(url: str) -> dict:
    """Fetch arbitrary data"""
    print(" > Fetching data -> Pydantic model -|")
    print(" < model_dump_json()               -|")
    data = get(url)
    return data.json()

def get_members(policy_no: int) -> list:
    """Return a list of members for the policy"""
    return ["Bob Chop", "Harry Houndini", "The other Guy"]

def process_prompt(raw_prompt_text: str, user_auth: dict[str, list[str]], fetches: dict[callable]) -> str:
    """Process the `raw_prompt_string` and insert data if role appropriate."""

    soup = BeautifulSoup("<root>" + raw_prompt_text + "</root>", "xml")
    # for tag in soup.find_all("claim_data"):
    for tag in soup.find_all(True):
        fetch_name = tag.get("callable")
        if fetch_name:
            del tag["callable"]

            # We have a tag for which data is defined
            auth_attr = tag.get("auth")
            if auth_attr:
                required_auth: dict[str, list[str]] = ast.literal_eval(auth_attr)
                authorised = False
                for required_auth, required_values in required_auth.items():
                    user_values = user_auth.get(required_auth, [])
                    if any(user_value in required_values for user_value in user_values):
                        authorised = True
                        func = fetches[fetch_name]  # Get the function to call for the data based on the tag name
                        tag.append(str(func()) + "\n")
                                                        
                del tag["auth"]
                if not authorised:
                    tag.replace_with("Data omitted due to insufficient permissions.")

    final_output = "".join(str(child) for child in soup.find("root").contents)
    return final_output.strip()


markdown_template = """
Prompt
======

# Claim Analysis
<sec_fence callable="claim_data" auth="{'roles': ['PP', 'PHA']}">
</sec_fence>

# View Policy
<sec_fence callable="list_members" auth="{'consents': ['VIEW_POLICY']}">
</sec_fence>
"""


fetches = {
    "claim_data": partial(get_data, 'https://jsonplaceholder.typicode.com/todos/1'),
    "list_members": partial(get_members, 1234)
}
"""A dictionary defining functions to be called to insert data as defiend by the 'callable' attribute."""


print("\n================================================  1. Spouse prompt")
print(process_prompt(markdown_template, user_auth={"roles": ["CH"], "consents": []}, fetches=fetches))

print("\n#================================================ 2. Principle pass")
print(process_prompt(markdown_template, user_auth={"roles": ["PH", "PP"], "consents": ["VIEW_POLICY"]}, fetches=fetches))

