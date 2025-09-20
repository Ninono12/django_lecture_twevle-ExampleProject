# Django Template Filters

## 1. Filter Basics

### Syntax
```django
{{ variable|filter_name:argument }}
```

### How Filters Work
- Transform variable values before output
- Can be chained (left-to-right evaluation)
- Some accept arguments, some don't
- Over 60 built-in filters available

## 2. Essential Filters

### String Filters
| Filter | Example | Result |
|--------|---------|--------|
| `lower` | `{{ "HELLO"\|lower }}` | "hello" |
| `upper` | `{{ "hello"\|upper }}` | "HELLO" |
| `title` | `{{ "hello world"\|title }}` | "Hello World" |
| `truncatechars` | `{{ "Long text"\|truncatechars:5 }}` | "Long..." |
| `truncatewords` | `{{ "A B C D"\|truncatewords:2 }}` | "A B..." |

### Number Filters
| Filter | Example | Result |
|--------|---------|--------|
| `floatformat` | `{{ 3.14159\|floatformat:2 }}` | "3.14" |
| `intcomma` | `{{ 1000000\|intcomma }}` | "1,000,000" |
| `filesizeformat` | `{{ 1024\|filesizeformat }}` | "1 KB" |

### Date/Time Filters
| Filter | Example | Result |
|--------|---------|--------|
| `date` | `{{ today\|date:"Y-m-d" }}` | "2023-07-15" |
| `time` | `{{ now\|time:"H:i" }}` | "14:30" |
| `timesince` | `{{ past_date\|timesince }}` | "3 days" |

## 3. Special Purpose Filters

### Default Values
```django
{{ undefined_var|default:"Not available" }}
```

### List/Array Handling
```django
{{ items|join:", " }}  # Apple, Banana, Cherry
{{ items|length }}    # 3
{{ items|first }}     # Apple
{{ items|last }}      # Cherry
{{ items|slice:":2" }} # First two items
```

### HTML/URL Handling
```django
{{ text|linebreaks }}  # Converts newlines to <br>
{{ text|urlize }}      # Makes URLs clickable
{{ html|safe }}        # Marks as safe HTML
{{ url|urlencode }}    # Encodes for URLs
```

## 4. Filter Chaining

### Examples
```django
{{ title|lower|truncatechars:20 }}
{{ content|striptags|truncatewords:50 }}
{{ user.bio|default:"No bio"|title }}
```

### Evaluation Order
1. `{{ var|filter1|filter2|filter3 }}`
2. Processes left-to-right:
   - `var → filter1 → result1`
   - `result1 → filter2 → result2`
   - `result2 → filter3 → final_result`

## 5. Custom Filters

### 1. Create `templatetags/custom_filters.py`
```python
from django import template

register = template.Library()

@register.filter
def currency(value):
    return f"${value:,.2f}"

@register.filter(name='shorten')
def shorten_text(value, length=10):
    return value[:length] + '...' if len(value) > length else value
```

### 2. Usage in Templates
```django
{% load custom_filters %}

{{ product.price|currency }}  # $1,299.99
{{ long_text|shorten:20 }}   # Truncates to 20 chars
```

## 6. Advanced Filter Techniques

### Conditional Filtering
```django
{{ value|default_if_none:"N/A" }}
{{ list|random }}  # Picks random item
```

### Math Operations
```django
{{ value|add:"5" }}    # Numeric addition
{{ list1|add:list2 }}  # List concatenation
```

### String Formatting
```django
{{ "Hello {0}"|format:user.name }}
{{ "ID: {id}"|format:id=product.id }}
```

## 7. Security Considerations

### Safe Filter
```django
{{ user_input|safe }}  # DANGEROUS with untrusted input
```

### Recommended Practice
```django
{{ user_input|striptags }}  # Remove HTML tags
{{ user_input|escape }}     # HTML escape
```

## 8. Debugging Filters

### Common Issues
1. **Missing Load Tag**: Forgot `{% load custom_filters %}`
2. **Wrong Type**: Applying string filter to number
3. **Argument Errors**: Passing wrong argument type
4. **Chaining Order**: Unexpected filter sequence results

### Debugging Techniques
```django
{{ value|pprint }}  # Show raw value
{{ value|filter_debug }}  # Some filters have debug versions
```
