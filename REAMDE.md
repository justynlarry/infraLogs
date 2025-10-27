# Infralogs - Log collector and Visualizer
## Architecture Overview (Plan):
- Each VM runs a Dockerized Log API Agent that exposes system logs via a controlled endpoint (instead of SSH).
- A central Python Log Collector (in its own Docker container) polls or subscribes to those APIs daily, parses the logs (using journalctl -o verbose output), and writes selected fields into a MySQL database (with replication).
- The MySQL layer is secured and credentialed through HashiCorp Vault, which manages and rotates passwords automatically via a Kubernetes sidecar pattern.
- The Python Bokeh visualization service connects to the MySQL replica and displays metrics and trends on an internal dashboard (accessible through VPN).
- Password rotation between Bokeh ↔ MySQL (the visible interface layer).
- Eventually, Jenkins will orchestrate Docker builds and Kubernetes deployments (CI/CD).


```
                   ┌──────────────────────────────────────────┐
                   │                Kubernetes                │
                   │   (Orchestrates Collector, Bokeh, Vault) │
                   └──────────────────────────────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │         HashiCorp Vault        │
                    │   - Secret storage & rotation  │
                    │   - Issues MySQL credentials   │
                    └────────────────────────────────┘
                          │                   |
                          |                   |                           
                          |                   |  
                          |                   | 
                          ▼                   ▼
           ┌──────────────────────┐        ┌────────────────────────┐
           │  Python Log Collector│        │ Python Bokeh Dashboard │
           │ (Docker Container)   │        │ (Docker Container)     │
           │  - Polls VM APIs     │        │  - Reads from replica  │
           │  - Writes to MySQL   │        │  - Displays metrics    │
           │  - Auth via Vault    │        │  - Auth via Vault      │
           └─────────┬────────────┘        └──────────────┬─────────┘
              ▲      │                                    │
              │      │                                    ▼
              │      │                       ┌────────────────────────┐          ┌────────────────────────┐
              │      └──────────────────────>│   MySQL Primary        │<--rep--->│   MySQL Replica        │
              │                              │   (writes from coll.)  │          │   (reads by Bokeh)     │
              │                              └────────────────────────┘          └────────────────────────┘
              │       
              │
     ┌──────────────────────────────────────────────┐
     │         VM Fleet (Each VM = Dockerized API)  │
     │----------------------------------------------│
     │ API Container runs:                          │
     │  - journalctl parser                         │
     │  - exposes /logs endpoint (token protected)  │
     └──────────────────────────────────────────────┘
```


# Planning / Phases
## Phase 0 - Asset Creation
- 1 VM hosting the Metrics Server for:
  - Python Log Collector
  - K3s Master Node
  - HashiCorp Vault
  - Bokeh Dashboard

- 2 VMs hosting MySQL DBs in Docker containers:

## Phase 1 - Create Log Collector on sys-monitor VM
a.  Write Python Code for Log Collector
b.  Install K3s on sys-monitor as Master
c.  Create K3s service for Collector

## Phase 2 - Create MySQL Databases
a.  Create MySQL Database on db-svr01 and Replica on db-svr02 in Docker Containers
### Fields:
  - TIMESTAMP
  - MESSAGE
  - _HOSTNAME
  - _COMM
  - _PID
  - PRIORITY
  - SYSLOG_IDENTIFIER

b.  Test System on Dummy VMs to make sure it correctly stores log data

## Phase 3 - Create Basic Dashboard in Python-Bokeh
a.  Write Python code for Bokeh Dashboard

b.  Import from db-svr01

c.  Ensure Functionality -> Flesh out once full system is completed, need an ugly, functional instance

## Phase 4 - Create Hasicorp Vault for Password Rotation between Web Interface and MySQL Database

## Phase X
Clean up, and flesh out

## Phase Y
Begin turning Password Rotator System into a Modular 'Plug In', that can be exported and used for a variety of scenarios.

# Logs Quick Reference:
 Quick Reference
## Code	Level Name	Meaning
```
0	emerg	System is unusable
1	alert	Immediate action required
2	crit	Critical condition
3	err	Error condition
4	warning	Warning condition
5	notice	Normal but significant condition
6	info	Informational
7	debug	Debug-level message
```

