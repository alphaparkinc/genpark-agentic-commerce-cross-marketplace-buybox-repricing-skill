# Cross-Marketplace Buy Box Algorithmic Repricing Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Multi-channel ecommerce Buy Box competitive price velocity tracking (Amazon, Walmart, eBay), algorithmic penny-undercutting, minimum advertised price (MAP) compliance guard, and gross margin floor protector. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_optimal_buybox_price`: Determine competitive Buy Box winning price across Amazon and Walmart while honoring MAP policy and minimum profit margin floor.
- `generate_repricing_feed_payload`: Synthesize automated SP-API (Selling Partner API) or Walmart Marketplace price feed update JSON payload.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_cross_marketplace_buybox_repricing_skill.server --test
```
