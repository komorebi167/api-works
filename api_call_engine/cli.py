import argparse
import asyncio
import json
import httpx
from api_client import fetch_api

def parse_params(param_list: list[str]) -> dict:
    params = {}
    for item in param_list:
        if "=" not in item:
            raise ValueError(f"パラメータ '{item}' は key=value の形式で指定してください")
        key, value = item.split("=", 1)
        params[key] = value
    return params

async def main(url: str, param_list: list[str]):
    try:
        params = parse_params(param_list)
        response_data = await fetch_api(url, params)
        print(json.dumps(response_data, ensure_ascii=False, indent=2))

    except httpx.HTTPStatusError as e:
        print(f"通信エラー（HTTPステータス）: {e.response.status_code} {e.response.reason_phrase}")
        print(f"URL: {e.request.url}")

    except httpx.RequestError as e:
        print(f"通信エラー（接続失敗など）: {str(e)}")
        print(f"URL: {e.request.url}")

    except Exception as e:
        print(f"予期しないエラー: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="任意のAPIに複数のクエリパラメータを渡して結果を取得するツール")
    parser.add_argument("url", help="APIのエンドポイントURL")
    parser.add_argument("params", nargs="+", help="クエリパラメータ（例: zipcode=3620011 foo=bar）")
    args = parser.parse_args()

    asyncio.run(main(args.url, args.params))