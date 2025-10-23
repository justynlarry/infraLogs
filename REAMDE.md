# Infralogs - Log collector and Visualizer


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
