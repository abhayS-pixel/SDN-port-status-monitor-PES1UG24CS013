
# SDN-port-status-monitor-PES1UG24CS013
=======
# SDN Mini Project: Port Status Monitoring Tool

This project is for **Topic 13: Port Status Monitoring Tool** in **Computer Networks / SDN**.

The tool monitors switch port status changes in an SDN network and logs:
- which switch changed
- which port changed
- whether the port went `UP`, `DOWN`
- the timestamp of the event
- alert messages for critical port failures
- live status in a browser dashboard

## What This Project Uses

- **Ryu Controller** for SDN control logic
- **Mininet** for network emulation
- **Open vSwitch** as the SDN switch
- **Python 3**

## Important for Mac Users

If you are using a Mac:

- **Ryu controller code can run on macOS**
- **Mininet and Open vSwitch should be run inside Ubuntu/Linux**

### Recommended setup on Mac

Use one of these:

1. **UTM + Ubuntu VM** on Mac
2. **VirtualBox + Ubuntu VM**
3. A Linux lab machine if your college provides one

### Simplest option

Run **everything inside an Ubuntu VM**. This is the easiest and most reliable way for demo and viva.

## Project Structure

```text
sdn-port-status-monitor/
├── controller/
│   └── port_status_monitor.py
├── dashboard/
│   ├── app.py
│   └── templates/
│       └── index.html
├── topo/
│   └── port_status_topology.py
├── scripts/
│   └── demo_steps.sh
├── logs/
│   ├── alerts.log
│   ├── current_status.json
│   └── port_status_log.csv
├── docs/
│   └── PROJECT_REPORT.md
└── requirements.txt
```

## Software Installation

### Inside Ubuntu VM

Open Ubuntu terminal and run:

```bash
sudo apt update
sudo apt install -y python3 python3-pip mininet openvswitch-switch
pip3 install -r requirements.txt
```

If `pip3 install -r requirements.txt` fails because of permissions, use:

```bash
python3 -m pip install --user -r requirements.txt
```

## Where To Run What

### Option A: Recommended

Run **everything inside Ubuntu VM**.

Terminal 1 in Ubuntu:

```bash
cd ~/sdn-port-status-monitor
ryu-manager controller/port_status_monitor.py
```

Terminal 2 in Ubuntu:

```bash
cd ~/sdn-port-status-monitor
python3 dashboard/app.py
```

Terminal 3 in Ubuntu:

```bash
cd ~/sdn-port-status-monitor
sudo python3 topo/port_status_topology.py
```

### Option B: Hybrid setup

If you really want:

- run `ryu-manager controller/port_status_monitor.py` on macOS
- run `sudo python3 topo/port_status_topology.py` inside Ubuntu VM

But then you must edit the controller IP in `topo/port_status_topology.py` so Mininet can reach your Mac.

For college mini-projects, **Option A is better**.

## How To Run the Project

### Step 1: Start the controller

In Ubuntu terminal:

```bash
cd ~/sdn-port-status-monitor
ryu-manager controller/port_status_monitor.py
```

You will see logs when switches connect and when ports change state.

### Step 2: Start the dashboard

In a second Ubuntu terminal:

```bash
cd ~/sdn-port-status-monitor
python3 dashboard/app.py
```

Open this in browser:

```bash
http://127.0.0.1:5000
```

### Step 3: Start the topology

In a third Ubuntu terminal:

```bash
cd ~/sdn-port-status-monitor
sudo python3 topo/port_status_topology.py
```

This opens the **Mininet CLI**.

### Step 4: Test the network

Inside the Mininet CLI:

```bash
pingall
```

### Step 5: Simulate a port failure

Inside the Mininet CLI:

```bash
sh ovs-ofctl -O OpenFlow13 mod-port s1 s1-eth2 down
```

This will bring the port down.

Check the controller terminal. It will print a port status update and an `ALERT` message.
Also check the browser dashboard.

### Step 6: Restore the port

Inside the Mininet CLI:

```bash
sh ovs-ofctl -O OpenFlow13 mod-port s1 s1-eth2 up
```

Again, check the controller terminal and dashboard for the update.

### Step 7: Exit Mininet

Inside Mininet CLI:

```bash
exit
```

If needed, clean Mininet:

```bash
sudo mn -c
```

## Expected Output

In the controller terminal, you should see messages like:

```text
Switch connected: dpid=0000000000000001
Port event -> switch=0000000000000001 port=2 name=s1-eth2 reason=MODIFY state=DOWN
Port event -> switch=0000000000000001 port=2 name=s1-eth2 reason=MODIFY state=UP
ALERT [2026-04-17 12:30:00] switch=0000000000000001 port=2 name=s1-eth2 state=DOWN reason=MODIFY
```

The same events are also stored in:

```text
logs/port_status_log.csv
logs/alerts.log
logs/current_status.json
```

## Viva Explanation

### Problem statement

In SDN networks, administrators need to know when switch ports go up or down so they can quickly detect failures, link problems, or manual configuration changes.

### Objective

To build a controller-based monitoring tool that detects and logs switch port status changes in real time, generates alerts for failures, and displays live status in a dashboard.

### Working

1. Mininet creates the SDN topology.
2. Open vSwitch connects to the Ryu controller.
3. When a switch port changes state, OpenFlow sends a `Port Status` message to the controller.
4. The Ryu app receives the event, decodes it, displays it, saves it to a log file, generates alerts, and updates a live dashboard.

### Applications

- fault monitoring
- link failure detection
- network administration
- SDN troubleshooting
- campus/lab network monitoring

## Files You Should Present

- `controller/port_status_monitor.py`
- `topo/port_status_topology.py`
- `docs/PROJECT_REPORT.md`
- `README.md`

## Topic Coverage Check

This upgraded version now does all required parts of the topic:

- monitors switch port status changes
- detects port up/down events
- logs changes
- generates alerts
- displays current status

## If You Want To Copy This Project Into Ubuntu

From your Mac, copy this folder into the Ubuntu VM and place it somewhere like:

```bash
~/sdn-port-status-monitor
```

Then run the commands from there.

>>>>>>> 7cb47a8 (first commit)
