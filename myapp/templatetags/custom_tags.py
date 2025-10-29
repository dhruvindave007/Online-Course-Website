from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def compact_page_range(page_obj, window=2):
    """
    Return a compact page range list for pagination with ellipses.
    Example output: [1, '...', 4, 5, 6, '...', 10]
    window controls how many pages to show around current page.
    """
    if not page_obj:
        return []
    total = page_obj.paginator.num_pages
    current = page_obj.number
    if total <= (window * 2) + 5:
        return list(range(1, total + 1))

    left = max(1, current - window)
    right = min(total, current + window)
    pages = []
    if left > 2:
        pages.extend([1, '...'])
    else:
        pages.extend(range(1, left))

    pages.extend(range(left, right + 1))

    if right < total - 1:
        pages.extend(['...', total])
    else:
        pages.extend(range(right + 1, total + 1))

    return pages