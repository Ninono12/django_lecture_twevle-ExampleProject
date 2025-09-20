# Django Template Tags

## 1. Tag Basics

### Syntax
```django
{% tag_name argument %}
```

### Key Characteristics
- Perform logic rather than display values
- Can create blocks ({% tag %}...{% endtag %})
- Over 25 built-in tags available
- Extensible through custom tags

## 2. Essential Control Tags

### Conditional Logic
```django
{% if user.is_authenticated %}
  Welcome back!
{% elif user.is_anonymous %}
  Please log in
{% else %}
  Error state
{% endif %}
```

### Looping
```django
{% for item in items %}
  <p>{{ forloop.counter }}. {{ item.name }}</p>
{% empty %}
  <p>No items available</p>
{% endfor %}
```

### Special Loop Variables
- `forloop.counter` (1-based index)
- `forloop.counter0` (0-based index)
- `forloop.revcounter` (reverse count)
- `forloop.first`/`forloop.last` (boolean)

## 3. Template Structure Tags

Django provides special template tags to help you organize and reuse your HTML code. These tags make your templates easier to maintain and keep consistent across pages.

---

### **Inheritance**

```django
{% extends "base.html" %}
```

* **Purpose:** Allows one template to build on another.
* **How it works:** The child template takes the layout from `base.html` and can replace or add content in predefined **blocks**.
* **Example use case:** Having a single layout (navigation, footer, styles) while customizing only the page-specific parts.

---

### **Includes**

```django
{% include "header.html" %}
{% include "footer.html" with year=2023 only %}
```

* **Purpose:** Reuse smaller template fragments inside other templates.
* **Example use case:** Put your site’s header and footer in separate files and include them wherever needed.
* **`with ... only`:** Pass extra context variables to the included template while keeping the rest of the parent’s context out.

---

### **Block Composition**

```django
{% block title %}
  {{ block.super }} - Subpage
{% endblock %}
```

* **Purpose:** Define placeholders in a parent template (`base.html`) that child templates can override.
* **`block.super`:** Keeps the parent block’s content and lets you add to it instead of fully replacing it.
* **Example use case:** In the `<title>` tag, you can keep the base title and add a page-specific title.

## 4. URL Handling Tags

Django’s `{% url %}` tag is used to **dynamically generate URLs** in templates. Instead of hardcoding paths (`/products/123/`), you reference the view name from your `urls.py`. This makes links reliable and easier to maintain when URLs change.

---

### **Basic URL**

```django
<a href="{% url 'view_name' %}">Link</a>
```

* **Purpose:** Generate a URL to a view using its name from `urls.py`.
* **Why:** If you later change the actual path in `urls.py`, your templates will still work as long as the view name stays the same.
* **Example use case:** Linking to a home page or about page.

---

### **With Arguments**

```django
{% url 'product_detail' product.id %}
```

* **Purpose:** Pass arguments (like IDs or slugs) that the view expects.
* **Positional arguments:** Values passed in the same order they appear in `urls.py`.
* **Example use case:** Linking to a specific product detail page using `product.id`.

---

### **Namespaced URLs**

```django
{% url 'shop:product_view' category='electronics' %}
```

* **Purpose:** Resolve view names when multiple apps have similarly named views.
* **Namespace:** Defined in the app’s `urls.py` with `app_name = 'shop'`.
* **Keyword arguments:** You can pass named parameters if the URL pattern requires them.
* **Example use case:** Linking to `shop` app’s product view, ensuring no conflicts with another app’s product view.

## 5. Special Purpose Tags

These tags don’t control structure or URLs but serve **specific purposes** like security, commenting, and debugging.

---

### **CSRF Protection**

```django
<form method="post">
  {% csrf_token %}
</form>
```

* **Purpose:** Protects forms against **Cross-Site Request Forgery (CSRF)** attacks.
* **How it works:** Generates a hidden token that must match the one stored in the user’s session.
* **When to use:** Always include inside any `<form>` that makes a `POST` request.
* ⚠️ Without `{% csrf_token %}`, Django will reject the form submission with a `403 Forbidden` error.

---

### **Comments**

```django
{# Single-line comment #}

{% comment "Optional note" %}
  Multi-line
  comment block
{% endcomment %}
```

* **Purpose:** Add notes or temporarily disable template code.
* **Types:**

  * `{# ... #}` → short, inline comments.
  * `{% comment %} ... {% endcomment %}` → larger blocks, can include template tags.
* **Important:** These comments **do not appear** in the rendered HTML (unlike HTML `<!-- ... -->` comments).

---

### **Debugging**

```django
{% debug %}  {# Shows complete context #}
```

* **Purpose:** Displays all variables currently available in the template’s context.
* **Output:** A dictionary-like dump, including `user`, `request`, `csrf_token`, and any variables you passed in.
* **Visibility:** It appears **directly on the rendered page** (not in the console).
* **When to use:** Debugging variable availability during development.
* ⚠️ Never leave `{% debug %}` in production—it exposes sensitive data.

## 6. Debugging Template Tags

When templates don’t behave as expected, the issue is often with missing context, incorrect tag usage, or template inheritance. Django provides ways to track and fix these problems.

---

### **Common Issues**

1. **Missing Load Tag**

   ```django
   {% load custom_tags %}
   ```

   * **Problem:** Custom filters or tags don’t work.
   * **Fix:** Ensure you’ve loaded the correct template tag library at the top of your template.

2. **Syntax Errors**

   ```django
   {% if user.is_authenticated %}
     Hello
   {% endif %}
   ```

   * **Problem:** Forgetting `{% endif %}`, misplacing braces, or nesting tags incorrectly.
   * **Fix:** Check that every `{% if %}`, `{% for %}`, etc. has a proper closing tag.

3. **Context Issues**

   ```django
   {{ product.name }}
   ```

   * **Problem:** Variable doesn’t exist in the context (e.g., `product` wasn’t passed from the view).
   * **Fix:** Double-check the view’s `context` dictionary or `render()` call.

4. **Circular Extends**

   ```django
   {% extends "base.html" %}
   ```

   * **Problem:** Template A extends B, and B extends A → infinite loop.
   * **Fix:** Ensure inheritance only flows one way.

---

### **Debugging Techniques**

1. **Check the `django.template` Logger**

   * Enable debug logging in `settings.py` to see detailed template errors.

2. **Use `{% debug %}`**

   ```django
   {% debug %}
   ```

   * Prints all variables available in the current template context.
   * Appears directly on the page → useful in development, unsafe in production.

3. **Verify Template Loaders**

   * In `settings.py`, ensure `DIRS` and `APP_DIRS` are correctly set in `TEMPLATES`.
   * Misconfigured loaders may prevent Django from finding your templates.
