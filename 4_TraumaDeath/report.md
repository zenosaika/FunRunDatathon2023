# Lab Report :dna:
### Description
> การประเมินความเสี่ยงการตายของผู้ป่วย Trauma
> + ผู้ป่วย Trauma หรือผู้ป่วยอุบติเหตุ มีโอกาสเสียชีวิตได้ตลอดเวลา แต่การพยากรณ์โอกาสการเสียชีวิตในปัจจุบันนั้นอาศัยประสบการณ์ของแพทย์เฉพาะทางผู้เชี่ยวชาญเป็นหลัก 
> + การพยากรณ์อาจจะแม่นยำมากขึ้นได้หากมีการพยากรณ์โดยอาศัยข้อมูลการเฝ้าระวังผู้ป่วย โดยกำหนดข้อมูลประกอบด้วย
> 1. ข้อมูลผู้ป่วย trauma ที่ได้รับการลงทะเบียน
> 2. ข้อมูลการ Admit
> 3. ข้อมูลส่วนตัวผู้ป่วย
> 4. ข้อมูลสัญญาณชีพ
> 5. ข้อมูลผลตรวจเลือด (lab)
> 6. ข้อมูลการตาย
> 7. ข้อมูลการให้เลือด
> 8. ข้อมูล Blood gas
### Ideas
`Problem : จงประเมินความเสี่ยงการเสียชีวิต`
+ ทำ survival analysis โดยใช้ random survival forest
    + สามารถบอก โอกาสการเสียชีวิต ณ เวลา t ใด ๆ ได้ (t >= 0)
+ ประเมินวันเวลาที่ผู้ป่วยมีโอกาสเสียชีวิต (regression problem)
    + ช่วยระบุวันเวลาที่ต้องทำการเฝ้าระวังเป็นพิเศษได้
### Relative Factors
+ Glasgow Coma Scale (GCS) is used to describe the level of consciousness
    + E - Eye Opening Response (Max 4)
    + V - Verbal Response (Max 5)
    + M - Motor Response (Max 6)
+ Abbreviated Injury Scale (AIS) is an anatomical-based coding system<br>
    The score written as 12(34)(56).7
    + 1 - Body region
    + 2 - Type of anatomical structure
    + 3, 4 - Specific anatomical structure
    + 5, 6 - Level
    + 7 - Severity of score
+ Injury Severity Score (ISS) is used to define the term major trauma
    + 1 <= ISS <= 75
    + ISS = sum of 3 highest AIS<sup>2</sup>
    + ISS = 75 when AIS = 5 for each category
    + If any of AIS = 6, ISS is automatically set at 75
    + Major truama (or polytrauma) when ISS > 15
+ Respiratory Rate
