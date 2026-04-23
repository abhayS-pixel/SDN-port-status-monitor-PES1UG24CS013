
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

## Where To Run What

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

## Expected Output

In the controller terminal :

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
This project uses 3 switches and 2 ports each.

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
