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
                    │         HashiCorp Vault         │
                    │   - Secret storage & rotation   │
                    │   - Issues MySQL credentials    │
                    └────────────────────────────────┘
                                     │
                                     ▼
           ┌──────────────────────┐        ┌────────────────────────┐
           │  Python Log Collector│        │ Python Bokeh Dashboard │
           │ (Docker Container)   │        │ (Docker Container)     │
           │  - Polls VM APIs     │        │  - Reads from replica  │
           │  - Writes to MySQL   │        │  - Displays metrics    │
           │  - Auth via Vault    │        │  - Auth via Vault      │
           └─────────┬────────────┘        └──────────────┬─────────┘
                     │                                    │
                     ▼                                    ▼
           ┌────────────────────────┐          ┌────────────────────────┐
           │   MySQL Primary        │<--rep--->│   MySQL Replica        │
           │   (writes from coll.)  │          │   (reads by Bokeh)     │
           └────────────────────────┘          └────────────────────────┘
                     ▲
                     │
     ┌──────────────────────────────────────────────┐
     │         VM Fleet (Each VM = Dockerized API)  │
     │----------------------------------------------│
     │ API Container runs:                          │
     │  - journalctl parser                         │
     │  - exposes /logs endpoint (token protected)  │
     └──────────────────────────────────────────────┘
```
