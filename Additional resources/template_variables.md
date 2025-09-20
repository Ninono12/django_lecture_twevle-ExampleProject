# Django Template Variables Guide

## 1. Variable Basics

### Syntax
```django
{{ variable_name }}
```

Template variables are placeholders that get replaced with actual data from your Django views. They're enclosed in double curly braces and automatically HTML-escaped for security.

### Simple Example
**views.py:**
```python
def home(request):
    context = {'username': 'Alice', 'age': 25}
    return render(request, 'home.html', context)
```

**template.html:**
```django
<h1>Welcome, {{ username }}!</h1>
<p>You are {{ age }} years old.</p>
<!-- Output: Welcome, Alice! You are 25 years old. -->
```

### How Variables Work
- Variables are resolved against the template context (data from views)
- Return empty string if variable doesn't exist
- Case-sensitive names
- Automatically HTML-escaped to prevent XSS attacks

## 2. Variable Types

### Strings
```python
context = {
    'title': 'My Blog Post',
    'description': 'Learn Django templates',
}
```

```django
<h1>{{ title }}</h1>
<p>{{ description }}</p>
<p>{{ missing_var|default:"No content" }}</p>
```

### Numbers
```python
context = {
    'price': 29.99,
    'quantity': 5,
    'views': 1234
}
```

```django
<p>Price: ${{ price }}</p>
<p>Quantity: {{ quantity }}</p>
<p>Views: {{ views|intcomma }}</p>  <!-- Output: 1,234 -->
```

### Booleans
```python
context = {
    'is_published': True,
    'is_featured': False,
}
```

```django
{% if is_published %}
    <span class="badge">Published</span>
{% endif %}

<p>Status: {{ is_published|yesno:"Live,Draft" }}</p>
<!-- Output: Status: Live -->
```

### Lists
```python
context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],
    'colors': ['red', 'green', 'blue']
}
```

```django
<p>First fruit: {{ fruits.0 }}</p>  <!-- Apple -->
<p>Last fruit: {{ fruits.2 }}</p>   <!-- Cherry -->
<p>All fruits: {{ fruits|join:", " }}</p>  <!-- Apple, Banana, Cherry -->

<ul>
{% for fruit in fruits %}
    <li>{{ forloop.counter }}: {{ fruit }}</li>
{% endfor %}
</ul>
```

### Dictionaries
```python
context = {
    'user': {
        'name': 'John',
        'email': 'john@example.com',
        'active': True
    },
    'settings': {
        'theme': 'dark',
        'language': 'en'
    }
}
```

```django
<p>Name: {{ user.name }}</p>
<p>Email: {{ user.email }}</p>
<p>Theme: {{ settings.theme }}</p>
<p>Language: {{ settings.language }}</p>
```

### Django Objects
```python
# In your view
context = {
    'article': Article.objects.get(pk=1),  # Django model instance
    'user': request.user  # Current user
}
```

```django
<h1>{{ article.title }}</h1>
<p>By {{ article.author.username }} on {{ article.created_at|date:"M j, Y" }}</p>
<p>Content: {{ article.content|truncatewords:50 }}</p>

<!-- User object -->
<p>Welcome, {{ user.first_name }} {{ user.last_name }}</p>
<p>Email: {{ user.email }}</p>
```

## 3. Variable Access Methods

### Dot Notation
Django uses dots to access nested data:

```django
{{ object.attribute }}     <!-- Object attribute -->
{{ dictionary.key }}       <!-- Dictionary key -->
{{ list.0 }}              <!-- List item by index -->
{{ user.profile.bio }}     <!-- Nested attributes -->
```

### Real Examples
```python
context = {
    'post': {
        'title': 'Django Tips',
        'author': {'name': 'Alice', 'email': 'alice@example.com'},
        'tags': ['python', 'django', 'web'],
        'stats': {'views': 1500, 'likes': 89}
    }
}
```

```django
<h1>{{ post.title }}</h1>
<p>By {{ post.author.name }} ({{ post.author.email }})</p>
<p>Tags: {{ post.tags|join:", " }}</p>
<p>{{ post.stats.views }} views, {{ post.stats.likes }} likes</p>
```

### Method Calls (No Parentheses)
```python
# In your model or view
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
```

```django
<p>Full name: {{ user.get_full_name }}</p>
<p>Username: {{ user.username }}</p>
<p>Is staff: {{ user.is_staff|yesno }}</p>
```

## 4. Built-in Variables

Django automatically provides certain variables in templates:

### Request Object
```django
<p>Current page: {{ request.path }}</p>
<p>Method: {{ request.method }}</p>
<p>User agent: {{ request.META.HTTP_USER_AGENT }}</p>
<p>Search query: {{ request.GET.q|default:"No search" }}</p>
```

### User Object
```django
{% if user.is_authenticated %}
    <p>Hello, {{ user.username }}!</p>
    {% if user.is_staff %}
        <a href="/admin/">Admin Panel</a>
    {% endif %}
{% else %}
    <a href="/login/">Please log in</a>
{% endif %}
```

### Loop Variables (in {% for %} loops)
```django
<table>
{% for item in items %}
    <tr class="{% if forloop.first %}first{% endif %}">
        <td>{{ forloop.counter }}</td>  <!-- 1, 2, 3... -->
        <td>{{ item.name }}</td>
        <td>
            {% if forloop.last %}
                Last item!
            {% endif %}
        </td>
    </tr>
{% endfor %}
</table>
```

**Available forloop variables:**
- `forloop.counter` - Current iteration (1, 2, 3...)
- `forloop.counter0` - Current iteration (0, 1, 2...)
- `forloop.first` - True if first iteration
- `forloop.last` - True if last iteration
- `forloop.revcounter` - Countdown (3, 2, 1...)

## 5. Variable Filters

Filters modify variables using the pipe symbol `|`:

### Text Filters
```django
{{ name|lower }}              <!-- Convert to lowercase -->
{{ title|title }}             <!-- Title Case -->
{{ content|truncatewords:10 }} <!-- First 10 words -->
{{ text|length }}             <!-- Length of string -->
{{ html_content|striptags }}   <!-- Remove HTML tags -->
```

### Number Filters
```django
{{ price|floatformat:2 }}     <!-- 29.99 (2 decimal places) -->
{{ big_number|intcomma }}     <!-- 1,234,567 -->
{{ 0.85|floatformat:1 }}%     <!-- 85.0% -->
```

### Date Filters
```django
{{ article.created_at|date:"F j, Y" }}        <!-- March 15, 2024 -->
{{ comment.created_at|timesince }} ago        <!-- 2 hours ago -->
{{ event.date|date:"l" }}                     <!-- Monday -->
```

### Default Values
```django
{{ bio|default:"No bio available" }}
{{ avatar|default:"/static/default-avatar.png" }}
{{ is_active|yesno:"Yes,No,Maybe" }}
```

### List Filters
```django
{{ fruits|join:", " }}        <!-- Apple, Banana, Cherry -->
{{ items|length }}            <!-- Number of items -->
{{ numbers|first }}           <!-- First item -->
{{ quotes|random }}           <!-- Random item -->
```

### Chaining Filters
You can use multiple filters together:
```django
{{ title|lower|title|truncatechars:20 }}
{{ content|striptags|truncatewords:15|default:"No content" }}
```

## 6. Special Variable Cases

### HTML Escaping
By default, Django escapes HTML to prevent security issues:
```django
{{ user_input }}           <!-- Automatically escaped -->
{{ trusted_html|safe }}    <!-- Mark as safe (be careful!) -->
```

### Missing Variables
```python
# In settings.py, you can control what happens with missing variables
TEMPLATES = [{
    'OPTIONS': {
        'string_if_invalid': 'MISSING',  # Show 'MISSING' instead of empty string
    },
}]
```

### Complex Nested Access
```python
context = {
    'data': [
        {'user': {'profile': {'settings': {'theme': 'dark'}}}},
        {'user': {'profile': {'settings': {'theme': 'light'}}}}
    ]
}
```

```django
<p>First user theme: {{ data.0.user.profile.settings.theme }}</p>
<p>Second user theme: {{ data.1.user.profile.settings.theme }}</p>
```

## 7. Common Patterns

### Safe Attribute Access
```django
<!-- Use default filter to handle missing values -->
{{ user.profile.bio|default:"No bio available" }}
{{ post.author.get_full_name|default:post.author.username }}
```

### Conditional Display
```django
{% if user.is_authenticated %}
    Welcome, {{ user.first_name|default:user.username }}!
{% else %}
    <a href="/login/">Please log in</a>
{% endif %}
```

### Working with Forms
```django
<!-- Display form field values and errors -->
<input type="text" name="title" value="{{ form.title.value|default:'' }}">
{% if form.title.errors %}
    <div class="error">{{ form.title.errors.0 }}</div>
{% endif %}
```

## 8. Debugging Variables

### Debug Tag
```django
{% debug %}
<!-- Shows all available variables in the template context -->
```

### Temporary Display
```django
<!-- Temporarily show variable content for debugging -->
<pre>{{ complex_variable|pprint }}</pre>
```

### Common Issues
- **Typos in variable names**: `{{ usernme }}` instead of `{{ username }}`
- **Wrong dot notation**: `{{ user-profile }}` instead of `{{ user.profile }}`
- **Missing context**: Variable not passed from view
- **Case sensitivity**: `{{ Username }}` vs `{{ username }}`

### Checking Variable Existence
```django
{% if variable %}
    {{ variable }}
{% else %}
    Variable is missing or empty
{% endif %}
```

## 9. Best Practices

1. **Use descriptive variable names** in your views:
   ```python
   context = {
       'current_user': user,      # Better than 'u'
       'recent_posts': posts,     # Better than 'data'
       'page_title': title        # Clear purpose
   }
   ```

2. **Provide defaults** for optional data:
   ```django
   {{ user.bio|default:"No bio provided" }}
   {{ settings.theme|default:"light" }}
   ```

3. **Use filters** to format data consistently:
   ```django
   {{ price|floatformat:2 }}        <!-- Always 2 decimals -->
   {{ date_created|date:"M j, Y" }}  <!-- Consistent date format -->
   ```

4. **Keep templates readable**:
   ```django
   <!-- Good -->
   <p>Price: {{ product.price|floatformat:2 }}</p>
   
   <!-- Avoid complex chaining -->
   <p>{{ product.name|lower|title|truncatechars:20|default:"No name" }}</p>
   ```

5. **Handle missing data gracefully**:
   ```django
   {% if articles %}
       {% for article in articles %}
           <h3>{{ article.title }}</h3>
       {% endfor %}
   {% else %}
       <p>No articles available.</p>
   {% endif %}
   ```
