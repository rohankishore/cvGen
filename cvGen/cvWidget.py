import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QGroupBox, QPushButton
from qfluentwidgets import (NavigationBar, NavigationItemPosition, MessageBox, LineEdit, TextEdit,
                            isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget, ScrollArea, StrongBodyLabel, PushButton)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, TitleBar


class ResumeBuilderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # Group for personal information
        personal_info_group = QGroupBox("Personal Information")
        personal_info_layout = QVBoxLayout(personal_info_group)

        self.labels_and_fields = [
            ("Name *", LineEdit()),
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
        social_networks_group = QGroupBox("Social Networks")
        social_networks_layout = QVBoxLayout(social_networks_group)

        self.social_network_fields = []
        for network in ["LinkedIn", "GitHub"]:
            network_label = StrongBodyLabel()
            network_label.setText(network)
            network_label.setStyleSheet("color: white;")
            network_field = LineEdit()
            social_networks_layout.addWidget(network_label)
            social_networks_layout.addWidget(network_field)
            self.social_network_fields.append((network, network_field))

        main_layout.addWidget(social_networks_group)

        # Group for summary
        summary_group = QGroupBox("")
        summary_layout = QVBoxLayout(summary_group)

        summary_label = StrongBodyLabel()
        summary_label.setText("Summary")
        summary_label.setStyleSheet("color: white;")
        summary_layout.addWidget(summary_label)

        self.summary_field = TextEdit()
        summary_layout.addWidget(self.summary_field)

        main_layout.addWidget(summary_group)

        # Group for education
        education_group = QGroupBox("Education *")
        education_layout = QVBoxLayout(education_group)

        self.education_fields = []
        education_labels = ["Start Date *", "End Date *", "Highlights", "Institution *", "Area *", "Degree *"]

        for label in education_labels:
            field = LineEdit() if label != "Highlights" else TextEdit()
            field_label = StrongBodyLabel()
            field_label.setText(label)
            field_label.setStyleSheet("color: white;")
            education_layout.addWidget(field_label)
            education_layout.addWidget(field)
            self.education_fields.append(field)

        main_layout.addWidget(education_group)

        # Add the "Create" button
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.generate_cv)  # Connect button clicked signal to generate_cv method
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

    def generate_cv(self):
        cv_data = "<!DOCTYPE html>\n<html>\n<head>\n<title>Curriculum Vitae</title>\n</head>\n<body>\n"

        cv_data += "<h1 style='color: #FFA500;'>Curriculum Vitae</h1>\n\n"

        cv_data += "<h2 style='color: #FFA500;'>Personal Information</h2>\n"
        for label, field in self.labels_and_fields:
            clean_label = label.replace('*', '')
            cv_data += f"<p><strong>{clean_label}:</strong> {field.text()}</p>\n"

        cv_data += "<h2 style='color: #FFA500;'>Social Networks</h2>\n"
        for network, field in self.social_network_fields:
            clean_network = network.replace('*', '')
            cv_data += f"<p><strong>{clean_network}:</strong> {field.text()}</p>\n"

        cv_data += "<h2 style='color: #FFA500;'>Summary</h2>\n"
        cv_data += f"<p>{self.summary_field.toPlainText()}</p>\n"

        cv_data += "<h2 style='color: #FFA500;'>Education</h2>\n"
        for field in self.education_fields:
            try:
                cv_data += f"<p>{field.toPlainText()}</p>\n"
            except AttributeError:
                cv_data += f"<p>{field.text()}</p>\n"

        cv_data += "</body>\n</html>"

        # You can further process the `cv_data` here (e.g., convert it to PDF, etc.)
        cv_data = cv_data.replace('*', '')
        print(cv_data)