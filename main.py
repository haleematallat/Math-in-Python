"""
Test Project for Reef Technologies
Description: Retrieves employee information from Hubstaff API to render time 
             spent on a project into an HTML report. Automation friendly. 
Author: Haleema Tallat
Date Created: 2024-09-17
Last Modified: 2024-09-18
"""
import logging
import os
import json
from datetime import datetime
from src.api.hubstaff_client import HubstaffClient
from src.data_processing.time_formatter import get_dates, parse_relative_date
from src.report.html_generator import generate_org_html
from src.utils.config_reader import Config
from src.utils.email_utils import send_email

logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'
)

logger = logging.getLogger(__name__)

def load_task_config():
    """Load task configuration from task_config.json file."""
    try:
        with open('task_config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("task_config.json file not found. Using defaults.")
        return {}

def process_organization(client, organization, date, output_folder):
    """Process a single organization and generate its report."""
    organization_id = organization['id']
    organization_name = organization['name']

    members = client.get_members(organization_id).get("members", [])
    projects = client.get_projects(organization_id).get("projects", [])
    daily_activities = client.get_daily_activities(organization_id, date).get("daily_activities", [])

    html_report = generate_org_html(organization_name, members, projects, daily_activities, date)

    org_folder = os.path.join(output_folder, organization_name.replace(" ", "_"))
    os.makedirs(org_folder, exist_ok=True)
    report_file_path = os.path.join(org_folder, f'{organization_name}_report.html')

    with open(report_file_path, 'w') as f:
        f.write(html_report)

    print(f"Report for {organization_name} saved to {report_file_path}")
    logger.info(f"HTML table for {organization_name} saved to {report_file_path}")

    return html_report, report_file_path

def main():
    try:
        config = Config()
        task_config = load_task_config()
        
        client = HubstaffClient(config)
        
        # Use date from task_config if enabled, otherwise use get_dates()
        if task_config.get("Task_Config_Enabled", True):
            date_string = task_config.get("date")
            date = parse_relative_date(date_string)  
            date = get_dates(date)  
        else:
            date = get_dates()

        org_data = client.get_org_info()
        
        # Use output_path from task_config if enabled, otherwise use default path
        if task_config.get("Task_Config_Enabled", True):
            output_folder = task_config.get("output_path", "output")
        else:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            output_folder = os.path.join(project_dir, 'output')
        
        os.makedirs(output_folder, exist_ok=True)

        all_reports = []
        all_report_paths = []

        for organization in org_data['organizations']:
            html_report, report_path = process_organization(client, organization, date, output_folder)
            all_reports.append(html_report)
            all_report_paths.append(report_path)

        # Combine all reports if needed
        combined_report = "\n".join(all_reports)
        
        # Send email only if email flag in task_config is true
        if task_config.get("send_email", True):
            send_email(combined_report)

        print(f"All reports have been generated and saved in {output_folder}")
        logger.info(f"All reports have been generated and saved in {output_folder}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()