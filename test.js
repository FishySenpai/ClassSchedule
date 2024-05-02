const axios = require("axios");
const cheerio = require("cheerio");
const schedule = require("node-schedule");

// Function to scrape class information and send it to the specified endpoint
async function scrapeAndSendClasses() {
  const url =
    "https://zabdesk.szabist-isb.edu.pk/ZabNoticeboard/StudentNoticeboard.aspx";

  try {
    // Fetch the webpage content
    const response = await axios.get(url);
    const htmlContent = response.data;

    // Parse the HTML content
    const $ = cheerio.load(htmlContent);

    // Find the table element
    const table = $("table");

    // Find all rows in the table
    const rows = table.find("tr");

    // Initialize an array to store class information
    const classes = [];

    // Loop through each row and extract data for BSCS 5B
    rows.each((index, row) => {
      // Find all cells in the row
      const cells = $(row).find("td");

      // Check if the row contains data for BSCS 5B in the class/section column
      if (cells.length >= 3 && $(cells[2]).text().includes("5 B")) {
        // Extract class information
        const classInfo = cells.toArray().map((cell) => $(cell).text().trim());
        classes.push(classInfo);
      }
    });

    // Send the class information to the specified endpoint
    await sendClassesToEndpoint(classes);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// Function to send class information to the specified endpoint
async function sendClassesToEndpoint(classes) {
  const url = "https://whin2.p.rapidapi.com/send";

  const payload = { text: JSON.stringify(classes) };
  const headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "325a7f72damshf16ffcb2c3ed7bep1f566djsn006db2e1a65a",
    "X-RapidAPI-Host": "whin2.p.rapidapi.com",
  };

  try {
    const response = await axios.post(url, payload, { headers });
    console.log("Response:", response.data);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

// Schedule the task to run at 10 PM every day
schedule.scheduleJob("0 22 * * *", function () {
  scrapeAndSendClasses();
});
