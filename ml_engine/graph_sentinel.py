"""
RazorShield AI — Graph Sentinel & Sybil Ring Detector
Maintains an in-memory heterogeneous entity graph to uncover coordinated fraud rings,
burner device sharing, and mutating UPI VPAs.
"""

import networkx as nx
from typing import Dict, List, Any

class GraphSentinel:
    def __init__(self):
        self.G = nx.Graph()
        self._init_sample_graph()
        
    def _init_sample_graph(self):
        """Initializes a representative graph of clean vs clustered fraud rings."""
        # Clean cluster
        self.add_transaction({
            "transaction_id": "tx_clean_101",
            "user_id": "usr_vikram_89",
            "device_id": "dev_macbook_pro_01",
            "ip_address": "49.207.210.12",
            "upi_vpa": "vikram@okaxis",
            "is_fraud": False
        })
        self.add_transaction({
            "transaction_id": "tx_clean_102",
            "user_id": "usr_vikram_89",
            "device_id": "dev_iphone_15_01",
            "ip_address": "49.207.210.12",
            "upi_vpa": "vikram@okaxis",
            "is_fraud": False
        })
        
        # Fraud Ring: Multiple fake users sharing 1 burner device & VPN subnet
        ring_users = [f"usr_bot_{i}" for i in range(1, 7)]
        shared_device = "dev_burner_emulator_999"
        shared_vpn = "185.220.101.55"
        
        for u in ring_users:
            self.add_transaction({
                "transaction_id": f"tx_sybil_{u}",
                "user_id": u,
                "device_id": shared_device,
                "ip_address": shared_vpn,
                "upi_vpa": f"{u}_fake@paytm",
                "is_fraud": True
            })
            
    def add_transaction(self, tx: Dict[str, Any]):
        tx_id = tx.get("transaction_id", "tx_unknown")
        user_id = tx.get("user_id", "usr_anon")
        device_id = tx.get("device_id", "dev_none")
        ip_addr = tx.get("ip_address", "ip_none")
        vpa = tx.get("upi_vpa", "none")
        is_fraud = tx.get("is_fraud", False)
        
        # Add Nodes with Type attributes
        self.G.add_node(tx_id, type="transaction", is_fraud=is_fraud)
        self.G.add_node(user_id, type="user", is_fraud=is_fraud)
        self.G.add_node(device_id, type="device", is_fraud=is_fraud)
        self.G.add_node(ip_addr, type="ip", is_fraud=is_fraud)
        if vpa != "none":
            self.G.add_node(vpa, type="vpa", is_fraud=is_fraud)
            
        # Add Edges
        self.G.add_edge(user_id, tx_id, relation="INITIATED")
        self.G.add_edge(tx_id, device_id, relation="EXECUTED_ON")
        self.G.add_edge(tx_id, ip_addr, relation="ORIGINATED_FROM")
        if vpa != "none":
            self.G.add_edge(tx_id, vpa, relation="PAID_VIA")
            
    def inspect_entity_ring(self, entity_id: str) -> Dict[str, Any]:
        """Calculates subgraph density and shared entity cardinality."""
        if not self.G.has_node(entity_id):
            return {"in_fraud_ring": False, "cluster_size": 1, "risk_multiplier": 1.0}
            
        # Extract 2-hop ego subgraph
        ego = nx.ego_graph(self.G, entity_id, radius=2)
        n_nodes = len(ego.nodes())
        n_edges = len(ego.edges())
        
        # Count connected users sharing device / IP
        users_in_ego = [n for n, attr in ego.nodes(data=True) if attr.get("type") == "user"]
        devices_in_ego = [n for n, attr in ego.nodes(data=True) if attr.get("type") == "device"]
        
        is_ring = len(users_in_ego) >= 3 and len(devices_in_ego) <= 2
        risk_multiplier = min(2.5, 1.0 + (len(users_in_ego) * 0.25))
        
        return {
            "entity_id": entity_id,
            "in_fraud_ring": is_ring,
            "connected_users_count": len(users_in_ego),
            "connected_devices_count": len(devices_in_ego),
            "subgraph_nodes": n_nodes,
            "subgraph_edges": n_edges,
            "risk_multiplier": risk_multiplier,
            "alert": f"Coordinated Sybil Ring detected: {len(users_in_ego)} users share device '{devices_in_ego[0]}'" if is_ring else "Clean entity neighborhood."
        }
        
    def export_graph_json(self) -> Dict[str, Any]:
        """Exports nodes and links for frontend force-directed visualization."""
        nodes = []
        for n, data in self.G.nodes(data=True):
            nodes.append({
                "id": str(n),
                "type": data.get("type", "entity"),
                "is_fraud": data.get("is_fraud", False),
                "degree": self.G.degree(n)
            })
            
        links = []
        for u, v, data in self.G.edges(data=True):
            links.append({
                "source": str(u),
                "target": str(v),
                "relation": data.get("relation", "CONNECTED")
            })
            
        return {"nodes": nodes, "links": links}
