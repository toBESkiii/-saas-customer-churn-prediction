# EDA Findings and Business Interpretation

The exploratory analysis examines whether customer characteristics, subscription behaviour, product usage and support activity differ between retained and churned customers.

The goal is not only to calculate descriptive metrics, but to understand which signals may be useful for customer-risk prioritisation.

## Customer Segments

DevTools customers showed the highest observed churn rate among the analysed industries, while EdTech and Cybersecurity showed lower churn rates.

This suggests that industry may provide useful segmentation information.

However, this should be treated as an association rather than a causal relationship.

### Business interpretation

Customer Success teams could use industry as one segmentation factor when prioritising account reviews, but it should not be used independently to determine risk.

## Acquisition Source

Customers acquired through events showed a higher observed churn rate than customers acquired through organic or partner channels.

### Business interpretation

This suggests that acquisition source may contain useful information about customer expectations, onboarding quality or product fit.

Further analysis could investigate whether different acquisition channels require different onboarding or engagement strategies.

## Subscription Behaviour

Differences were observed across billing frequency, plan tier and subscription history.

However, the relationships were not consistently strong enough to treat subscription characteristics as standalone churn indicators.

### Business interpretation

Subscription information should contribute to a broader customer-risk assessment rather than be used independently.

Changes such as upgrades, downgrades, plan movement or seat changes may still provide useful context for Customer Success teams.

## Product Usage Behaviour

Raw usage activity did not show the expected pattern of lower usage among churned customers.

In several comparisons, churned customers showed similar or slightly higher usage levels than retained customers.

### Business interpretation

Usage volume alone is not a reliable churn indicator in this dataset.

This supports the decision to combine multiple engagement measures such as:

- usage frequency;
- number of active usage days;
- feature breadth;
- error rate;
- recency of usage.

The result also highlights a limitation of the synthetic dataset, where some relationships may not follow typical real-world SaaS behaviour.

## Customer Support Behaviour

Support ticket counts, response times, resolution times and satisfaction scores showed relatively small differences between churned and retained customers.

### Business interpretation

Support behaviour may contribute some predictive information, but it does not appear strong enough to independently identify churn risk.

Support metrics should therefore be combined with subscription, account and usage information.

## Overall Analytical Conclusion

The EDA suggests that no single variable provides a strong explanation of customer churn.

This motivated the use of a multivariate machine learning model that combines customer, subscription, product usage and support signals.

The selected model also showed only modest predictive separation on the holdout data.

For this reason, the final churn probabilities and health scores are treated as decision-support signals for customer prioritisation rather than definitive predictions.

## Actionable Use of the Analysis

The analysis supports a Customer Success workflow where:

1. customers are ranked by predicted churn risk;
2. high-risk customers are prioritised for review;
3. model risk signals provide context for investigation;
4. Customer Success teams combine model outputs with business knowledge before taking retention action.

The system is therefore designed to support prioritisation and investigation rather than automate retention decisions.