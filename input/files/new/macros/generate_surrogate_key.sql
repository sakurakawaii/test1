{% macro generate_surrogate_key(field_list) %}

    {%- set fields = [] -%}

    {%- for field in field_list -%}
        {%- set _ = fields.append(
            "coalesce(cast(" ~ field ~ " as varchar), '_null_')"
        ) -%}
    {%- endfor -%}

    to_hex(sha2_binary('acct_v2|' || {{ fields | join(" || '|' || ") }}))

{% endmacro %}
