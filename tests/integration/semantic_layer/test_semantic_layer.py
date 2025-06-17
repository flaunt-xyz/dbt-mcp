from dbtsl.api.shared.query_params import GroupByParam, GroupByType

from dbt_mcp.config.config import load_config
from dbt_mcp.semantic_layer.client import get_semantic_layer_fetcher
from dbt_mcp.semantic_layer.types import OrderByParam

config = load_config()


def test_semantic_layer_list_metrics():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    metrics = semantic_layer_fetcher.list_metrics()
    assert len(metrics) > 0


def test_semantic_layer_list_dimensions():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    metrics = semantic_layer_fetcher.list_metrics()
    dimensions = semantic_layer_fetcher.get_dimensions(metrics=[metrics[0].name])
    assert len(dimensions) > 0


def test_semantic_layer_create_query():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    result = semantic_layer_fetcher.create_query(
        metrics=["avg_click_rate"],
        group_by=[
            GroupByParam(
                name="metric_time",
                type=GroupByType.TIME_DIMENSION,
                grain=None,
            )
        ],
    )
    assert result.sql is not None
    assert result.error is None


def test_semantic_layer_create_query_complex():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    result = semantic_layer_fetcher.create_query(
        metrics=["avg_conversion_rate"],
        group_by=[
            GroupByParam(
                name="campaign__campaign_name",
                type=GroupByType.DIMENSION,
                grain=None,
            ),
            GroupByParam(
                name="metric_time",
                type=GroupByType.TIME_DIMENSION,
                grain="MONTH",
            ),
        ],
        order_by=[
            OrderByParam(
                name="metric_time",
                descending=True,
            ),
            OrderByParam(
                name="campaign__campaign_name",
                descending=True,
            ),
        ],
        limit=5,
    )
    assert result.sql is not None
    assert result.error is None


def test_semantic_layer_create_query_with_group_by_grain():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    result = semantic_layer_fetcher.create_query(
        metrics=["avg_click_rate"],
        group_by=[
            GroupByParam(
                name="metric_time",
                type=GroupByType.TIME_DIMENSION,
                grain="day",
            )
        ],
    )
    if isinstance(result, dict):
        assert "sql" in result
        assert result["sql"] is not None
        assert result["error"] is None
    else:
        assert hasattr(result, 'sql')
        assert result.sql is not None
        assert result.error is None


def test_semantic_layer_create_query_with_order_by():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    result = semantic_layer_fetcher.create_query(
        metrics=["avg_click_rate"],
        group_by=[
            GroupByParam(
                name="metric_time",
                type=GroupByType.TIME_DIMENSION,
                grain=None,
            )
        ],
        order_by=[OrderByParam(name="metric_time", descending=True)],
    )
    if isinstance(result, dict):
        assert "sql" in result
        assert result["sql"] is not None
        assert result["error"] is None
    else:
        assert hasattr(result, 'sql')
        assert result.sql is not None
        assert result.error is None


def test_semantic_layer_create_query_with_misspellings():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    result = semantic_layer_fetcher.create_query(["avg_click_ratee"])
    assert hasattr(result, 'error')
    assert result.error is not None
    assert "avg_click_rate" in result.error


def test_semantic_layer_get_entities():
    semantic_layer_fetcher = get_semantic_layer_fetcher(config.semantic_layer_config)
    entities = semantic_layer_fetcher.get_entities(
        metrics=["avg_click_rate"]
    )
    assert len(entities) > 0
