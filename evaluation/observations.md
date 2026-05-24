# Model Evaluation Summary

- Accuracy: 96%
- Fraud Recall: 87%
- Fraud Precision: 54%
- False Positives: 170
- False Negatives: 31

# Observations

## What Worked Well

- The model detects most fraudulent transactions successfully.
- High recall helps reduce missed fraud cases.
- Behavioral features improved fraud detection performance.

## Current Limitations

- Some legitimate transactions are incorrectly flagged as fraud.
- The model can react strongly to unusual spending behavior.
- Evaluation was performed on synthetic transaction data.

# Notes

- Consistent feature generation is important during training and evaluation.
- Rolling transaction history features had a noticeable impact on results.
- Error handling improved stability during streaming.

