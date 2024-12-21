# CrackFusion - Track Safety Powered by Zenith

CrackFusion is an innovative railway crack detection system developed by **Team Zenith** for the event **TEJAS**. This project ensures railway safety by identifying defects such as cracks and fractures on tracks. Using piezoelectric sensors, AI-based analysis, and real-time notifications, CrackFusion provides a reliable solution for track monitoring and maintenance.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [System Workflow](#system-workflow)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Overview
CrackFusion leverages acoustic data collected by piezoelectric sensors mounted near the train wheelbase. By analyzing vibrations and sound patterns, it identifies anomalies indicative of potential track damage. The data is processed using a pre-trained AI model, and track managers receive instant notifications of detected issues.

## Features
- **Real-Time Anomaly Detection:** Detects cracks and fractures during train operation.
- **Acoustic Sensor Monitoring:** Utilizes piezoelectric sensors for vibration detection.
- **AI-Powered Analysis:** Employs a pre-trained autoencoder model for efficient anomaly detection.
- **Denoising and Data Processing:** Filters out noise to ensure accurate results.
- **Instant Notifications:** Sends alerts directly to track managers for immediate action.

## Technology Stack
- **Hardware**: Piezoelectric sensors, ADC (Analog-to-Digital Converter)
- **Software**: Python, JSON for data processing
- **Machine Learning**: Autoencoder model for anomaly detection
- **Communication**: Real-time data transfer to the central node

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Nikhil-Gorasa/TEJAS.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TEJAS
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure the piezoelectric sensors and ADC are connected and configured as per the project specifications.

## Usage
1. Run the main Python script to start the system:
   ```bash
   python main.py
   ```
2. Monitor real-time logs for vibration data and anomaly detection.
3. Check for notifications or alerts sent to the designated track managers.

## System Workflow
1. **Data Collection**: Sensors capture vibrations and convert analog signals to digital using ADC.
2. **Data Preprocessing**: Noise is removed, and relevant features are extracted.
3. **Anomaly Detection**: The pre-trained autoencoder analyzes data to detect anomalies.
4. **Notification**: Alerts are sent via a messaging system to the track managers.

## Future Enhancements
- Integration with cloud storage for historical data analysis.
- Enhanced visualization tools for data monitoring.
- Incorporation of additional sensors for comprehensive track health analysis.
- Implementation of predictive maintenance using historical data trends.

## Contributing
We welcome contributions to improve CrackFusion! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and open a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

---
Feel free to explore, contribute, and enhance railway safety with CrackFusion, brought to you by Team Zenith for TEJAS!

