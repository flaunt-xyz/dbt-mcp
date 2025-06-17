import logging

from dbtsl.api.shared.query_params import GroupByParam
from mcp.server.fastmcp import FastMCP

from dbt_mcp.config.config import SemanticLayerConfig
from dbt_mcp.prompts.prompts import get_prompt
from dbt_mcp.semantic_layer.client import get_semantic_layer_fetcher
from dbt_mcp.semantic_layer.types import (
    DimensionToolResponse,
    EntityToolResponse,
    MetricToolResponse,
    OrderByParam,
    ComposeQueryResponse,
)

logger = logging.getLogger(__name__)


def register_sl_tools(dbt_mcp: FastMCP, config: SemanticLayerConfig) -> None:
    semantic_layer_fetcher = get_semantic_layer_fetcher(config)

    @dbt_mcp.tool(description=get_prompt("semantic_layer/list_metrics"))
    def list_metrics() -> list[MetricToolResponse] | str:
        return semantic_layer_fetcher.list_metrics()

    @dbt_mcp.tool(description=get_prompt("semantic_layer/get_dimensions"))
    def get_dimensions(metrics: list[str]) -> list[DimensionToolResponse] | str:
        return semantic_layer_fetcher.get_dimensions(metrics=metrics)

    @dbt_mcp.tool(description=get_prompt("semantic_layer/get_entities"))
    def get_entities(metrics: list[str]) -> list[EntityToolResponse] | str:
        return semantic_layer_fetcher.get_entities(metrics=metrics)

    @dbt_mcp.tool(description=get_prompt("semantic_layer/compose_query"))
    def compose_query(
        metrics: list[str],
        group_by: list[GroupByParam] | None = None,
        order_by: list[OrderByParam] | None = None,
        where: str | None = None,
        limit: int | None = None,
    ) -> ComposeQueryResponse:
        return semantic_layer_fetcher.compose_query(
            metrics=metrics,
            group_by=group_by,
            order_by=order_by,
            where=where,
            limit=limit,
        )
