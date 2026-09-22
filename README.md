# Olist E-commerce Analytics

브라질 전자상거래 플랫폼 Olist의 2016–2018 공개 데이터를 이용해 **Seller 확보, 고객 유지, 배송 운영 문제**를 분석한 팀 프로젝트입니다.

이 저장소는 당시 발표자료와 **복구된 원본 분석 notebook**을 바탕으로, 면접·코드리뷰에서 분석 흐름과 실제 코드를 함께 확인할 수 있도록 재구성했습니다.

## Business Questions

- **B2B** — 어떤 Seller를 더 확보해야 marketplace 성장을 만들 수 있는가?
- **B2C** — 신규 고객을 기존 고객으로 전환하려면 무엇을 개선해야 하는가?
- **Operations** — 배송 지연 문제를 어디에서 우선 해결해야 하는가?

## Data

Olist 공개 데이터의 9개 CSV를 사용했습니다.

- Customers
- Payments
- Geolocation
- Reviews
- Order Items
- Orders
- Products
- Sellers
- Category Name

## Data Validation & Preprocessing

### Join duplication

단순 schema join을 적용하면 n:n 관계 때문에 동일 주문이 여러 행으로 증식하는 문제가 있었습니다.

특히:

- `order_item_id`: 동일 주문 내 품목 순번
- `payment_sequential`: 하나의 주문에서 여러 결제수단/결제가 발생할 때 결제 순서

때문에 `order_id` 기준 merge 시 실제 주문보다 행 수가 커질 수 있음을 확인했습니다.

분석 목적에 따라 `order_id.nunique()`를 사용하고 Payment merge를 필요한 경우에만 적용하는 방식으로 대응했습니다.

### Missing / abnormal values

발표자료에 기록된 주요 처리:

- `review_comment_message`: 빈 문자열 대체
- 일부 product/review/category 결측: 분석 목적에 따라 제거
- 가격 0인 데이터 제거
- 구매→출고→배송 흐름에 맞지 않는 timestamp 제거
- 분석 기간 밖의 2016년·2018년 9월 일부 데이터 제거
- 날짜형 변환 및 배송기간 파생변수 생성

발표자료 기준 shape는 **113,314 × 24 → 105,898 × 33**으로 정리되었습니다.

자세한 내용: [Data Processing Notes](./docs/data-processing.md)

## Analysis 1 · Seller Acquisition

### Seller growth

Seller 수와 Order Count의 관계를 확인했고, 발표자료에는 **Pearson correlation 0.979, p-value 0.000**으로 기록되어 있습니다.

### Core categories

전체 74개 카테고리 중 상위 10개 카테고리가 전체 주문량의 약 **65%**를 차지했습니다.

주요 카테고리의 seller 집중도를 HHI로 확인했으며, 발표자료에서는 대부분의 주요 카테고리가 **HHI < 0.15**로 나타났습니다.

### Emerging categories

주요 카테고리 외 성장 후보를 찾기 위해:

- 월 평균 주문 50건 이상
- 전월 대비 평균 성장률

조건으로 성장 카테고리를 선별했습니다.

### OLS scenario

발표자료의 OLS 분석에서는 seller 1명 증가 시:

- 주문 약 **5.3건 증가**
- 매출 약 **136.4 BRL 증가**

시나리오가 제시되었습니다.

이 수치는 관측 데이터 기반 회귀 결과이며 실제 seller 추가의 인과효과를 의미하지 않습니다.

## Analysis 2 · Customer Retention

발표자료에서는 대부분 고객이 신규 고객이며, 기존/재구매 고객 비중이 약 **1.6%**로 나타났습니다.

월별 Review Score와 신규→기존 고객 전환 흐름을 비교했고:

- 평균 Review Score 약 **4.1**
- 전월 전환율과 만족도: **Spearman 0.31, p=0.01**

로 기록되어 있습니다.

## Analysis 3 · Delivery & Satisfaction

배송기간과 Review Score의 관계를 확인한 결과:

- 배송기간 vs Review Score: **Spearman -0.22, p=0.00**

으로 기록되어 있습니다.

60일 이후 구간은 전체의 약 **0.3%**로 표본이 매우 작아 별도로 다뤘고, 나머지 99.7% 데이터에서는 배송기간이 길어질수록 평균 Review Score가 하락하는 패턴을 확인했습니다.

## Dashboard

세 가지 관점의 대시보드를 구성했습니다.

### Company-wide
- 총 매출
- 주문 수
- Seller 수
- Customer 수
- 평균 Review Score
- 월별 주문/Seller 추이
- 카테고리/지역별 성과

### Seller
- Seller 증가율
- Target Category 주문 비중
- 성장 카테고리
- Seller 증가 시 주문/매출 시나리오

### Customer / Logistics
- 신규 vs 기존 고객
- Review Score
- 배송기간별 Review Score
- 배송 지연 지역
- Hub 관련 운영 지표

자세한 분석 맥락: [Business Insights](./docs/business-insights.md)

## Reviewable Code

- [Cleaned Analysis Notebook](./notebooks/01_olist_analysis.ipynb) — 복구된 원본 notebook의 데이터 로딩·merge·배송/리뷰 EDA 흐름을 정리
- [Preprocessing Pipeline](./src/preprocessing.py) — 원본 전처리 로직을 함수 단위로 재구성하고 payment 중복 위험을 보완

원본 notebook에서는 payment 행을 order/item과 직접 merge하는 실험도 수행했습니다. 정리된 pipeline은 주문당 payment를 먼저 집계해 n:n 증식 위험을 줄였습니다.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── notebooks/
│   └── 01_olist_analysis.ipynb
├── src/
│   └── preprocessing.py
└── docs/
    ├── business-insights.md
    └── data-processing.md
```

## What This Project Demonstrates

- 관계형 데이터 join에서 생기는 중복 원인 검증
- 분석 단위와 unique count 정의
- 비즈니스 질문을 지표로 변환
- 상관/회귀/HHI를 활용한 가설 검증
- Tableau 대시보드와 실행 우선순위 연결

## Source Note

프로젝트 발표자료와 함께 **실제 Olist CSV를 불러와 전처리·merge·EDA를 수행한 원본 notebook을 복구**했습니다.

공개 repository에는 원본 실행 출력과 임시 셀을 그대로 복사하지 않고, 실제 분석 로직을 확인할 수 있는 cleaned notebook과 reviewable pipeline을 정리했습니다. 원본 CSV는 저장소에 포함하지 않습니다.
