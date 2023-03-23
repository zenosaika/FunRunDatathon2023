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
`Problem : ให้ predict ว่าผู้ป่วยตอน discharge ออกจาก รพ. มี class แบบใด (multiclass) โดยใช้แค่ผลการวินิจฉัยผู้ป่วยตอนมาถึง รพ. เท่านั้น (เพราะต้องการทราบ outcome ของผู้ป่วยตั้งแต่เนิ่น ๆ เลย)`
1. Preprocessing
    - Feature Engineering
        - data encoding (เช่น onehot)
        - data creation (แบบ paper ที่เราอ่านกัน)
        - scaling, normalization, standardization 
        - etc.
    - shuffle then split data
2. เพราะ target คือ predict ว่าตอน discharge ออกจาก รพ. ผู้ป่วยจะมี outcome แบบไหน โดยใช้ข้อมูลจากการวินิจฉัยแค่ที่มีตอนเข้ารักษาวันแรกเท่านั้น ไม่ได้ใช้ข้อมูลทั้งหมด ดังนั้น
- เราจะเทรน regression model มา predict จำนวนวันที่ผู้ป่วยจะอยู่ รพ. จน discharge (ใช้แค่ data ที่ตรวจตอนมาถึง รพ. ครั้งแรกมาเทรน)
- เทรน classification model โดยใช้ data แค่ที่ตรวจตอนมาถึง รพ. ครั้งแรก บวกกับ จำนวนวันที่อยู่ รพ. จน discharge ซึ่งจะ predict เป็น class ออกมา (multiclass) 
- ทำ survival analysis ได้กราฟ โอกาสที่จะอยู่รอด ณ เวลา t ใด ๆ ของคน ๆ นั้นมา
- นำทั้งหมดมาใช้ คือใช้กราฟ survival มาเป็นพื้นหลัง แล้ว plot จุดไปที่วันที่ discharge ที่ regressor เรา predict ได้ กับวันที่ discharge จริงจากฐานข้อมูล พร้อมกับระบุว่าออกไปด้วย class (outcome) แบบใด

<br>![Final Graph](images/final_graph.png)<br>

- คราวนี้เราก็เอามาสรุปได้ว่า จากกราฟ survival ที่แสดงถึงโอกาสการรอดชีวิต ณ เวลา t ใด ๆ นับตั้งแต่เข้ารักษา regression model ของเรา predict ได้ว่า ผู้ป่วยจะ discharge ออกจาก รพ. วันที่ 7 ซึ่งมีโอกาสรอดชีวิต 50% ด้วย outcome ที่ predict จาก classification model ว่าเป็นแบบ recovery
- ซึ่งเทียบกับผลลัพธ์จริงจากฐานข้อมูล ที่ผู้ป่วย discharge ออกจาก รพ. หลังผ่านไป 6 วัน ที่โอกาสรอดชีวิตเท่ากับ 60% ด้วย outcome แบบ recovery
- สรุปได้ว่าโมเดลของเรามีความแม่นยำ ... % จากการใช้แค่ข้อมูลจากการวินิจฉัยตอนผู้ป่วยมาถึง รพ.
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
