# Data

Olist 원본 CSV는 저장소에 포함하지 않습니다.

복구된 원본 notebook에서 확인된 입력 파일:

```text
data/
├── olist_customers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_orders_dataset.csv
├── olist_products_dataset.csv
└── olist_sellers_dataset.csv
```

Notebook은 위 파일명을 기준으로 실행되며, `src/preprocessing.py`는 분석에 직접 필요한 주요 테이블을 사용합니다.

데이터는 Olist 공개 데이터셋의 원본 배포 조건을 따릅니다.
