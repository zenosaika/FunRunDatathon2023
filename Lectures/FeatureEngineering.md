# Feature Engineering

- Imputation - handle missing values.
    - Numerical Imputation 
        - `data['column_name'].fillna(0)`
    - Categorical Imputation
        - `data['column_name'].fillna(data['column_name'].value_counts().idx_max(), inplace=True)`
- Handling Outliers
    - Removal ลบทิ้งไปเลย ถ้ามันไม่หายไปหลาย sample เกิน
    - Replacing Value เปลี่ยนค่าเป็นค่า default เลย (ทำเหมือน imputation)
    - Capping สุ่มค่าจาก sample อื่นมาใส่แทน
    - Discretization ไม่เข้าใจ
    - ปัญหาของ outlier คือแบบสมมุติทำ linear regression เจ้า outlier มันมีแรงดึงมากกว่าชาวบ้านเขา จะทำให้กราฟมันเอียงไปหา outlier
- Log Transform - handle skew data.
    - data['column_name] = np.log(data['column_name'])
    - ช่วยให้ data มัน distribute แบบ normal หรือไม่ก็ skew น้อยลง
    - Central Tendencies ค่ากลาง eg. mean, median, mode
    - Ideal ของ data คือมัน Normal Distribution (mean = median = mode)
    - Left Skew ขวาสูงกว่า (mode > median > mean)
    - Right Skew ซ้ายสูงกว่า (mode < median < mean)
    - พอ take log ลงไปแล้ว ระยะห่างของ outlier กับข้อมูลปกติจะลดลง ทำให้ outlier ส่งผลต่อข้อมูลทั้งหมดน้อยลง eg. ข้อมูลปกติอยู่ที่ 1 ส่วน outlier อยู่ที่ 10000 ห่างกัน 9999 แต่ log10(1) = 0 ห่างกับ log10(10000) = 1000 แค่ 999
    - Log Tranform ใช้ง่ายสุด แต่ยังมี Square Root กับ Box-Cox Transform อยู่อีกนะ
- One Hot Encoding
    - สมมุติ column "color" มี 3 class คือ 1=เขียว 2=เหลือง 3=แดง มันไม่ได้หมายความว่า ระยะห่างของเขียวกับเหลือง น้อยกว่า ระยะห่างของเขียวกับแดง ดังนั้นเลยใช้ one hot เพื่อให้ model เรียนรู้ข้อมูลของเราได้ง่ายขึ้น
- Scaling
    - Distance-based algorithm ควรทำ feature scaling
    - Normalization 
    - Standardization

## Link to Source

- [Feature Engineering](https://towardsdatascience.com/what-is-feature-engineering-importance-tools-and-techniques-for-machine-learning-2080b0269f10)
- [Outlier and Skew Data](https://arnondora.in.th/handling-skew-data-with-log-transform/)

