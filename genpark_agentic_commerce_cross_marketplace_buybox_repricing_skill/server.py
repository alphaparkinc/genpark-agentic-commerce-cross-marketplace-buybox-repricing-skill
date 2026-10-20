# -*- coding: utf-8 -*-
"""MCP Server for Cross-Marketplace Buy Box Algorithmic Repricing Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import CrossMarketplaceBuyBoxRepricer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_optimal_buybox_price",
        "description": "Determine competitive Buy Box winning price across Amazon and Walmart while honoring MAP policy and minimum profit margin floor.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string"
                },
                "current_competitor_buybox_price": {
                    "type": "number"
                },
                "unit_cost_cogs": {
                    "type": "number"
                },
                "marketplace_referral_fee_pct": {
                    "type": "number",
                    "description": "e.g. 15.0%"
                },
                "fba_fulfillment_fee_usd": {
                    "type": "number"
                },
                "map_minimum_advertised_price": {
                    "type": "number"
                },
                "minimum_net_margin_pct": {
                    "type": "number",
                    "description": "e.g. 12.0%"
                }
            },
            "required": [
                "sku",
                "current_competitor_buybox_price",
                "unit_cost_cogs",
                "fba_fulfillment_fee_usd",
                "map_minimum_advertised_price"
            ]
        }
    },
    {
        "name": "generate_repricing_feed_payload",
        "description": "Synthesize automated SP-API (Selling Partner API) or Walmart Marketplace price feed update JSON payload.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "marketplace": {
                    "type": "string",
                    "enum": [
                        "AMAZON_US",
                        "WALMART_US",
                        "EBAY_US"
                    ]
                },
                "sku": {
                    "type": "string"
                },
                "new_target_price": {
                    "type": "number"
                },
                "expected_margin_usd": {
                    "type": "number"
                }
            },
            "required": [
                "marketplace",
                "sku",
                "new_target_price",
                "expected_margin_usd"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-cross-marketplace-buybox-repricing-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(CrossMarketplaceBuyBoxRepricer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-cross-marketplace-buybox-repricing-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-cross-marketplace-buybox-repricing-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
