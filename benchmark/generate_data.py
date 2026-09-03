"""
RazorShield AI — Realistic Indian FinTech & D2C Transaction Generator
Generates a statistically sound dataset representing 100,000 transactions across legitimate shoppers,
Sybil card testing rings, COD Return-To-Origin (RTO) syndicates, Account Takeovers (ATO), and Friendly Fraud disputes.
Includes realistic adversarial noise, stealth proxy rotations, and mutated boundary cases.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def generate_indian_transactions(n_records=100000, output_csv="benchmark/datasets/transactions_100k.csv"):
    set_seed(42)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    
    print(f"[*] Generating {n_records} realistic Indian payment transactions with adversarial noise...")
    
    # Configuration distributions
    payment_methods = ["UPI", "CARD", "NETBANKING", "COD", "WALLET"]
    pm_weights = [0.55, 0.22, 0.08, 0.12, 0.03]
    
    upi_providers = ["okhdfcbank", "okaxis", "oksbi", "paytm", "ybl", "ibl", "axl"]
    card_networks = ["VISA", "MASTERCARD", "RUPAY", "AMEX"]
    card_weights = [0.45, 0.35, 0.18, 0.02]
    
    tier1_pincodes = ["560001", "110001", "400001", "600001", "500001", "700001", "411001", "380001"]
    tier2_3_pincodes = ["226001", "800001", "302001", "452001", "141001", "248001", "834001", "682001"]
    high_rto_pincodes = ["845401", "851204", "273001", "247001", "824231", "282001"]
    
    all_pincodes = tier1_pincodes * 5 + tier2_3_pincodes * 3 + high_rto_pincodes * 2

    start_time = datetime(2026, 6, 20, 0, 0, 0)
    
    sybil_device_pool = [f"dev_sybil_ring_{i:03d}" for i in range(12)]
    sybil_ip_pool = [f"185.220.101.{i}" for i in range(15)]
    legit_device_pool = [f"dev_usr_{i:06d}" for i in range(40000)]
    
    records = []
    
    for i in range(n_records):
        tx_id = f"pay_rzp_{i+1:08d}"
        time_offset = random.uniform(0, 60 * 24 * 3600)
        tx_timestamp = start_time + timedelta(seconds=time_offset)
        hour = tx_timestamp.hour
        
        rand_scenario = random.random()
        
        if rand_scenario < 0.958:
            # 1. LEGITIMATE TRANSACTION
            fraud_type = "NONE"
            is_fraud = 0
            pm = random.choices(payment_methods, weights=pm_weights)[0]
            
            if pm == "COD":
                amount = round(random.uniform(250, 4500), 2)
                is_cod = 1
                address_quality_score = round(random.uniform(0.65, 1.0), 3)
            else:
                amount = round(float(np.random.lognormal(mean=7.2, sigma=1.1)), 2)
                amount = max(100.0, min(amount, 95000.0))
                is_cod = 0
                address_quality_score = round(random.uniform(0.70, 1.0), 3)
                
            user_account_age_days = random.randint(15, 1200)
            tx_velocity_1h = np.random.poisson(0.4) + 1
            tx_velocity_24h = tx_velocity_1h + np.random.poisson(1.2)
            ip_is_vpn_or_datacenter = 1 if random.random() < 0.02 else 0 # 2% benign VPN usage
            card_country = "IN" if random.random() < 0.97 else "US"
            device_id = random.choice(legit_device_pool)
            otp_attempts = 1 if random.random() < 0.93 else 2
            checkout_duration_sec = round(random.uniform(15.0, 180.0), 1)
            pincode = random.choice(all_pincodes)
            
        elif rand_scenario < 0.974:
            # 2. SYBIL BIN TESTING ATTACK (High velocity, low amount, burner devices/VPN + 8% stealth noise)
            fraud_type = "SYBIL_BIN_TEST"
            is_fraud = 1
            pm = "CARD"
            is_cod = 0
            amount = round(random.uniform(1.0, 150.0), 2)
            
            # Stealth noise: 10% of attackers use residential proxy with normal-looking velocity
            is_stealth = random.random() < 0.10
            if is_stealth:
                user_account_age_days = random.randint(10, 40)
                tx_velocity_1h = random.randint(2, 5)
                tx_velocity_24h = random.randint(5, 12)
                ip_is_vpn_or_datacenter = 0
                checkout_duration_sec = round(random.uniform(12.0, 30.0), 1)
            else:
                user_account_age_days = random.randint(0, 3)
                tx_velocity_1h = random.randint(12, 65)
                tx_velocity_24h = tx_velocity_1h + random.randint(20, 180)
                ip_is_vpn_or_datacenter = 1
                checkout_duration_sec = round(random.uniform(1.2, 8.0), 1)
                
            card_country = random.choice(["US", "RU", "NG", "GB", "IN"])
            device_id = random.choice(sybil_device_pool)
            otp_attempts = random.choice([1, 3, 4])
            address_quality_score = round(random.uniform(0.1, 0.45), 3)
            pincode = random.choice(tier1_pincodes)
            
        elif rand_scenario < 0.988:
            # 3. MUTATED ADDRESS COD RTO RING
            fraud_type = "MUTATED_ADDRESS_RTO"
            is_fraud = 1
            pm = "COD"
            is_cod = 1
            amount = round(random.uniform(2800, 14500), 2)
            user_account_age_days = random.randint(0, 5)
            tx_velocity_1h = random.randint(3, 18)
            tx_velocity_24h = tx_velocity_1h + random.randint(5, 30)
            ip_is_vpn_or_datacenter = 1 if random.random() < 0.35 else 0
            card_country = "IN"
            device_id = random.choice(sybil_device_pool)
            otp_attempts = 1
            checkout_duration_sec = round(random.uniform(4.0, 22.0), 1)
            address_quality_score = round(random.uniform(0.05, 0.38), 3)
            pincode = random.choice(high_rto_pincodes)
            
        else:
            # 4. FRIENDLY CHARGEBACK / FIRST-PARTY FRAUD (High value, legitimate-looking attributes)
            fraud_type = "FRIENDLY_CHARGEBACK"
            is_fraud = 1
            pm = random.choice(["CARD", "UPI"])
            is_cod = 0
            amount = round(random.uniform(12000, 85000), 2)
            user_account_age_days = random.randint(50, 400)
            tx_velocity_1h = random.randint(1, 3)
            tx_velocity_24h = random.randint(1, 6)
            ip_is_vpn_or_datacenter = 0
            card_country = "IN"
            device_id = random.choice(legit_device_pool)
            otp_attempts = 1
            checkout_duration_sec = round(random.uniform(25.0, 120.0), 1)
            address_quality_score = round(random.uniform(0.70, 0.95), 3)
            pincode = random.choice(tier1_pincodes)

        if pm == "UPI":
            upi_handle = random.choice(upi_providers)
            card_network = "NA"
            card_bin = "NA"
        elif pm == "CARD":
            upi_handle = "NA"
            card_network = random.choices(card_networks, weights=card_weights)[0]
            card_bin = str(random.randint(400000, 559999))
        else:
            upi_handle = "NA"
            card_network = "NA"
            card_bin = "NA"

        records.append({
            "transaction_id": tx_id,
            "timestamp": tx_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": hour,
            "amount": amount,
            "payment_method": pm,
            "is_cod": is_cod,
            "upi_handle": upi_handle,
            "card_network": card_network,
            "card_bin": card_bin,
            "card_country": card_country,
            "device_id": device_id,
            "ip_is_vpn": ip_is_vpn_or_datacenter,
            "user_account_age_days": user_account_age_days,
            "tx_velocity_1h": tx_velocity_1h,
            "tx_velocity_24h": tx_velocity_24h,
            "address_pincode": pincode,
            "address_quality_score": address_quality_score,
            "otp_attempts": otp_attempts,
            "checkout_duration_sec": checkout_duration_sec,
            "is_fraud": is_fraud,
            "fraud_type": fraud_type
        })
        
    df = pd.DataFrame(records)
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    df.to_csv(output_csv, index=False)
    
    fraud_counts = df["fraud_type"].value_counts().to_dict()
    print(f"[✓] Generated dataset saved to {output_csv}")
    print(f"    Total: {len(df)} | Fraud Distribution: {fraud_counts}")
    return df

if __name__ == "__main__":
    generate_indian_transactions()
