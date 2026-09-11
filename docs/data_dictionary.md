# Data Dictionary

This document describes the main source and engineered features used in the SaaS Customer Health & Churn Prediction System.

The final modelling dataset contains one row per customer account and combines information from account, subscription, product usage and customer support data.

## Account Features

| Feature | Description | Calculation / Source |
|---|---|---|
| account_id | Unique identifier for each customer account | Source: accounts table |
| industry | Industry associated with the customer | Source: accounts table |
| country | Customer country | Source: accounts table |
| referral_source | Channel through which the customer was acquired | Source: accounts table |
| initial_plan_tier | Plan tier recorded for the account initially | Source: accounts table |
| customer_tenure_days | Number of days the customer has been associated with the product | Snapshot date minus signup date |
| churn_flag | Target variable indicating whether the customer is classified as churned | Source: accounts table |

## Subscription Features

| Feature | Description | Calculation / Source |
|---|---|---|
| subscription_count | Number of subscription records associated with the customer | Count of subscription_id per account |
| ever_upgraded | Indicates whether the customer has ever recorded an upgrade | 1 if any upgrade_flag is true, otherwise 0 |
| ever_downgraded | Indicates whether the customer has ever recorded a downgrade | 1 if any downgrade_flag is true, otherwise 0 |
| latest_plan_tier | Most recent subscription plan | Latest subscription ordered by start_date |
| latest_seats | Number of seats on the most recent subscription | Latest subscription seats |
| latest_mrr | Monthly recurring revenue from the most recent subscription | Latest subscription mrr_amount |
| latest_is_trial | Indicates whether the most recent subscription is a trial | Latest subscription is_trial |
| latest_billing_frequency | Billing frequency of the most recent subscription | Latest subscription billing_frequency |
| latest_auto_renew | Indicates whether auto-renew is enabled on the latest subscription | Latest subscription auto_renew_flag |
| seat_change | Change in seat count between initial and latest customer state | latest_seats - initial_seats |
| plan_changed | Indicates whether the current plan differs from the initial plan | 1 if latest_plan_tier differs from initial_plan_tier, otherwise 0 |

## Product Usage Features

| Feature | Description | Calculation / Source |
|---|---|---|
| usage_event_count | Number of recorded product usage events | Count of usage records associated with the customer |
| total_usage_count | Total number of recorded feature uses | Sum of usage_count |
| unique_features_used | Number of unique product features used | Count of distinct feature_name |
| active_usage_days | Number of unique days with recorded usage | Count of distinct usage_date |
| beta_usage_events | Number of usage events involving beta features | Count where is_beta_feature is true |
| errors_per_100_usage | Usage error rate normalised by activity | (total_errors / total_usage_count) × 100 |
| average_duration_per_event | Average duration of a usage event | total_usage_duration_secs / usage_event_count |
| average_usage_per_event | Average usage count per event | total_usage_count / usage_event_count |
| days_since_last_usage | Number of days since the customer's latest usage activity | Snapshot date - last_usage_date |

## Support Features

| Feature | Description | Calculation / Source |
|---|---|---|
| ticket_count | Number of support tickets associated with the customer | Count of ticket_id |
| has_support_tickets | Indicates whether the customer has any support history | 1 if ticket_count > 0, otherwise 0 |
| average_first_response_minutes | Average first response time across support tickets | Mean first_response_time_minutes |
| average_resolution_hours | Average support ticket resolution time | Mean resolution_time_hours |
| average_satisfaction_score | Average available customer satisfaction score | Mean satisfaction_score |
| has_satisfaction_score | Indicates whether satisfaction data is available | 1 if a satisfaction score exists, otherwise 0 |
| escalation_count | Number of escalated support tickets | Sum of escalation_flag |
| days_since_last_support_ticket | Number of days since the customer's latest support ticket | Snapshot date - last_support_ticket_date |

## Model Output Features

| Feature | Description |
|---|---|
| churn_probability | Model-generated churn risk score between 0 and 1 |
| churn_probability_percent | Churn probability expressed as a percentage |
| health_score | Prototype customer health score calculated as 100 minus churn probability percentage |
| risk_level | Operational risk category: Low, Medium or High |
| action_priority | Customer Success priority derived from risk level |
| top_risk_signals | Features contributing most strongly toward the customer's churn prediction |
| recommended_action | Suggested Customer Success action based on the customer's risk category |