Capitol Insider-Trading Analyzer

What is it?

This project is a data-centered Streamlit dashboard that displays US congressional stock trades alongside the SP-500 Index to access the likelihood of insider trading. By scraping from Quiver Quantitative while analyzing financial moves, this tool aims to promote transparency and insight into elected officials' activities.

Features
- User-friendly interactive Streamlit dashboard
- Dropdown to select politician
- Graphs comparing individual stock performance to S&P 500
- SQL-backed database

How is suspicion determined?

- For **purchases**: suspicious if stock significantly **outperforms** S&P afterward
- For **sales**: suspicious if stock significantly **underperforms** S&P afterward
- Thresholds like **±5%** are considered **abnormal returns**
  
