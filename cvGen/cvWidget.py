import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QComboBox, QFileDialog
from qfluentwidgets import (LineEdit, TextEdit,
                            ScrollArea, StrongBodyLabel, MessageBox)
from xhtml2pdf import pisa

local_app_data = os.path.join(os.getenv("LocalAppData"), "cvGen")
print(local_app_data)
local_app_data = local_app_data.replace("\\", "/")
print(local_app_data)

css_temp1 = "resource/html_templates/temp1/resume.css"


class ResumeBuilderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # Group for personal information
        personal_info_group = QGroupBox("Personal Information")
        personal_info_layout = QVBoxLayout(personal_info_group)

        # Combo box for template selection
        self.template_combo_box = QComboBox(self)
        items = ["Template 1", "Template 2", "Template 3"]
        self.template_combo_box.addItems(items)
        self.template_combo_box.currentTextChanged.connect(self.handle_layout)
        main_layout.addWidget(self.template_combo_box)

        self.labels_and_fields = [
            ("Name *", LineEdit()),
            ("Position *", LineEdit()),  # Add a line edit field for position
            ("Location *", LineEdit()),
            ("Email *", LineEdit()),
            ("Phone *", LineEdit()),
            ("Website", LineEdit())
        ]

        for label, field in self.labels_and_fields:
            label_widget = StrongBodyLabel()
            label_widget.setText(label)
            label_widget.setStyleSheet("color: white;")
            personal_info_layout.addWidget(label_widget)
            personal_info_layout.addWidget(field)

        main_layout.addWidget(personal_info_group)

        # Group for social networks
        self.social_networks_group = QGroupBox("Social Networks")
        social_networks_layout = QVBoxLayout(self.social_networks_group)

        self.social_network_fields = []
        for network in ["LinkedIn", "GitHub"]:
            network_label = StrongBodyLabel()
            network_label.setText(network)
            network_label.setStyleSheet("color: white;")
            network_field = LineEdit()
            social_networks_layout.addWidget(network_label)
            social_networks_layout.addWidget(network_field)
            self.social_network_fields.append((network, network_field))

        main_layout.addWidget(self.social_networks_group)

        # Group for summary
        summary_group = QGroupBox("")
        summary_layout = QVBoxLayout(summary_group)

        summary_label = StrongBodyLabel()
        summary_label.setText("Summary (Tell us what you do in 1 or two lines)")
        summary_label.setStyleSheet("color: white;")
        summary_layout.addWidget(summary_label)

        self.summary_field = TextEdit()
        summary_layout.addWidget(self.summary_field)

        main_layout.addWidget(summary_group)

        # Group for technical skills
        technical_group = QGroupBox("")
        technical_layout = QVBoxLayout(technical_group)

        technical_label = StrongBodyLabel()
        technical_label.setText("Technical Skills (Separate each skill by comma)")
        technical_label.setStyleSheet("color: white;")
        technical_layout.addWidget(technical_label)

        self.technical_textbox = TextEdit()
        self.technical_textbox.setText("Python, Figma, GitHub")
        technical_layout.addWidget(self.technical_textbox)

        main_layout.addWidget(technical_group)

        # Group for talents
        talent_group = QGroupBox("")
        talent_layout = QVBoxLayout(talent_group)

        talent_label = StrongBodyLabel()
        talent_label.setText("Talents (Format: Talent(Explanation))")
        talent_label.setStyleSheet("color: white;")
        talent_layout.addWidget(talent_label)

        self.talent_textbox = TextEdit()
        self.talent_textbox.setText("Python(Beginner Level), Java(Expert Level)")
        talent_layout.addWidget(self.talent_textbox)

        main_layout.addWidget(talent_group)

        # Group for experience
        experience_group = QGroupBox("")
        experience_layout = QVBoxLayout(experience_group)
        experience_label = StrongBodyLabel()
        experience_label.setText(
            "Experience (Format: [Company Name]{Role}(Date(Start to End seperated with underscore)))")
        experience_label.setStyleSheet("color: white;")
        experience_layout.addWidget(experience_label)

        self.experience_textbox = TextEdit()
        self.experience_textbox.setText("[Apple]{SDE}(27-12-2023_14-03-2024), [Samsung]{Intern}(27-12-2021_14-02-2023)")
        experience_layout.addWidget(self.experience_textbox)
        main_layout.addWidget(experience_group)

        # Group for education
        education_group = QGroupBox("")
        education_layout = QVBoxLayout(education_group)
        education_label = StrongBodyLabel()
        education_label.setText(
            "Experience (Format: [Institution]{Degree - CGPA}(Date(Start to End seperated with underscore)))")
        education_label.setStyleSheet("color: white;")
        education_layout.addWidget(education_label)
        self.educational_textbox = TextEdit()
        self.educational_textbox.setText(
            "[VIT Vellore]{BTech CSE - 9.1}(27-12-2018_14-03-2022), [NIT Calicut]{MTech}(12-01-2023_14-02-2025)")
        education_layout.addWidget(self.educational_textbox)
        main_layout.addWidget(education_group)

        # Add the "Create" button
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.generate_cv_temp1)  # Connect button clicked signal to generate_cv method
        main_layout.addWidget(create_button)

        # Create scroll area
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create widget to contain the main layout
        scroll_widget = QWidget()
        scroll_widget.setLayout(main_layout)

        # Set the layout of the scroll area to the new widget
        scroll_area.setWidget(scroll_widget)

        # Set main layout of the main widget
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(scroll_area)

        self.handle_layout()

    def handle_layout(self):
        currentSelection = self.template_combo_box.currentText()
        if currentSelection == "Template 1":
            self.social_networks_group.hide()
        else:
            self.social_networks_group.show()

    def get_name(self):
        return self.labels_and_fields[0][1].text()

    def get_location(self):
        return self.labels_and_fields[1][1].text()

    def get_email(self):
        return self.labels_and_fields[2][1].text()

    def get_technical(self):
        technical_skills_text = self.technical_textbox.toPlainText().strip()
        technical_skills_list = [skill.strip() for skill in technical_skills_text.split(',')]
        return technical_skills_list

    def get_education(self):
        education_text = self.educational_textbox.toPlainText().strip()
        education_entries = education_text.split(',')
        education_list = []
        for edu in education_entries:
            edu_parts = edu.split('{')
            if len(edu_parts) == 2:
                institution_part = edu_parts[0].strip()
                if institution_part.startswith('[') and institution_part.endswith(']'):
                    institution = institution_part[1:-1]
                else:
                    institution = institution_part
                details = edu_parts[1].strip(')').split('(')
                if len(details) == 2:
                    degree_parts = details[0].split('-')
                    if len(degree_parts) == 2:
                        degree = degree_parts[0].strip() + " - CGPA: " + degree_parts[1].strip()
                    else:
                        degree = details[0].strip()
                    # Replace underscores with hyphens in the date part
                    date = details[1].strip().replace('_', '-')
                    education_list.append((institution, degree, date))
        return education_list

    def get_phone(self):
        return self.labels_and_fields[3][1].text()

    def get_website(self):
        return self.labels_and_fields[4][1].text()

    def get_position(self):
        return self.labels_and_fields[1][1].text()  # Get text from the position field

    def get_linkedin(self):
        return self.social_network_fields[0][1].text()

    def get_github(self):
        return self.social_network_fields[1][1].text()

    def get_summary(self):
        return self.summary_field.toPlainText()

    def get_experience(self):
        return self.experience_textbox.toPlainText()

    def generate_cv_temp1(self):
        with open(f'{local_app_data}/resource/html_templates/temp1/srt-resume.html', 'r') as html_file:
            html_template = html_file.read()

        name = self.get_name()
        phone = self.get_phone()
        email = self.get_email()
        position = self.get_position()  # Get position from the new field
        location = self.get_location()
        website = self.get_website()
        li = self.get_linkedin()
        git = self.get_github()
        summary = self.get_summary()

        # Replace placeholders in the HTML template with the corresponding values
        html_template = html_template.replace('{name}', name)
        html_template = html_template.replace('{phone}', phone)
        html_template = html_template.replace('{position}', position)
        html_template = html_template.replace('{email}', email)
        html_template = html_template.replace('{location}', location)
        html_template = html_template.replace('{website}', website)
        html_template = html_template.replace('{linkedin}', li)
        html_template = html_template.replace('{github}', git)
        html_template = html_template.replace('{summary}', summary)

        # Generate talent sections
        talents = self.talent_textbox.toPlainText().strip()  # Get talents input from the textbox
        talent_list = talents.split(',') if talents else []  # Split talents by comma
        talent_section = ""
        for talent in talent_list:
            talent_heading, talent_description = talent.split('(')  # Split talent into heading and description
            talent_description = talent_description.strip(')')  # Remove closing parenthesis
            # Add talent HTML section
            talent_section += f"<div class='talent'>\n<h2>{talent_heading}</h2>\n<p>{talent_description}</p>\n</div>\n"

        # Replace {talent} placeholder in the HTML template with the talent sections
        html_template = html_template.replace('{talent}', talent_section)

        # Retrieve education data
        education_data = self.get_education()

        # Generate HTML content for education
        education_content = ""
        for institution, degree, date in education_data:
            education_content += f"<h2>{institution}</h2>\n"
            # Remove curly brackets from degree if present
            degree = degree.replace('{', '').replace('}', '')
            education_content += f"<h3>{degree}</h3>\n"
            education_content += f"<p>Date: {date}</p>\n"
            # Add line break after each college detail
            education_content += "<br/>\n"

        # Replace the placeholder with the education content in the HTML template
        html_template = html_template.replace('{education_placeholder}', education_content)

        # Replace placeholder for technical skills
        technical_skills = self.get_technical()
        technical_skills_section = ""
        for skill in technical_skills:
            technical_skills_section += f"<li>{skill}</li>"
        html_template = html_template.replace('{technical_list_items}', technical_skills_section)

        # Generate experience section
        experience_text = self.experience_textbox.toPlainText()
        experience_entries = experience_text.split(',')
        experience_content = ""
        for exp in experience_entries:
            exp_parts = exp.split('{')
            if len(exp_parts) == 2:
                company_part = exp_parts[0].strip()  # Remove leading/trailing whitespace
                if company_part.startswith('[') and not company_part.endswith(']'):
                    # Adjust company name if it starts with '[' but does not end with ']'
                    company = company_part[1:]  # Remove the leading '['
                else:
                    company = company_part.strip('[]')  # Remove brackets if present
                dates_role = exp_parts[1].strip(')').split('(')
                if len(dates_role) == 2:
                    role = dates_role[0].strip('{}')  # Remove curly braces
                    dates = dates_role[1].strip()
                    # Replace underscores with hyphens in the dates
                    dates = dates.replace('_', '-')
                    dates_str = f"<h4>{dates}</h4>"
                    experience_content += f"<div class='job'>\n<h2>{company}</h2>\n<h3>{role}</h3>\n{dates_str}\n</div>\n"

        # Replace the placeholder in the HTML template with the experience content
        html_template = html_template.replace('{experience_placeholder}', experience_content)

        print(html_template)
        self.save_as_html(html_content=html_template)

    def save_as_html(self, html_content):
        css_file_path = f'{local_app_data}/resource/html_templates/temp1/resume.css'
        # Ask the user to select the directory to save files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        save_path = file_dialog.getExistingDirectory(self, "Select Directory to Save Files", ".")

        if save_path:
            try:
                # Create a folder named "output" in the selected directory
                output_folder_path = os.path.join(save_path, "cv")
                os.makedirs(output_folder_path, exist_ok=True)

                # Generate HTML file path
                html_file_path = os.path.join(output_folder_path, "output.html")

                # Move the CSS file to the output folder
                # css_file_name = os.path.basename(css_file_path)
                # css_file_destination = os.path.join(output_folder_path, css_file_name)
                # os.rename(css_file_path, css_file_destination)

                css_temp = css_temp1

                # Write HTML content to output HTML file
                with open(html_file_path, "w") as html_file:
                    html_file.write(html_content)

                    # Copy CSS file to the output folder
                    css_file_name = "resume.css"
                    css_file_destination = os.path.join(output_folder_path, css_file_name)

                    if not os.path.exists(css_file_destination):
                        open(css_file_destination, 'a').close()
                        with open(css_temp, "r") as csstemp1:
                            css_temp1_data = csstemp1.read()
                        with open(css_file_destination, 'w') as new_css:
                            new_css.write(css_temp1_data)

                # Show success message
                w = MessageBox(
                    'Success!',
                    "You can now find your HTML file and CSS file in the 'output' folder within the chosen directory. Have fun!",
                    self
                )
                w.yesButton.setText('Alright blud!')
                w.cancelButton.setText('Cool')
                w.exec()

            except Exception as e:
                print("Exc: ", e)
                w = MessageBox(
                    'Error!',
                    str(e),
                    self
                )
                w.yesButton.setText('Alright blud!')
                w.cancelButton.setText('Let me try again')
                w.exec()
