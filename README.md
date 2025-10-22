📦 What Is This Tool?
This tool is a map-based fleet tracking and route visualization system built using React Leaflet and integrated with ELD (Electronic Logging Device) data. It allows fleet managers and logistics operators to:

View real-time vehicle locations

Visualize routes between pickup and dropoff points

Track driving history and logs

Ensure compliance with Hours of Service (HOS) regulations

🚛 What Is an ELD?
An Electronic Logging Device (ELD) is a hardware unit that connects to a commercial vehicle’s engine and automatically records:

Driving time

Engine hours

Vehicle movement

Location data

Driver identification

ELDs are mandated by the FMCSA (Federal Motor Carrier Safety Administration) to replace paper logs and older AOBRD systems. They help ensure drivers follow legal limits on driving hours and rest periods.

⚙️ How Does ELD Work?
Hardware Connection: ELD plugs into the vehicle’s engine via OBD-II, 6-pin, or 9-pin connector.

Data Sync: It syncs with a mobile app or tablet via Bluetooth or USB.

Automatic Logging: It records engine status, motion, and HOS data in real time.

Cloud Dashboard: Data is sent to a cloud platform where fleet managers can monitor trips, violations, and performance.

🗺️ How This Tool Uses ELD Data
This tool uses ELD-generated data to:

Plot vehicle routes on a map using Leaflet

Show pickup and dropoff locations

Display route lines based on actual driving paths

Optionally show driving logs and mileage

Help visualize compliance and efficiency

🛠️ Technologies Used
React + React Leaflet for interactive maps

Leaflet Routing Machine for route visualization

Django (optional) for backend data management

ELD device integration via API or raw data logs
