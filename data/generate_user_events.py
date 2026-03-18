#!/usr/bin/env python3
"""
Generate synthetic user event data for cohort retention analysis.
Simulates realistic SaaS retention patterns with configurable decay curves.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
N_USERS = 3000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 9, 30)

# Retention decay parameters (realistic SaaS benchmarks)
# Day 1: ~60%, Day 7: ~35%, Day 30: ~20%
RETENTION_BASE_RATES = {
    'day_1': 0.60,
    'day_7': 0.35,
    'day_30': 0.20,
    'day_90': 0.12,
}

# Acquisition channel retention multipliers
CHANNEL_MULTIPLIERS = {
    'organic': 1.25,      # Best retention
    'referral': 1.15,     # Good retention, highest LTV
    'paid_social': 0.75,  # Lower retention
}

# Plan type retention multipliers
PLAN_MULTIPLIERS = {
    'free': 0.85,
    'starter': 1.0,
    'pro': 1.35,          # Pro users rarely churn
}

# Product improvement effect: cohorts from Jan 2024 onward have better retention
IMPROVEMENT_START = datetime(2024, 1, 1)
IMPROVEMENT_BOOST = 0.12  # 12% improvement

# Revenue parameters
REVENUE_BY_PLAN = {
    'free': (0, 0),
    'starter': (29, 49),
    'pro': (99, 199),
}

def generate_retention_curve(registration_date, channel, plan_type, completed_onboarding):
    """
    Generate a retention curve for a user based on their attributes.
    Returns a list of days when the user was active.
    """
    # Base retention probabilities
    base_day_1 = RETENTION_BASE_RATES['day_1']
    base_day_7 = RETENTION_BASE_RATES['day_7']
    base_day_30 = RETENTION_BASE_RATES['day_30']
    base_day_90 = RETENTION_BASE_RATES['day_90']
    
    # Apply channel multiplier
    channel_mult = CHANNEL_MULTIPLIERS[channel]
    
    # Apply plan multiplier
    plan_mult = PLAN_MULTIPLIERS[plan_type]
    
    # Apply onboarding effect (strong predictor)
    onboarding_mult = 1.4 if completed_onboarding else 0.75
    
    # Apply product improvement boost for later cohorts
    improvement_mult = 1.0
    if registration_date >= IMPROVEMENT_START:
        improvement_mult = 1 + IMPROVEMENT_BOOST
    
    # Calculate adjusted retention rates
    day_1_prob = min(base_day_1 * channel_mult * plan_mult * onboarding_mult * improvement_mult, 0.95)
    day_7_prob = min(base_day_7 * channel_mult * plan_mult * onboarding_mult * improvement_mult, 0.85)
    day_30_prob = min(base_day_30 * channel_mult * plan_mult * onboarding_mult * improvement_mult, 0.70)
    day_90_prob = min(base_day_90 * channel_mult * plan_mult * onboarding_mult * improvement_mult, 0.50)
    
    # Generate active days using exponential decay with some noise
    active_days = [0]  # Day 0 = signup (always active)
    
    # Day 1 activity
    if np.random.random() < day_1_prob:
        active_days.append(1)
    
    # Day 2-7 activity (interpolated)
    for day in range(2, 8):
        prob = day_7_prob + (day_1_prob - day_7_prob) * (7 - day) / 5
        prob *= np.random.uniform(0.85, 1.15)  # Add noise
        if np.random.random() < prob:
            active_days.append(day)
    
    # Day 8-30 activity
    for day in range(8, 31):
        prob = day_30_prob + (day_7_prob - day_30_prob) * (30 - day) / 22
        prob *= np.random.uniform(0.85, 1.15)
        if np.random.random() < prob:
            active_days.append(day)
    
    # Day 31-90 activity
    max_days = (END_DATE - registration_date).days
    for day in range(31, min(91, max_days + 1)):
        prob = day_90_prob + (day_30_prob - day_90_prob) * (90 - day) / 59
        prob *= np.random.uniform(0.85, 1.15)
        if np.random.random() < prob:
            active_days.append(day)
    
    # Day 91+ activity (long-term retention)
    for day in range(91, max_days + 1):
        prob = day_90_prob * 0.7  # Gradual continued decay
        prob *= np.random.uniform(0.80, 1.20)
        if np.random.random() < prob:
            active_days.append(day)
    
    return sorted(active_days)

def generate_user_events():
    """Generate the complete user events dataset."""
    events = []
    
    # Generate user base
    for user_idx in range(N_USERS):
        user_id = f"user_{user_idx:05d}"
        
        # Registration date (weighted toward more recent dates)
        days_range = (END_DATE - START_DATE).days
        # Use beta distribution to skew toward more recent signups
        registration_offset = int(np.random.beta(2, 1) * days_range)
        registration_date = START_DATE + timedelta(days=registration_offset)
        
        # Acquisition channel (referral is rarest but best)
        channel = np.random.choice(
            ['organic', 'paid_social', 'referral'],
            p=[0.45, 0.40, 0.15]
        )
        
        # Plan type (most users start free)
        plan_type = np.random.choice(
            ['free', 'starter', 'pro'],
            p=[0.65, 0.25, 0.10]
        )
        
        # Onboarding completion (60% complete it, varies by channel)
        base_onboarding_rate = 0.60
        if channel == 'referral':
            base_onboarding_rate = 0.70  # Referral users more engaged
        elif channel == 'paid_social':
            base_onboarding_rate = 0.50  # Paid users less engaged
        
        completed_onboarding = np.random.random() < base_onboarding_rate
        
        # Generate retention curve (active days)
        active_days = generate_retention_curve(
            registration_date, channel, plan_type, completed_onboarding
        )
        
        # Determine if user makes purchases
        first_purchase_day = None
        upgrade_day = None
        churn_day = None
        
        # First purchase logic (10% of free users, 80% of starter/pro)
        if plan_type in ['starter', 'pro'] or np.random.random() < 0.10:
            # Purchase happens within first 30 days if at all
            purchase_candidates = [d for d in active_days if 0 < d <= 30]
            if purchase_candidates and np.random.random() < 0.40:
                first_purchase_day = np.random.choice(purchase_candidates)
        
        # Upgrade logic (20% of paying users upgrade)
        if plan_type == 'starter' and first_purchase_day:
            upgrade_candidates = [d for d in active_days if d > first_purchase_day]
            if upgrade_candidates and np.random.random() < 0.20:
                upgrade_day = np.random.choice(upgrade_candidates[:10])  # Within 10 days of purchase
        
        # Churn logic (users stop being active)
        if len(active_days) > 1:
            last_active = active_days[-1]
            # If user hasn't been active for 30+ days, mark as churned
            days_since_reg = (END_DATE - registration_date).days
            if last_active < days_since_reg - 30:
                churn_day = last_active + np.random.randint(7, 30)
        
        # Build event timeline
        user_events = []
        
        # 1. Signup event
        user_events.append({
            'user_id': user_id,
            'registration_date': registration_date.strftime('%Y-%m-%d'),
            'event_date': registration_date.strftime('%Y-%m-%d'),
            'event_type': 'signup',
            'revenue': 0.0,
            'plan_type': plan_type,
            'acquisition_channel': channel,
        })
        
        # 2. Onboarding completion (if applicable, within first 3 days)
        if completed_onboarding:
            onboarding_day = np.random.choice([d for d in active_days if 0 < d <= 3]) if [d for d in active_days if 0 < d <= 3] else 1
            onboarding_date = registration_date + timedelta(days=int(onboarding_day))
            user_events.append({
                'user_id': user_id,
                'registration_date': registration_date.strftime('%Y-%m-%d'),
                'event_date': onboarding_date.strftime('%Y-%m-%d'),
                'event_type': 'onboarding_complete',
                'revenue': 0.0,
                'plan_type': plan_type,
                'acquisition_channel': channel,
            })
        
        # 3. Return visits (subset of active days)
        for day in active_days[1:]:  # Skip day 0 (signup)
            # Not every active day generates a return_visit event
            if np.random.random() < 0.6:
                event_date = registration_date + timedelta(days=int(day))
                if event_date <= END_DATE:
                    user_events.append({
                        'user_id': user_id,
                        'registration_date': registration_date.strftime('%Y-%m-%d'),
                        'event_date': event_date.strftime('%Y-%m-%d'),
                        'event_type': 'return_visit',
                        'revenue': 0.0,
                        'plan_type': plan_type,
                        'acquisition_channel': channel,
                    })
        
        # 4. First purchase event
        if first_purchase_day:
            purchase_date = registration_date + timedelta(days=int(first_purchase_day))
            if purchase_date <= END_DATE:
                # Determine purchase amount based on plan
                min_rev, max_rev = REVENUE_BY_PLAN[plan_type]
                if min_rev > 0:
                    revenue = round(np.random.uniform(min_rev, max_rev), 2)
                else:
                    revenue = round(np.random.uniform(29, 99), 2)  # Free to paid conversion
                
                user_events.append({
                    'user_id': user_id,
                    'registration_date': registration_date.strftime('%Y-%m-%d'),
                    'event_date': purchase_date.strftime('%Y-%m-%d'),
                    'event_type': 'first_purchase',
                    'revenue': revenue,
                    'plan_type': plan_type,
                    'acquisition_channel': channel,
                })
        
        # 5. Upgrade event
        if upgrade_day:
            upgrade_date = registration_date + timedelta(days=int(upgrade_day))
            if upgrade_date <= END_DATE:
                upgrade_revenue = round(np.random.uniform(50, 150), 2)
                user_events.append({
                    'user_id': user_id,
                    'registration_date': registration_date.strftime('%Y-%m-%d'),
                    'event_date': upgrade_date.strftime('%Y-%m-%d'),
                    'event_type': 'upgrade',
                    'revenue': upgrade_revenue,
                    'plan_type': 'pro',
                    'acquisition_channel': channel,
                })
        
        # 6. Churn event
        if churn_day:
            churn_date = registration_date + timedelta(days=int(churn_day))
            if churn_date <= END_DATE:
                user_events.append({
                    'user_id': user_id,
                    'registration_date': registration_date.strftime('%Y-%m-%d'),
                    'event_date': churn_date.strftime('%Y-%m-%d'),
                    'event_type': 'churn',
                    'revenue': 0.0,
                    'plan_type': plan_type,
                    'acquisition_channel': channel,
                })
        
        events.extend(user_events)
    
    # Create DataFrame
    df = pd.DataFrame(events)
    
    # Sort by user_id and event_date
    df['event_date_dt'] = pd.to_datetime(df['event_date'])
    df = df.sort_values(['user_id', 'event_date_dt']).drop('event_date_dt', axis=1)
    
    return df

def main():
    """Main execution function."""
    print("Generating user events data...")
    print(f"Target users: {N_USERS}")
    print(f"Date range: {START_DATE.date()} to {END_DATE.date()}")
    
    # Generate data
    df = generate_user_events()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(__file__), exist_ok=True)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'user_events.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Generated {len(df):,} events for {df['user_id'].nunique():,} unique users")
    print(f"📁 Saved to: {output_path}")
    
    # Print summary statistics
    print("\n📊 Dataset Summary:")
    print(f"   Total events: {len(df):,}")
    print(f"   Unique users: {df['user_id'].nunique():,}")
    print(f"   Date range: {df['event_date'].min()} to {df['event_date'].max()}")
    print(f"\n   Event type breakdown:")
    for event_type, count in df['event_type'].value_counts().items():
        print(f"      {event_type}: {count:,}")
    
    print(f"\n   Acquisition channel breakdown:")
    users_by_channel = df.drop_duplicates('user_id')['acquisition_channel'].value_counts()
    for channel, count in users_by_channel.items():
        print(f"      {channel}: {count:,} users ({count/len(df['user_id'].unique())*100:.1f}%)")
    
    print(f"\n   Plan type breakdown:")
    users_by_plan = df.drop_duplicates('user_id')['plan_type'].value_counts()
    for plan, count in users_by_plan.items():
        print(f"      {plan}: {count:,} users ({count/len(df['user_id'].unique())*100:.1f}%)")
    
    # Revenue stats
    total_revenue = df['revenue'].sum()
    paying_users = df[df['revenue'] > 0]['user_id'].nunique()
    print(f"\n   Total revenue: ${total_revenue:,.2f}")
    print(f"   Paying users: {paying_users:,}")
    print(f"   ARPU: ${total_revenue / df['user_id'].nunique():.2f}")
    
    # Onboarding completion rate
    users_df = df.drop_duplicates('user_id').copy()
    onboarding_completed = df[df['event_type'] == 'onboarding_complete']['user_id'].nunique()
    print(f"\n   Onboarding completion rate: {onboarding_completed / len(users_df) * 100:.1f}%")

if __name__ == "__main__":
    main()