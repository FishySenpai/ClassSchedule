import requests
from bs4 import BeautifulSoup

# Function to scrape class information and send it to the specified endpoint
def scrape_and_send_classes():
    url = "https://zabdesk.szabist-isb.edu.pk/ZabNoticeboard/StudentNoticeboard.aspx"

    # Fetch the webpage content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table element
    table = soup.find("table")

    # Find all rows in the table
    rows = table.find_all("tr")

    # Initialize a list to store class information
    classes = []

    # Loop through each row and extract data for BSCS 5B
    for row in rows:
        # Find all cells in the row
        cells = row.find_all("td")

        # Check if the row contains data for BSCS 5B in the class/section column
        if len(cells) >= 3 and "5 B" in cells[2].text.strip():
            # Extract class information
            class_info = [cell.text.strip() for cell in cells]
            classes.append(class_info)

    # Send the class information to the specified endpoint
    send_classes_to_endpoint(classes)

# Function to send class information to the specified endpoint
def send_classes_to_endpoint(classes):
    url = "https://whin2.p.rapidapi.com/send"

    payload = {"text": str(classes)}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "325a7f72damshf16ffcb2c3ed7bep1f566djsn006db2e1a65a",
        "X-RapidAPI-Host": "whin2.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())

# Call the function to scrape class information and send it to the endpoint
scrape_and_send_classes()
