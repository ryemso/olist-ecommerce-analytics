# Business Insights

## 1. Seller Acquisition

### Why Seller growth matters

Olist의 B2B 수익 구조에서 Seller 확보는 marketplace 상품 공급과 주문 증가에 연결될 수 있는 핵심 운영 과제였습니다.

발표자료 기준 Seller 수와 Order Count의 Pearson 상관계수는 **0.979**로 기록되어 있습니다.

이는 높은 동행성을 보여주지만, Seller 증가가 주문 증가를 직접적으로 유발한다는 인과관계를 의미하지는 않습니다.

### Core categories

전체 74개 카테고리 중 상위 10개가 약 **65%**의 주문량을 차지했습니다.

주요 카테고리의 HHI는 대부분 **0.15 미만**으로 기록되어 있어, 특정 Seller가 시장을 독점하는 구조라기보다 여러 Seller가 경쟁하는 분산된 구조로 해석했습니다.

### Emerging categories

월 평균 주문 50건 이상을 기준으로 필터링한 뒤 전월 대비 평균 성장률로 성장 카테고리를 정리했습니다.

### OLS scenario

발표자료의 회귀 분석에서는 Seller 1명 증가 시:

- 주문 약 **5.3건**
- 매출 약 **136.4 BRL**

증가하는 시나리오가 제시되었습니다.

이 값은 관측 데이터에 기반한 회귀 추정치이며 정책 실행의 확정 효과가 아닙니다.

## 2. Customer Retention

분석 데이터에서는 재구매/기존 고객 비중이 약 **1.6%**로 나타났습니다.

월별 Review Score와 신규→기존 고객 전환 흐름의 Spearman 상관계수는 **0.31 (p=0.01)**로 기록되었습니다.

따라서 고객 만족도는 고객 유지와 함께 관찰할 필요가 있는 지표로 정리했습니다.

## 3. Delivery & Review Score

배송기간과 Review Score의 Spearman 상관계수는 **-0.22**로 기록되었습니다.

60일 초과 배송 구간은 전체의 약 **0.3%**로 표본이 매우 작아 별도로 분리했고, 나머지 구간에서는 배송기간이 길어질수록 평균 Review Score가 낮아지는 경향을 확인했습니다.

## 4. Dashboard Use

### Company-wide
- 주문
- 매출
- Seller
- Customer
- Review Score

### Seller
- Seller 증가율
- Target Category 비중
- 성장 카테고리
- Seller 증가 시 주문/매출 시나리오

### Customer / Logistics
- 신규 vs 기존 고객
- Review Score
- 배송기간
- 배송 지연 지역
- Hub 관련 운영 지표

분석 결과를 단순 EDA로 끝내지 않고, 운영팀·마케팅팀·CS/물류 관점의 의사결정 화면으로 연결하는 것이 프로젝트의 주요 목표였습니다.
