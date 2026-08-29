"""
RazorShield AI — Real-Time Streaming Feature Extractor
Extracts sub-millisecond tabular, behavioral, and geographical risk features from an incoming transaction.
"""

import re
import math
import numpy as np

def score_indian_address_quality(address_str: str) -> float:
    """
    Evaluates address completeness, structure, and presence of valid Indian postal indicators.
    Returns a score between 0.0 (high RTO risk/gibberish) and 1.0 (verified structure).
    """
    if not address_str or len(address_str.strip()) < 8:
        return 0.10
    
    clean_addr = address_str.lower().strip()
    score = 0.50
    
    # Penalize placeholder / suspicious tokens
    suspicious_terms = ["dummy", "fake", "unknown", "test", "asdf", "xyz", "temp", "null", "none", "na", "sample"]
    if any(term in clean_addr for term in suspicious_terms):
        score -= 0.50
        
    # Check for meaningful length
    if len(clean_addr) > 30 and not any(term in clean_addr for term in suspicious_terms):
        score += 0.15
    elif len(clean_addr) < 18:
        score -= 0.20
        
    # Check for common Indian landmark / street anchors
    landmark_keywords = [
        "near", "opp", "opposite", "behind", "beside", "road", "rd", "street", "st",
        "nagar", "colony", "sector", "phase", "block", "floor", "flat", "apartment",
        "cross", "main", "chowk", "gali", "mandi", "layout", "bhavan", "enclave"
    ]
    if any(k in clean_addr for k in landmark_keywords) and not any(term in clean_addr for term in suspicious_terms):
        score += 0.20
        
    # Check for 6-digit Indian PIN code
    if re.search(r'\b[1-9][0-9]{5}\b', clean_addr):
        score += 0.15
        
    # Penalize repetitive characters or gibberish (e.g. "asdfg", "near temple near temple")
    words = clean_addr.split()
    if len(words) > 0 and len(set(words)) / len(words) < 0.6:
        score -= 0.25
        
    if re.search(r'(.)\1{3,}', clean_addr): # repeated chars like "aaaa"
        score -= 0.30

    return max(0.05, min(round(score, 3), 1.0))

class RealtimeFeaturePipeline:
    def __init__(self, cat_mappings=None):
        self.cat_mappings = cat_mappings or {
            "payment_method": {"UPI": 0, "CARD": 1, "NETBANKING": 2, "COD": 3, "WALLET": 4},
            "card_network": {"NA": 0, "VISA": 1, "MASTERCARD": 2, "RUPAY": 3, "AMEX": 4},
            "card_country": {"IN": 0, "US": 1, "SG": 2, "AE": 3, "GB": 4, "RU": 5, "NG": 6}
        }
        
    def transform(self, payload: dict) -> np.ndarray:
        """
        Transforms raw transaction dictionary into model-ready vector.
        Features expected:
        [amount, hour, user_account_age_days, tx_velocity_1h, tx_velocity_24h,
         address_quality_score, otp_attempts, checkout_duration_sec, ip_is_vpn, is_cod,
         payment_method, card_network, card_country]
        """
        amount = float(payload.get("amount", 1000.0))
        hour = int(payload.get("hour", 14))
        user_account_age_days = int(payload.get("user_account_age_days", 180))
        tx_velocity_1h = int(payload.get("tx_velocity_1h", 1))
        tx_velocity_24h = int(payload.get("tx_velocity_24h", 2))
        
        # Address score
        raw_addr = payload.get("shipping_address", "")
        if payload.get("address_quality_score") is not None:
            address_quality_score = float(payload["address_quality_score"])
        else:
            address_quality_score = score_indian_address_quality(raw_addr)
            
        otp_attempts = int(payload.get("otp_attempts", 1))
        checkout_duration_sec = float(payload.get("checkout_duration_sec", 45.0))
        ip_is_vpn = 1 if payload.get("ip_is_vpn", False) else 0
        
        pm = str(payload.get("payment_method", "UPI")).upper()
        is_cod = 1 if pm == "COD" or payload.get("is_cod", False) else 0
        
        card_network = str(payload.get("card_network", "NA")).upper()
        card_country = str(payload.get("card_country", "IN")).upper()
        
        pm_encoded = self.cat_mappings["payment_method"].get(pm, 0)
        cn_encoded = self.cat_mappings["card_network"].get(card_network, 0)
        cc_encoded = self.cat_mappings["card_country"].get(card_country, 0)
        
        cols = [
            "amount", "hour", "user_account_age_days", "tx_velocity_1h", "tx_velocity_24h",
            "address_quality_score", "otp_attempts", "checkout_duration_sec", "ip_is_vpn", "is_cod",
            "payment_method", "card_network", "card_country"
        ]
        values = [
            amount, hour, user_account_age_days, tx_velocity_1h, tx_velocity_24h,
            address_quality_score, otp_attempts, checkout_duration_sec, ip_is_vpn, is_cod,
            pm_encoded, cn_encoded, cc_encoded
        ]
        import pandas as pd
        return pd.DataFrame([values], columns=cols)
