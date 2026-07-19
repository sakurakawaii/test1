{% macro first_touch_feature(array_col) %}

    ELEMENT_AT({{ array_col }}, 1)

{% endmacro %}
