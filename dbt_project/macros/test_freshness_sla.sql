{% macro test_freshness_sla(source_name, table_name, loaded_at_field, warn_hours, error_hours) %}
{% set warn_h = warn_hours | default(var('freshness_warn_hours', 6)) %}
{% set error_h = error_hours | default(var('freshness_error_hours', 12)) %}
with freshness as (
    select max({{ loaded_at_field }}) as latest_load,
           datediff('hour', max({{ loaded_at_field }}), current_timestamp) as hours_since_load
    from {{ source(source_name, table_name) }}
)
select * from freshness where hours_since_load > {{ error_h }}
{% endmacro %}
