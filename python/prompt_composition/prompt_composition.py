from bs4 import BeautifulSoup
import ast
from requests import get
from functools import partial


AUTH_DICT = dict[str, list[str]]
"""A standard dict structure for holding user data. e.g {'roles': ['PP', 'PHA']}"""

def get_data(url: str) -> dict:
    """Fetch arbitrary data"""
    print(" > Fetching data -> Pydantic model -|")
    print(" < model_dump_json()               -|")
    data = get(url)
    return data.json()

def get_members(policy_no: int) -> list:
    """Return a list of members for the policy"""
    return ["Bob Chop", "Harry Houndini", "The other Guy"]

def has_all_auth(user_auth: AUTH_DICT, required_auth: AUTH_DICT) -> bool:
    """Return True if the user has all on trhe required authentication, False otherwise"""                
    for required_key, required_values in required_auth.items():
        user_values = user_auth.get(required_key, [])
        if not any(user_value in required_values for user_value in user_values):
            return False
    return True                                                        

def process_prompt(raw_prompt_text: str, user_auth: dict[str, list[str]], fetches: dict[callable]) -> str:
    """Process the `raw_prompt_string` and insert data if role appropriate."""

    soup = BeautifulSoup("<root>" + raw_prompt_text + "</root>", "xml")
    fetch_keys = list(fetches.keys()) 
    for tag in soup.find_all(True):
        if tag.name in fetch_keys:
            # We have a tag for which a data fetch is defined
            auth_attr = tag.get("auth")
            authorised = not bool(auth_attr)
            if not authorised:
                required_auth: dict[str, list[str]] = ast.literal_eval(auth_attr)
                authorised = has_all_auth(user_auth, required_auth)
                                                        
                del tag["auth"]
                if authorised:
                    # TODO: Collects the fetches and run async in parallel
                    func = fetches[tag.name]  # Get the function to call for the data based on the tag name
                    tag.append(str(func()) + "\n")  # TODO: model_dump_json
                else:
                    tag.replace_with("Data omitted due to insufficient permissions.")

    final_output = "".join(str(child) for child in soup.find("root").contents)
    return final_output.strip()


markdown_template = """
Prompt
======

Claim Analysis
--------------
<get_claims  auth="{'roles': ['PP', 'PHA']}">
</get_claims>

Admin and billing
-----------------
<get_admin_and_billing  auth="{'roles': ['PP', 'PHA']}">
</get_admin_and_billing>

Member list
------------
Authorisation requirements are processed as "AND" if in one auth item, "OR" if across multiple

<get_member_list auth="{'consents': ['VIEW_POLICY']}" auth="{'roles': ['PP']}">
User has view policy access or is a PP!
</get_member_list>
"""


fetches = {
    "get_claims": partial(get_data, 'https://jsonplaceholder.typicode.com/todos/1'),
    "get_admin_and_billing": lambda: {"admin": "admin stuff", "billing": "billing stuff"},
    "get_member_list": partial(get_members, 1234)
}
"""A dictionary defining functions to be called to insert data as defiend by the 'callable' attribute."""


print("\n================================================  1. Spouse prompt")
print(process_prompt(markdown_template, user_auth={"roles": ["SP"], "consents": []}, fetches=fetches))

print("\n#================================================ 2. Principle pass")
print(process_prompt(markdown_template, user_auth={"roles": ["PH", "PP"], "consents": ["VIEW_POLICY"]}, fetches=fetches))

