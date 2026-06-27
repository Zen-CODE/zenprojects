from bs4 import BeautifulSoup
import ast
from requests import get
from functools import partial


def get_data(url: str) -> dict:
    """Fetch arbitrary data"""
    print("                                                    > Fetching data")
    data = get(url)
    return data.json()


def process_prompt(raw_prompt_text: str, roles: list, fetches: dict[callable]) -> str:
    """Process the `raw_prompt_string` and insert data if role appropriate."""

    soup = BeautifulSoup("<root>" + raw_prompt_text + "</root>", "xml")
    # for tag in soup.find_all("claim_data"):
    for tag in soup.find_all(True):
        if tag.name in fetches:

            # We have a tag for which data is defined
            roles_attr = tag.get("required_roles")
            if roles_attr:
                required_roles = ast.literal_eval(roles_attr)
                if any(role in roles for role in required_roles):
                    # Authorised
                    func = fetches[tag.name]  # Get the function to call for the data based on the tag name
                    tag.append(str(func()) + "\n")
                    del tag["required_roles"]
                else:
                    tag.replace_with("Data omitted due to insufficient permissions")

    final_output = "".join(str(child) for child in soup.find("root").contents)
    return final_output.strip()

markdown_template = """

Claim Analysis
--------------
<claim_data required_roles="['PP', 'PHA']">
</claim_data>
"""


fetches = {"claim_data": partial(get_data, 'https://jsonplaceholder.typicode.com/todos/1')}


print("\n# 1. Spouse pass")
print(process_prompt(markdown_template, roles=["CH"], fetches=fetches))

print("\n#2. Principle pass")
print(process_prompt(markdown_template, roles=["PH", "PP"], fetches=fetches))

