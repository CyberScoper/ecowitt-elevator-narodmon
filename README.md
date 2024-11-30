# 🌦️ Ecowitt to Narodmon Data Sender

[![CodeFactor](https://www.codefactor.io/repository/github/cyberscopetoday/ecowitt-elevator-narodmon/badge)](https://www.codefactor.io/repository/github/cyberscopetoday/ecowitt-elevator-narodmon)

This Python script collects weather data from an Ecowitt weather station and sends it to Narodmon, a popular public monitoring service. The script periodically queries the Ecowitt API, extracts all available weather data, and sends it to Narodmon for visualization and tracking.

## ✨ Features

- 📊 Collects data from an Ecowitt weather station using its API.
- 📡 Sends weather data such as temperature, humidity, pressure, wind speed, gust, direction, rainfall rate, solar radiation, and UV index to Narodmon.
- 🔄 Designed to run continuously, sending updates every 5 minutes.
- 🐛 Simple logging to console for debug purposes.

## 📋 Requirements

- 🐍 Python 3.7 or higher
- 🌦️ Ecowitt weather station with API access enabled
- 📡 Narodmon account to monitor and share weather data

## 🚀 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/CyberScopeToday/ecowitt-elevator-narodmon.git
   cd ecowitt-elevator-narodmon
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Usage

1. Update the configuration parameters in `bot.py`:

   - Set your Ecowitt API credentials:
     - `ecowitt_application_key`
     - `ecowitt_api_key`
     - `ecowitt_mac`
   
   - Set your Narodmon device MAC address:
     - `narodmon_device_mac`

2. Run the script:

   ```bash
   python bot.py
   ```

3. Optionally, run the script as a service:

   Create a systemd service unit file as follows to run the script as a background service (e.g., `/etc/systemd/system/ecowitttonarodmon.service`):

   ```ini
   [Unit]
   Description=Ecowitt to Narodmon Data Sender
   After=network.target

   [Service]
   User=root
   WorkingDirectory=/home/server/ecowitttonarodmon
   ExecStart=/home/server/ecowitttonarodmon/venv/bin/python /home/server/ecowitttonarodmon/bot.py
   Restart=always
   RestartSec=5
   Environment="PYTHONPATH=/home/server/ecowitttonarodmon/venv/bin/python"
   StandardOutput=file:/var/log/ecowitttonarodmon.log
   StandardError=file:/var/log/ecowitttonarodmon.log

   [Install]
   WantedBy=multi-user.target
   ```

   Then enable and start the service:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ecowitttonarodmon.service
   sudo systemctl start ecowitttonarodmon.service
   ```

## 🔧 Configuration Parameters

- `ecowitt_application_key`: Your Ecowitt application key.
- `ecowitt_api_key`: Your Ecowitt API key.
- `ecowitt_mac`: MAC address of the Ecowitt weather station.
- `narodmon_device_mac`: MAC address of your Narodmon device.

## 📜 Logs

Logs will be stored at `/var/log/ecowitttonarodmon.log`. You can check them with:

```bash
cat /var/log/ecowitttonarodmon.log
```

## 🤝 Contributing

Feel free to submit pull requests, open issues, and suggest features. Contributions are always welcome! 🙌

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- 🌦️ Ecowitt for providing their weather station API.
- 📡 Narodmon for enabling public data monitoring.

