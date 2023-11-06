import scrapy
import pdfplumber
import csv

class CarbonMetricsSpider(scrapy.Spider):
    name = "carbon_metrics"

    # Define the path to the local PDF file you want to extract text from
    local_pdf_path = r"C:\Users\user\OneDrive\Desktop\Planvivo_goldstd_PDD\carbon_metrics\carbon_metrics\PROJ_DESC_983_18MAR2013.pdf"

    # Define the keywords for the data metrics you want to search for
    metric_keywords = ["Project Title", "Project ID", "Project Proponent", "Other Entities"]

    def start_requests(self):
        try:
            with pdfplumber.open(self.local_pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                yield scrapy.Request(url='file://', body=text, callback=self.parse)

                # Create a CSV file to store the extracted data
                with open('carbon_metrics.csv', 'w', newline='') as csvfile:
                    fieldnames = ["Metric Name", "Metric Value"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
        except Exception as e:
            self.logger.error(f"Error reading the PDF: {str(e)}")

    def parse(self, response):
        extracted_text = response.body.decode('utf-8')

        # Search for and log the specified metric keywords
        for keyword in self.metric_keywords:
            if keyword in extracted_text:
                start_index = extracted_text.index(keyword)
                end_index = start_index + len(keyword)

                # Extract text around the keyword to provide context if needed
                start_context = max(0, start_index - 50)
                end_context = end_index + 50
                metric_text = extracted_text[start_context:end_context]

                # Write the extracted metric to the CSV file
                with open('carbon_metrics.csv', 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=["Metric Name", "Metric Value"])
                    writer.writerow({"Metric Name": keyword, "Metric Value": metric_text})
