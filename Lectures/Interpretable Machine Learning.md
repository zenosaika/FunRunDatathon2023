Interpretability of modelling
![figure_2_fix](https://user-images.githubusercontent.com/128203147/227242463-b711faea-e3e4-45ec-90f7-4c59958d0009.png)


ธรรมชาติของโมเดล
Intrinsically explainable - An intrinsically explainable model is designed to be simple and transparent enough that we can get a sense for how it works by looking at its structure, e.g. simple regression models and small decision trees. These models are directly interpretable.
สรุปคือ โดยธรรมชาติโมเดลมันอธิบายได้ด้วยตัวมันเองอยู่แล้ว

Post-hoc explainable - For more complicated, already trained models, we can use explainability tools (often called interpretability tools) to obtain post-hoc explanations. Explanations of sufficiently complex models such as deep neural networks are always post-hoc explanations as they are not directly interpretable.
สรุปคือ โดยธรรมชาติตัวโมเดลเองมันอธิบายไม่ได้ / ซับซ้อนไป


รูปแบบของการอธิบายโมเดล

Global explanations - A global explanation of a ML model details what features are important to the model overall. This can be measured by looking at effect sizes or determining which features have the biggest impact on model accuracy. Global explanations are helpful for guiding policy or finding evidence for, or rejecting a hypothesis that a particular feature is important. Figure (4) shows a visualisation of a global explanation for a wine classification task
สรุปคือ การอธิบายโมเดลในภาพรวมว่าเวลาจะ predict ในทุกครั้งๆ มันดูอะไรบ้าง
![figure_4_fix](https://user-images.githubusercontent.com/128203147/227242618-57a4caa3-f34c-4cdf-aab9-aed094488f14.png)



Local explanations - A local explanation details how a ML model arrived at a specific prediction. For tabular data, it could be a list of features with their impact on the prediction. For a computer vision task, it might be a subset of pixels that had the biggest impact on the classification.
      - Why did the model return this output for this input?
      - What if this feature had a different value?
สรุปคือ การอธิบายโดเดลสำหรับค่า output ค่าๆหนึ่่ง ว่ามันได้ output = 6 นี้มันดูจากอะไร เช่นดูจาก x1 มีน้ำหนักมาก แต่ ถ้า output = 7 มันก็อาจจะอธิบายได้อีกแบบ เช่น x2 มีน้ำหนักมากกว่า x1 ในการ prediction = 7
![figure_5_fix](https://user-images.githubusercontent.com/128203147/227242746-bd2a4ec4-0ecd-49f4-b9af-07d93d66a425.png)




รูปแบบของการทำงานของ tool ที่ใช้อธิบายโมเดด


Model-specific - Model-specific methods work by inspecting or having access to the model internals. Interpreting regression coefficient weights or P-values in a linear model or counting the number of times a feature is used in an ensemble tree model are examples of model-specific methods.
สรุปคือ มันดูไปที่ตัวโครงสร้าง model เลยว่าทำไมถึงได้ output


Model-agnostic - Model-agnostic methods work by investigating the relationship between input-output pairs of trained models. They do not depend on the internal structure of the model. These methods are very useful for when we have no theory or other mechanism to interpret what is happening inside the model.
      - example-based. These are model-agnostic and use the difference or similarity between examples in the data to provide an understanding of how the model behaves.             Example-based explanations can provide intuitive explanations for predictions when the features in the data are simple or human-interpretable.
สรุปคือ อันนี้ดูจากความสัมพันธ์ input - output ว่าทำไมมันถึง predict แบบนี้


The tools for explaining machine learning models
![Screenshot_66](https://user-images.githubusercontent.com/128203147/227242921-6b156aa4-d570-45aa-ada0-9e9c6172977b.png)


Source
https://www.ambiata.com/blog/2021-04-12-xai-part-1/
