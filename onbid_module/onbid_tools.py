import os
import httpx
from typing import Optional

# 공공데이터포털 디코딩 인증키 환경변수
DATA_GO_KR_API_KEY = os.environ.get("DATA_GO_KR_API_KEY", "")

# 차세대 온비드 공고상세 물건정보 조회 기본 엔드포인트
BASE_URL = "http://apis.data.go.kr/B551220/onbidPbctCltrInfoService"

def register_onbid_tools(mcp):
    """FastMCP 인스턴스에 온비드 공매 조회 도구들을 등록하는 함수"""

    @mcp.tool()
    async def search_onbid_items(
        keyword: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 10
    ) -> str:
        """
        캠코 차세대 온비드 공매 물건 목록을 검색합니다.
        
        Args:
            keyword: 검색어 (물건명, 용도 또는 지역명 등)
            page_no: 페이지 번호 (기본 1)
            num_of_rows: 한 번에 조회할 건수 (기본 10건)
        """
        api_key = os.environ.get("DATA_GO_KR_API_KEY", DATA_GO_KR_API_KEY)
        if not api_key:
            return "오류: DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다."

        endpoint = f"{BASE_URL}/getCltrList"
        params = {
            "serviceKey": api_key,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
            "resultType": "json",
        }
        if keyword:
            params["cltrNm"] = keyword  # 물건명/키워드

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(endpoint, params=params)
                if response.status_code != 200:
                    return f"API 호출 실패 (HTTP {response.status_code}): {response.text}"
                
                data = response.json()
                body = data.get("response", {}).get("body", {})
                items = body.get("items", {}).get("item", [])
                
                if not items:
                    return f"'{keyword or '전체'}' 조건에 해당하는 온비드 공매 물건이 없습니다."

                if isinstance(items, dict):
                    items = [items]

                result_lines = [f"=== 온비드 공매 물건 검색 결과 (총 {body.get('totalCount', len(items))}건 중 {len(items)}건) ===\n"]
                for i, it in enumerate(items, 1):
                    cltr_no = it.get("cltrNo", "N/A")            # 물건관리번호
                    cltr_nm = it.get("cltrNm", "N/A")            # 물건명
                    ctgr_nm = it.get("ctgrFullNm", "N/A")        # 용도/분류
                    appr_amt = it.get("appraisalAmt", "0")       # 감정평가금액
                    min_bid_amt = it.get("minBidAmt", "0")       # 최저입찰가
                    bid_start = it.get("bidBegnDtm", "N/A")      # 입찰시작일시
                    bid_end = it.get("bidClsDtm", "N/A")         # 입찰마감일시
                    
                    result_lines.append(
                        f"[{i}] {cltr_nm}\n"
                        f" - 물건번호: {cltr_no}\n"
                        f" - 용도: {ctgr_nm}\n"
                        f" - 감정가: {int(appr_amt):,}원 | 최저입찰가: {int(min_bid_amt):,}원\n"
                        f" - 입찰기간: {bid_start} ~ {bid_end}\n"
                    )

                return "\n".join(result_lines)
            except Exception as e:
                return f"온비드 API 조회 중 오류 발생: {str(e)}"

    @mcp.tool()
    async def get_onbid_item_detail(cltr_no: str) -> str:
        """
        물건관리번호(cltr_no)를 기반으로 해당 공매 물건의 상세 제원 및 유찰/입찰 정보를 조회합니다.
        
        Args:
            cltr_no: 온비드 물건관리번호 (search_onbid_items에서 확인)
        """
        api_key = os.environ.get("DATA_GO_KR_API_KEY", DATA_GO_KR_API_KEY)
        if not api_key:
            return "오류: DATA_GO_KR_API_KEY 환경변수가 설정되지 않았습니다."

        endpoint = f"{BASE_URL}/getCltrDetail"
        params = {
            "serviceKey": api_key,
            "cltrNo": cltr_no,
            "resultType": "json",
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(endpoint, params=params)
                if response.status_code != 200:
                    return f"API 호출 실패 (HTTP {response.status_code}): {response.text}"
                
                data = response.json()
                item = data.get("response", {}).get("body", {}).get("item", {})
                if not item:
                    return f"물건번호 '{cltr_no}'에 대한 상세 정보를 찾을 수 없습니다."

                return (
                    f"=== 온비드 물건 상세 정보: {item.get('cltrNm', 'N/A')} ===\n"
                    f"- 물건번호: {item.get('cltrNo', 'N/A')}\n"
                    f"- 처분방식: {item.get('dispsMthdNm', '매각')}\n"
                    f"- 소재지/주소: {item.get('ldnmAddr', item.get('nmrAddr', '정보없음'))}\n"
                    f"- 감정평가액: {int(item.get('appraisalAmt', 0)):,}원\n"
                    f"- 최저입찰가: {int(item.get('minBidAmt', 0)):,}원 (유찰회차: {item.get('uscCnt', 0)}회)\n"
                    f"- 입찰기간: {item.get('bidBegnDtm', 'N/A')} ~ {item.get('bidClsDtm', 'N/A')}\n"
                    f"- 담당기관: {item.get('orgNm', '캠코')}\n"
                    f"- 물건상세설명: {item.get('cltrDesc', '내용 없음')}\n"
                )
            except Exception as e:
                return f"온비드 상세 조회 중 오류 발생: {str(e)}"