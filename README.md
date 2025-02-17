# **T-Series Data Engineering Analytics** ▶️🎵📊  

## 📖 **Overview**  
![Report Home Page](https://github.com/KirandeepMarala/T-Series-Data-Engineering-Analytics/blob/main/Images/dashboard_home_page.png) 
This project is an **end-to-end data engineering solution** for analyzing YouTube channels under the **T-Series Universe**. It automates data extraction, processing, warehousing, and visualization, providing deep insights into **views, likes, comments, content duration, and top-performing videos**.  

The final output is an interactive **Power BI report**, enabling users to analyze YouTube content trends over different time periods.  

---

## 📁 **Data Source**  
- **Data Source:** YouTube API  
- **Channels Covered:**  
  - 📺 T-Series Hindi  
  - 📺 T-Series Telugu  
  - 📺 T-Series Tamil  
  - 📺 T-Series Kannada  
  - 📺 T-Series Malayalam  
  - 📺 T-Series Bhakti Sagar  
- **Time Period:** Data is collected daily from **January 2022** to the present.  

---

## 🛠️ **Tech Stack & Tools Used**  

| **Category**       | **Tools Used**  |
|-------------------|---------------|
| **Data Extraction** | YouTube API, AWS Lambda  |
| **Data Scheduling** | AWS EventBridge (CloudWatch)  |
| **Data Storage** | AWS S3 (CSV Files)  |
| **Data Warehousing** | Snowflake  |
| **Data Visualization** | Power BI  |
| **Programming Language** | Python  |

---

## 📊 **Project Architecture & Pipeline**  
![Architecture of the data pipeline](https://github.com/KirandeepMarala/T-Series-Data-Engineering-Analytics/blob/main/Images/youtube_analytics_architecture_pipeline.jpg) 

This project follows a **fully automated data pipeline** that runs daily at **6:30 AM & 6:30 PM IST**.  

### **Data Flow Steps:**  

1. **Data Fetching**:  
   - YouTube API fetches **daily stats** on views, likes, comments, and published videos for 6 T-Series channels.
2. **AWS Lambda Execution**:
   - A Python script runs in **AWS Lambda**, processes, and cleans the data.
3. **AWS EventBridge Trigger**:  
   - The Lambda function is triggered **daily at 6:30 AM & 6:30 PM IST** using **AWS EventBridge (CloudWatch)**.  
4. **Data Storage in AWS S3**:  
   - The processed data is stored as **CSV files** in an Amazon S3 bucket.  
5. **Data Ingestion into Snowflake**:  
   - The **Object Put event** in S3 triggers **Snowflake**, which automatically ingests the new data into a structured table.  
6. **Power BI Visualization**:  
   - The Power BI dashboard updates **twice daily at 7:00 AM & 7:00 PM IST**, fetching fresh data from Snowflake.  

---

## ⚙️ **Key Features in Power BI Report** 📊 
![Report overall stats](https://github.com/KirandeepMarala/T-Series-Data-Engineering-Analytics/blob/main/Images/dashboard_stats_page.png) 
![Report overall info](https://github.com/KirandeepMarala/T-Series-Data-Engineering-Analytics/blob/main/Images/dashboard_overall_info.png) 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Overall Channel Performance – Total Views, Likes, Comments, and Published Videos.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Shorts vs. Full-Length Videos – Comparative performance analysis.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Top 7 Trending Videos – Based on selected time periods.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Time-Based Filtering – View data for **L7D, L30D, L60D, L3M, L6M, L12M, L24M, or All Time**.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Channel Selection – Analyze data for **6 T-Series channels** individually or collectively.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✔️ Engagement Metrics – Detailed insights into **views, likes, comments, and content duration (minutes)**.  

  🔗 **Live Interactive Report:** [Click Here to View Power BI Report](https://app.powerbi.com/view?r=eyJrIjoiYTJhYjQyNTAtMDNmYi00ZTQwLWExYjItZWY0MTVjYmY5N2ViIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)  


---

## 🚀 **Key Functionalities**  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **Automated Data Pipeline** (Runs twice daily at **6:30 AM & 6:30 PM IST**).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **YouTube API Integration** for real-time analytics.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **AWS Lambda & EventBridge** for serverless processing.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **AWS S3 & Snowflake** for scalable data storage.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **Time-based Trend Analysis** (Daily, Weekly, Monthly stats).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **Power BI Dynamic Filtering** (By channel, content type, and date range).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;✅ **Scalability** – Can be extended to include more YouTube channels.  

---


## 📜 How to Run This Project

1. **Clone the Repository:**
```bash
git clone https://github.com/KirandeepMarala/T-Series-Data-Engineering-Analytics
 ```
2. **Set Up AWS Lambda & S3:**:
   - Deploy the Lambda function to AWS.
   - Configure AWS EventBridge for scheduling at 6:30 AM & PM IST.
   - Ensure S3 bucket permissions allow Snowflake to read data.
    
3. **Set Up Snowflake Data Warehouse:**
   - Create a table to store YouTube analytics data.
   - Configure auto-ingestion from AWS S3.
    
4. **Connect Power BI to Snowflake:**:
   - Use Power BI Desktop → Get Data → Snowflake Connector.
   - Load data & create visualizations.
    
---

## 🎯 Conclusion
This project showcases a scalable & automated data engineering pipeline for YouTube analytics. With AWS, Snowflake, and Power BI, we built a robust & efficient system to track YouTube performance metrics across multiple T-Series channels.

Feel free to reach out for any questions or suggestions! 😊

---

## 📬 Contact

- **Author**: [kirandeep Marala](#)
- **Email**: [kirandeep.marala@gmail.com](mailto:kirandeep.marala@gmail.com)
- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/kirandeepmarala/)

---
