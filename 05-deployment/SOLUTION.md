# واجب 5 — نشر نماذج التعلم الآلي

حل عملي لواجب **ML Zoomcamp 2026 — Deploying Machine Learning Models** باستخدام ملفات الدفعة الرسمية والنموذج المجمد دون إعادة تدريبه أو تعديل ملف القفل.

## الإجابات

| السؤال | الإجابة |
|---|---|
| 1 — نسخة uv المحلية | `0.12.13` |
| 2 — نسخة Scikit-Learn المقفلة | `1.7.2` |
| 3 — احتمال التحويل من النموذج | `0.533` |
| 4 — احتمال التحويل عبر API | `0.770` |
| 5 — صورة Python الأساسية | `python:3.11.15-slim-bookworm` |
| 6 — احتمال التحويل من الحاوية | `0.770` |

القيمة غير المدوّرة للسؤال الثالث هي `0.5329944186432507`. وأعادت واجهة API والحاوية القيمة نفسها تمامًا: `0.769799` مع `conversion: true`.

نسخة `uv` المحلية تختلف عن النسخة المثبتة داخل Docker، وهي `0.10.11`. السؤال الأول يطلب النسخة المحلية؛ وتصف التعليمات الرسمية هذا السؤال بأنه فحص إعداد.

## ما تم التحقق منه

- تشغيل البيئة المقفلة باستخدام Python `3.11.15` و`uv sync --locked`.
- نجاح اختبار `smoke_test.py` المرجعي.
- تحميل النموذج عبر `pickle` بعد مطابقة بصمة SHA-256 الرسمية.
- تشغيل واجهة FastAPI محليًا واختبار `/health` و`/predict`.
- بناء Dockerfile الرسمي وتشغيل حاوية فعلية، ثم نجاح `q6_test.py`.
- تطابق التنبؤ وبصمتي النموذج وقيم التعويض بين API المحلي والحاوية.
- عدم تعديل `Dockerfile` أو `uv.lock` أو النموذج الرسمي.

بصمة النموذج:

```text
1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1
```

## إعادة التشغيل

من داخل مجلد المشروع، مع تثبيت `uv` وDocker:

```bash
uv sync --locked
uv run python smoke_test.py
uv run python q3.py
```

في نافذة طرفية أولى، شغّل API المحلي على منفذ منفصل حتى يمكن مقارنته بالحاوية:

```bash
uv run uvicorn predict:app --host 127.0.0.1 --port 9697
```

وفي نافذة ثانية:

```bash
uv run python verify_api.py --runtime local_api --base-url http://127.0.0.1:9697
```

لبناء الحاوية وتشغيلها:

```bash
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

ثم من نافذة أخرى:

```bash
uv run python verify_api.py --runtime docker --base-url http://127.0.0.1:9696
uv run python q6_test.py
```

تكتب السكربتات نتائجها في `q3_result.json` و`local_api_result.json` و`docker_result.json`. يحتوي `answers.json` على ملخص الإجابات والتحقق. استُخدم `--network=host` عند بناء الحاوية وتشغيلها في بيئة التنفيذ المعزولة؛ لم يتغير Dockerfile.

## حالة التسليم

الحل والاختبارات مكتملان محليًا. لم يُنشر هذا الحل ولم يُحفظ نموذج واجب 5 بعد؛ يشترط النموذج رابطًا عامًا للكود. صفحة الدورة كانت ما تزال تقبل التسليم رغم انتهاء الموعد الأصلي.

## المصادر

- [تعليمات واجب 5 الرسمية](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/main/cohorts/2026/homework/05-deployment/homework.md)
- [ملفات الإصدار الرسمي](https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/main/cohorts/2026/homework/05-deployment)
- [صفحة تسليم الواجب](https://courses.datatalks.club/ml-zoomcamp-2026/homework/hw05)
