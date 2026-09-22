# Data Processing Notes

이 문서는 Olist 프로젝트 발표자료에 기록된 전처리 판단을 요약합니다.

## 1. Join Duplication

Olist 데이터는 주문, 결제, 리뷰, 상품이 서로 1:n 또는 n:n 관계를 가질 수 있습니다.

특히 `payment_sequential`이나 `order_item_id`가 포함된 상태에서 `order_id`만 기준으로 여러 테이블을 결합하면 동일 주문이 여러 행으로 확장될 수 있었습니다.

따라서 분석 목적에 따라 다음 원칙을 적용했습니다.

- 주문 수: `order_id.nunique()`
- 상품 수: order/item 기준
- 결제 정보: 결제 분석에서만 제한적으로 사용
- 불필요한 payment field는 최종 통합 테이블에서 제외

## 2. Missing Values

- `review_comment_message`: 빈 문자열로 대체
- product/review/category 관련 결측: 분석 목적에 따라 제거
- 제품 수치형 결측은 해당 분석에서 필요 여부를 보고 처리

## 3. Abnormal Values

다음 사례를 비정상 데이터로 검토했습니다.

- `payment_value = 0`
- 구매보다 출고/배송 시점이 먼저 기록된 경우
- 분석 범위 밖의 일부 기간
- 배송기간 60일 초과 극단 구간

## 4. Derived Variables

- 구매→고객 수령까지 배송기간
- 월/연도 단위 집계 변수
- 카테고리별 주문/판매자 수
- 신규/기존 고객 구분
- 지역별 배송기간

## 5. Shape

발표자료 기준 통합 데이터 shape는:

```text
113,314 rows × 24 columns
→
105,898 rows × 33 columns
```

로 정리되었습니다.

이 문서는 당시 발표자료가 실제로 지원하는 처리 내용만 반영합니다.
