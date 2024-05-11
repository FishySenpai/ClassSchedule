import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Function to scrape class information and send it to the specified endpoint
def scrape_and_send_classes():
    print("Scraping and sending classes...")
    try:
        url = "https://zabdesk.szabist-isb.edu.pk/ZabNoticeboard/StudentNoticeboard.aspx"

        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
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

        # If no classes are found, print a message
        if not classes:
            print("No classes found.")
        else:
            # Send the class information to the specified endpoint
            send_classes_to_endpoint(classes)
    except Exception as e:
        print("Error occurred while scraping and sending classes:", e)

# Function to send class information to the specified endpoint
def send_classes_to_endpoint(classes):
    print("Sending classes to endpoint...")
    try:
        formatted_classes = ""
        for idx, class_info in enumerate(classes, start=1):
            course_name = class_info[3]
            instructor = class_info[4]
            room = class_info[5]
            time_schedule = class_info[6]

            formatted_class = f"{idx}. Course: {course_name}\n" \
                              f"   Instructor: {instructor}\n" \
                               f"   Room: {room}\n" \
                              f"   Time: {time_schedule}\n\n"
            formatted_classes += formatted_class
        url = "https://whin2.p.rapidapi.com/send"

        payload = {"text": str(formatted_classes)}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "ab5260649dmsh1c14116f3d59e38p17de0djsn0e0cd39cc3ff",
            "X-RapidAPI-Host": "whin2.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        print(response.json())
    except Exception as e:
        print("Error occurred while sending classes to endpoint:", e)

print("Running...")

# Schedule the task to run at 11:51 AM Karachi time every day
scrape_and_send_classes()


