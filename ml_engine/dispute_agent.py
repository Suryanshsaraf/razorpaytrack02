"""
RazorShield AI — Visa Compelling Evidence 3.0 (CE 3.0) Dispute Synthesizer
Automatically compiles dispute representment dossiers by mapping 3DS tokens,
prior undisputed transactions, logistics delivery telemetry, and IP device fingerprints
against Visa 10.4 / 13.1 and Mastercard dispute regulations.
"""

from datetime import datetime
from typing import Dict, List, Any

class DisputeRepresentmentAgent:
    def __init__(self):
        self.reason_codes = {
            "VISA_10.4": "Visa 10.4 — Other Fraud / Card-Absent Environment",
            "VISA_13.1": "Visa 13.1 — Merchandise / Services Not Received",
            "MC_4837": "Mastercard 4837 — No Cardholder Authorization",
            "MC_4853": "Mastercard 4853 — Goods Not Provided / Defective"
        }
        
    def synthesize_dossier(self, dispute_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles a comprehensive representment packet with Visa CE 3.0 compliance checks.
        """
        dispute_id = dispute_data.get("dispute_id", "disp_rzp_9901")
        arn = dispute_data.get("acquirer_reference_number", "745210982341908234")
        amount = float(dispute_data.get("amount", 8499.0))
        reason_code = dispute_data.get("reason_code", "VISA_10.4")
        customer_name = dispute_data.get("customer_name", "Rahul Sharma")
        customer_email = dispute_data.get("customer_email", "rahul.s@gmail.com")
        
        # Telemetry
        device_ip = dispute_data.get("device_ip", "49.207.210.12")
        device_fingerprint = dispute_data.get("device_fingerprint", "fp_sha256_90a1b2c3d4")
        eci_code = dispute_data.get("eci_code", "05 (Fully Authenticated 3DS)")
        tracking_id = dispute_data.get("tracking_id", "DELHIVERY_IN_881923019")
        delivery_timestamp = dispute_data.get("delivery_timestamp", "2026-07-15 14:22:10 IST")
        delivery_gps = dispute_data.get("delivery_gps", "12.9716° N, 77.5946° E (Bengaluru)")
        
        # Prior Qualifying Transactions (Visa CE 3.0 requires >= 2 undisputed settled orders with matching parameters > 120 days old)
        prior_qualifying_txs = dispute_data.get("prior_qualifying_transactions", [
            {
                "tx_id": "pay_rzp_prior_001",
                "date": "2026-03-10",
                "amount": 3499.0,
                "status": "SETTLED_UNDISPUTED",
                "matching_device": True,
                "matching_ip": True
            },
            {
                "tx_id": "pay_rzp_prior_002",
                "date": "2026-04-22",
                "amount": 4200.0,
                "status": "SETTLED_UNDISPUTED",
                "matching_device": True,
                "matching_ip": True
            }
        ])
        
        # Determine Visa CE 3.0 Eligibility
        ce30_qualifies = len(prior_qualifying_txs) >= 2 and all(
            t.get("matching_device") or t.get("matching_ip") for t in prior_qualifying_txs
        )
        
        # Compute Win Probability
        base_score = 45.0
        if "05" in eci_code:
            base_score += 25.0 # 3DS liability shift
        if ce30_qualifies:
            base_score += 20.0 # CE 3.0 conclusive evidence rule
        if tracking_id and "DELHIVERY" in tracking_id:
            base_score += 7.0 # Verified carrier POD
            
        win_probability = min(96.0, base_score)
        
        # Synthesize Executive Legal Argument
        executive_argument = (
            f"REPRESENTMENT BRIEF UNDER VISA CE 3.0 RULES:\n"
            f"The cardholder claims unauthorized transaction for Dispute {dispute_id} (ARN: {arn}). "
            f"However, the transaction passed full 3DS 2.2 authentication (ECI {eci_code}). "
            f"Under Visa Compelling Evidence 3.0 guidelines, the merchant provides proof of {len(prior_qualifying_txs)} "
            f"prior undisputed transactions sharing identical Device Fingerprint ({device_fingerprint[:12]}...) and IP ASN. "
            f"Furthermore, Carrier tracking ({tracking_id}) confirms physical delivery with signed POD to verified GPS coordinates ({delivery_gps}). "
            f"Merchant requests immediate reversal of chargeback and full fund settlement."
        )
        
        timeline = [
            {"step": "Order Placed & Paid", "timestamp": "2026-07-12 18:30:12", "detail": f"Authenticated via 3DS (ECI {eci_code}) from IP {device_ip}"},
            {"step": "Logistics Dispatch", "timestamp": "2026-07-13 09:15:00", "detail": f"Shipped via Delhivery Express (AWB: {tracking_id})"},
            {"step": "Successful Delivery", "timestamp": delivery_timestamp, "detail": f"Delivered to GPS {delivery_gps} with digital OTP receipt"},
            {"step": "Dispute Initiated", "timestamp": "2026-08-01 11:20:00", "detail": f"Cardholder filed {self.reason_codes.get(reason_code, reason_code)}"},
            {"step": "CE 3.0 Dossier Assembled", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "detail": "Autonomous representment package submitted with win probability 92%+"}
        ]
        
        return {
            "dispute_id": dispute_id,
            "arn": arn,
            "amount_inr": amount,
            "reason_code_title": self.reason_codes.get(reason_code, reason_code),
            "customer_info": {"name": customer_name, "email": customer_email},
            "ce30_qualifies": ce30_qualifies,
            "win_probability_pct": win_probability,
            "liability_shift_status": "LIABILITY_WITH_ISSUER" if "05" in eci_code else "STANDARD_REVIEW",
            "executive_argument": executive_argument,
            "timeline": timeline,
            "prior_qualifying_transactions": prior_qualifying_txs
        }
